"""Top-level CLI process return-code behavior contracts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_INJECTED_MAIN_DRIVER = """
import argparse
import os
import sys

from hermes_cli import config
from hermes_cli import main as main_mod

values = {
    "none": None,
    "false": False,
    "true": True,
    "zero": 0,
    "two": 2,
    "negative_one": -1,
    "text_two": "2",
}
value = values[os.environ["D6_TEST_RETURN_VALUE"]]

config.get_container_exec_info = lambda: None
main_mod._prepare_agent_startup = lambda args: None
argparse.ArgumentParser.parse_args = lambda self, args=None: argparse.Namespace(
    version=False,
    yolo=False,
    oneshot=None,
    resume=None,
    continue_last=None,
    command="d6-test-handler",
    func=lambda args: value,
)
sys.argv = ["hermes", "d6-test-handler"]
main_mod.main()
"""


def _isolated_env(home: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HERMES_HOME"] = str(home)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env.pop("BWS_ACCESS_TOKEN", None)
    return env


def _run_injected_main(
    tmp_path: Path, value_name: str
) -> subprocess.CompletedProcess[str]:
    driver = tmp_path / "injected_main.py"
    driver.write_text(_INJECTED_MAIN_DRIVER, encoding="utf-8")
    env = _isolated_env(tmp_path / f"home-{value_name}")
    env["D6_TEST_RETURN_VALUE"] = value_name
    return subprocess.run(
        [sys.executable, str(driver)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def _run_cli(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "hermes_cli.main", *args],
        cwd=REPO_ROOT,
        env=_isolated_env(tmp_path / "cli-home"),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


@pytest.mark.parametrize(
    ("value_name", "expected_code"),
    [
        ("none", 0),
        ("false", 0),
        ("true", 0),
        ("zero", 0),
        ("two", 2),
        ("text_two", 0),
    ],
)
def test_main_propagates_only_exact_integer_return_codes(
    tmp_path: Path, value_name: str, expected_code: int
) -> None:
    result = _run_injected_main(tmp_path, value_name)

    assert result.returncode == expected_code


@pytest.mark.skipif(os.name != "posix", reason="POSIX shell return-code normalization")
def test_main_preserves_negative_integer_return_code_semantics(tmp_path: Path) -> None:
    result = _run_injected_main(tmp_path, "negative_one")

    assert result.returncode == 255


def test_egress_configuration_failure_reaches_the_shell(tmp_path: Path) -> None:
    home = tmp_path / "cli-home"
    home.mkdir()
    (home / "config.yaml").write_text(
        "proxy:\n"
        "  enabled: true\n"
        "  credential_source: bitwarden\n"
        "secrets:\n"
        "  bitwarden:\n"
        "    enabled: false\n",
        encoding="utf-8",
    )

    result = _run_cli(tmp_path, "egress", "start")

    assert result.returncode == 1
    assert "Refusing to start" in result.stdout


def test_missing_kanban_task_reaches_the_shell(tmp_path: Path) -> None:
    result = _run_cli(tmp_path, "kanban", "show", "definitely_missing")

    assert result.returncode == 1
    assert "no such task" in result.stderr


def test_invalid_kanban_board_reaches_the_shell(tmp_path: Path) -> None:
    result = _run_cli(tmp_path, "kanban", "--board", "bad slug", "list")

    assert result.returncode == 2
    assert "invalid board slug" in result.stderr


def test_argparse_misuse_remains_exit_two(tmp_path: Path) -> None:
    result = _run_cli(tmp_path, "kanban", "--definitely-invalid")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_help_remains_success(tmp_path: Path) -> None:
    result = _run_cli(tmp_path, "--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout
