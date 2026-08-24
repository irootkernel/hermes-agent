"""Actual-process contracts for top-level CLI return-code propagation."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_DRIVER = """
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


def _run_main(tmp_path: Path, value_name: str) -> subprocess.CompletedProcess[str]:
    driver = tmp_path / "d6_main_driver.py"
    driver.write_text(_DRIVER, encoding="utf-8")
    env = os.environ.copy()
    env["HERMES_HOME"] = str(tmp_path / "home")
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["D6_TEST_RETURN_VALUE"] = value_name
    env.pop("BWS_ACCESS_TOKEN", None)
    return subprocess.run(
        [sys.executable, str(driver)],
        cwd=REPO_ROOT,
        env=env,
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
    result = _run_main(tmp_path, value_name)

    assert result.returncode == expected_code
