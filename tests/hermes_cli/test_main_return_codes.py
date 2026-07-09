import os
import subprocess
import sys

import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _run_hermes(tmp_path, *args):
    env = os.environ.copy()
    env["HERMES_HOME"] = str(tmp_path / ".hermes")
    env["PYTHONPATH"] = REPO_ROOT
    env.pop("HERMES_KANBAN_DB", None)
    env.pop("HERMES_KANBAN_BOARD", None)
    return subprocess.run(
        [sys.executable, "-m", "hermes_cli.main", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def test_top_level_cli_passthroughs_subcommand_return_code_1(tmp_path):
    result = _run_hermes(tmp_path, "kanban", "show", "definitely_missing")

    assert result.returncode == 1
    assert "no such task: definitely_missing" in result.stderr


def test_top_level_cli_passthroughs_subcommand_return_code_2(tmp_path):
    result = _run_hermes(tmp_path, "kanban", "--board", "bad slug", "list")

    assert result.returncode == 2
    assert "invalid board slug" in result.stderr


def test_top_level_cli_help_still_exits_zero(tmp_path):
    result = _run_hermes(tmp_path, "--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout


def test_exit_code_passthrough_ignores_bool():
    import importlib

    main_mod = importlib.import_module("hermes_cli.main")

    # The helper is only for exact ints. It should not raise on bools because
    # bool is a subclass of int and would otherwise turn True into shell rc=1.
    assert main_mod._exit_if_int_return(True) is None
    assert main_mod._exit_if_int_return(False) is None
    assert main_mod._exit_if_int_return(None) is None

    with pytest.raises(SystemExit) as exc_info:
        main_mod._exit_if_int_return(2)
    assert exc_info.value.code == 2
