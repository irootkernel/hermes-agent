"""Top-level Hermes CLI exit-code passthrough tests."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys

import pytest

cli_main = importlib.import_module("hermes_cli.main")


def _run_cli(tmp_path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["HERMES_HOME"] = str(tmp_path / ".hermes")
    env["PYTHONPATH"] = os.getcwd()
    return subprocess.run(
        [sys.executable, "-m", "hermes_cli.main", *args],
        cwd=os.getcwd(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_main_passthrough_missing_kanban_task_returns_nonzero(tmp_path):
    result = _run_cli(tmp_path, "kanban", "show", "definitely_missing_task")

    assert result.returncode == 1
    assert "no such task: definitely_missing_task" in result.stderr


def test_main_passthrough_kanban_usage_returns_two(tmp_path):
    result = _run_cli(tmp_path, "kanban", "boards", "switch", "")

    assert result.returncode == 2
    assert "slug is required" in result.stderr


def test_main_help_path_still_returns_zero(tmp_path):
    result = _run_cli(tmp_path, "kanban", "--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()


def test_main_return_code_passthrough_ignores_bool():
    cli_main._exit_if_int_return_code(True)
    cli_main._exit_if_int_return_code(False)


@pytest.mark.parametrize("rc", [0, 1, 2])
def test_main_return_code_passthrough_accepts_exact_int(rc):
    with pytest.raises(SystemExit) as exc:
        cli_main._exit_if_int_return_code(rc)

    assert exc.value.code == rc
