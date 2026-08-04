"""Tests for the kanban CLI surface (hermes_cli.kanban)."""

from __future__ import annotations

import argparse
import json
import os
import threading
from pathlib import Path

import pytest

from hermes_cli import kanban as kc
from hermes_cli import kanban_db as kb


@pytest.fixture
def kanban_home(tmp_path, monkeypatch):
    home = tmp_path / ".hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    kb.init_db()
    return home


# ---------------------------------------------------------------------------
# Workspace flag parsing
# ---------------------------------------------------------------------------







# ---------------------------------------------------------------------------
# run_slash smoke tests (end-to-end via the same entry both CLI and gateway use)
# ---------------------------------------------------------------------------



def test_kanban_list_json_includes_session_id(kanban_home):
    """JSON output exposes `session_id` so external clients (Scarf, web
    dashboards) don't need a side query to filter by chat session."""
    from hermes_cli import kanban_db as kb
    with kb.connect() as conn:
        kb.create_task(
            conn, title="acp task", assignee="alice", session_id="acp-x"
        )
    raw = kc.run_slash("list --json")
    payload = json.loads(raw)
    assert any(
        row.get("title") == "acp task"
        and row.get("session_id") == "acp-x"
        for row in payload
    )


def test_run_slash_create_and_dispatch_json_expose_mutex_key(kanban_home, monkeypatch):
    from hermes_cli import profiles

    monkeypatch.setattr(profiles, "profile_exists", lambda _name: True)
    first = json.loads(
        kc.run_slash(
            "create 'first mutex task' --assignee worker-a "
            "--mutex-key ' repo:rk ' --json"
        )
    )
    second = json.loads(
        kc.run_slash(
            "create 'second mutex task' --assignee worker-b "
            "--mutex-key repo:rk --json"
        )
    )
    assert first["mutex_key"] == "repo:rk"
    assert second["mutex_key"] == "repo:rk"

    dispatched = json.loads(kc.run_slash("dispatch --dry-run --max 10 --json"))
    assert [row["task_id"] for row in dispatched["spawned"]] == [first["id"]]
    assert dispatched["skipped_mutex_locked"] == [
        {"task_id": second["id"], "mutex_key": "repo:rk"}
    ]

    human = kc.run_slash("dispatch --dry-run")
    assert f"Deferred (mutex locked repo:rk): {second['id']}" in human


def test_run_slash_create_json_has_no_mutex_length_cap(kanban_home):
    long_key = "Repo://" + ("x" * 120_002)
    created = json.loads(
        kc.run_slash(
            f"create 'long mutex task' --assignee worker "
            f"--mutex-key {long_key} --json"
        )
    )
    assert len(created["mutex_key"]) == 120_009
    assert created["mutex_key"] == long_key
    with kb.connect() as conn:
        stored = kb.get_task(conn, created["id"])
        assert stored is not None and stored.mutex_key == long_key


def test_board_override_is_isolated_per_concurrent_call(kanban_home, monkeypatch):
    kb.create_board("alpha")
    kb.create_board("beta")

    parser = argparse.ArgumentParser(prog="hermes", add_help=False)
    sub = parser.add_subparsers(dest="command")
    kc.build_parser(sub)

    barrier = threading.Barrier(2)
    original_init_db = kb.init_db

    def slow_init_db(*args, **kwargs):
        try:
            barrier.wait(timeout=5)
        except threading.BrokenBarrierError:
            pass
        return original_init_db(*args, **kwargs)

    monkeypatch.setattr(kb, "init_db", slow_init_db)

    failures: list[str] = []

    def worker(board: str, title: str) -> None:
        args = parser.parse_args(["kanban", "--board", board, "create", title])
        rc = kc.kanban_command(args)
        if rc != 0:
            failures.append(f"{board}:{rc}")

    t1 = threading.Thread(target=worker, args=("alpha", "alpha-task"))
    t2 = threading.Thread(target=worker, args=("beta", "beta-task"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert failures == []

    with kb.connect_closing(board="alpha") as conn:
        alpha_titles = [row.title for row in kb.list_tasks(conn, limit=100)]
    with kb.connect_closing(board="beta") as conn:
        beta_titles = [row.title for row in kb.list_tasks(conn, limit=100)]

    assert alpha_titles == ["alpha-task"]
    assert beta_titles == ["beta-task"]


# ---------------------------------------------------------------------------
# Integration with the COMMAND_REGISTRY
# ---------------------------------------------------------------------------






# ---------------------------------------------------------------------------
# reclaim + reassign CLI smoke tests
# ---------------------------------------------------------------------------

def test_run_slash_reclaim_running_task(kanban_home):
    import re
    import time
    import secrets
    from hermes_cli import kanban_db as kb

    out1 = kc.run_slash("create 'stuck worker task' --assignee broken-model")
    m = re.search(r"(t_[a-f0-9]+)", out1)
    assert m
    tid = m.group(1)

    # Simulate a running claim outside TTL.
    conn = kb.connect()
    try:
        lock = secrets.token_hex(4)
        conn.execute(
            "UPDATE tasks SET status='running', claim_lock=?, claim_expires=?, "
            "worker_pid=? WHERE id=?",
            (lock, int(time.time()) + 3600, 4242, tid),
        )
        conn.execute(
            "INSERT INTO task_runs (task_id, status, claim_lock, claim_expires, "
            "worker_pid, started_at) VALUES (?, 'running', ?, ?, ?, ?)",
            (tid, lock, int(time.time()) + 3600, 4242, int(time.time())),
        )
        rid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute("UPDATE tasks SET current_run_id=? WHERE id=?", (rid, tid))
        conn.commit()
    finally:
        conn.close()

    out = kc.run_slash(f"reclaim {tid} --reason 'test'")
    assert "Reclaimed" in out, out
    # Status back to ready.
    out2 = kc.run_slash(f"show {tid}")
    assert "ready" in out2.lower()




def test_run_slash_submit_result_requires_owned_run_and_emits_json(
    kanban_home, monkeypatch
):
    from hermes_cli import profiles

    monkeypatch.setattr(profiles, "profile_exists", lambda _name: True)
    with kb.connect() as conn:
        task_id = kb.create_task(
            conn,
            title="CLI result",
            assignee="worker",
            created_by="creator",
        )
        claimed = kb.claim_task(conn, task_id)
        assert claimed is not None
        run_id = claimed.current_run_id
        assert run_id is not None

    raw = kc.run_slash(
        f"submit-result {task_id} --run-id {run_id} "
        "--summary 'verified by CLI' --metadata '{\"tests_run\": 3}' --json"
    )
    payload = json.loads(raw)

    assert payload == {
        "assignee": "creator",
        "outcome": "submitted_result",
        "run_id": run_id,
        "status": "review",
        "task_id": task_id,
    }
    with kb.connect() as conn:
        task = kb.get_task(conn, task_id)
        run = kb.get_run(conn, run_id)
    assert task is not None and task.status == "review"
    assert run is not None and run.metadata == {"tests_run": 3}


def test_submit_result_cli_rejects_nonpositive_run_metadata_and_delegated_child(
    kanban_home, monkeypatch, capsys
):
    parser = argparse.ArgumentParser(prog="hermes", add_help=False)
    sub = parser.add_subparsers(dest="command")
    kc.build_parser(sub)

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(
            ["kanban", "submit-result", "t_fake", "--run-id", "0"]
        )
    assert exc_info.value.code == 2

    with kb.connect() as conn:
        task_id = kb.create_task(
            conn,
            title="CLI failure contracts",
            assignee="worker",
            created_by="creator",
        )
        claimed = kb.claim_task(conn, task_id)
        assert claimed is not None and claimed.current_run_id is not None
        run_id = claimed.current_run_id

    bad_metadata = parser.parse_args(
        [
            "kanban",
            "submit-result",
            task_id,
            "--run-id",
            str(run_id),
            "--metadata",
            "[]",
        ]
    )
    assert kc.kanban_command(bad_metadata) == 2
    assert "JSON object" in capsys.readouterr().err

    monkeypatch.setenv("HERMES_DELEGATED_CHILD_CONTEXT", "1")
    delegated = parser.parse_args(
        ["kanban", "submit-result", task_id, "--run-id", str(run_id)]
    )
    assert kc.kanban_command(delegated) == 1
    assert "delegate_task child" in capsys.readouterr().err
    with kb.connect() as conn:
        unchanged = kb.get_task(conn, task_id)
    assert unchanged is not None and unchanged.status == "running"
    assert unchanged.current_run_id == run_id


# ---------------------------------------------------------------------------
# /kanban specify — slash surface (same entry point CLI + gateway use)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# /kanban help / no-args / unknown-action UX (issue #21794)
# ---------------------------------------------------------------------------


