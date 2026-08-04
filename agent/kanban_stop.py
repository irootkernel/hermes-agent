"""Turn-end guard for kanban workers.

Kanban workers must end with a successful terminal or run-release board transition.
Models
(especially GLM / Qwen families) sometimes narrate the next step
("Let me write the report now") and stop with ``finish_reason=stop`` and no
tool calls. Hermes treats that as a clean exit → ``rc=0`` → dispatcher
``protocol_violation``.

This module is policy-only: when a kanban worker tries to finish without a
terminal board tool, return a bounded synthetic nudge so the conversation
loop continues instead of exiting.
"""

from __future__ import annotations

import json
import os
from typing import Iterable, Optional


_TERMINAL_KANBAN_TOOLS = frozenset({"kanban_complete", "kanban_block"})
_RUN_RELEASE_KANBAN_TOOLS = frozenset({
    "kanban_reassign",
    "kanban_submit_review",
    "kanban_submit_result",
    "kanban_request_changes",
})

_STOP_SATISFYING_KANBAN_TOOLS = (
    _TERMINAL_KANBAN_TOOLS | _RUN_RELEASE_KANBAN_TOOLS
)

_DEFAULT_MAX_ATTEMPTS = 2


def kanban_stop_nudge_enabled() -> bool:
    """Return whether the kanban stop-guard is active for this process.

    On when ``HERMES_KANBAN_TASK`` is set (dispatcher-spawned worker), unless
    ``HERMES_KANBAN_STOP_NUDGE`` explicitly disables it.
    """
    env = os.environ.get("HERMES_KANBAN_STOP_NUDGE")
    if env is not None and env.strip().lower() in {"0", "false", "no", "off"}:
        return False
    task = (os.environ.get("HERMES_KANBAN_TASK") or "").strip()
    return bool(task)


def _successful_tool_result(msg: dict[str, object]) -> bool:
    content = msg.get("content")
    if isinstance(content, dict):
        payload = content
    elif isinstance(content, str):
        try:
            payload = json.loads(content)
        except (TypeError, ValueError, json.JSONDecodeError):
            return False
    else:
        return False
    return isinstance(payload, dict) and payload.get("ok") is True


def session_called_kanban_terminal(messages: Iterable[dict] | None) -> bool:
    """True if this conversation already invoked a terminal kanban tool."""
    if not messages:
        return False
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        if msg.get("role") == "tool":
            name = str(msg.get("name") or "")
            if (
                name in _STOP_SATISFYING_KANBAN_TOOLS
                and _successful_tool_result(msg)
            ):
                return True
    return False


def build_kanban_stop_nudge(
    *,
    messages: Iterable[dict] | None = None,
    attempts: int = 0,
    max_attempts: int = _DEFAULT_MAX_ATTEMPTS,
    task_id: Optional[str] = None,
) -> Optional[str]:
    """Return a synthetic follow-up when a kanban worker exits without a terminal tool.

    Returns ``None`` when the guard should not fire (not a kanban worker,
    already completed/blocked, or nudge budget exhausted).
    """
    if not kanban_stop_nudge_enabled():
        return None
    if attempts >= max_attempts:
        return None
    if session_called_kanban_terminal(messages):
        return None

    tid = (task_id or os.environ.get("HERMES_KANBAN_TASK") or "").strip() or "this task"
    return (
        "[System: You are a Hermes kanban worker. A plain-text reply is NOT a "
        "terminal state for the board.\n\n"
        f"Task `{tid}` is still `running`. Ending now without a successful board "
        "transition causes a protocol violation.\n\n"
        "Do this immediately in your next response — do not narrate intent:\n"
        "1. Finish any remaining deliverable (write the required file(s) now).\n"
        "2. Call `kanban_complete(summary=..., artifacts=[...])` if the current "
        "gate is final, `kanban_block(reason=...)` for a genuine blocker, or the "
        "appropriate run-release tool (`kanban_submit_result`, "
        "`kanban_submit_review`, `kanban_request_changes`, `kanban_reassign`) "
        "when the same card must move to another owner.\n\n"
        "Never end a turn with only a promise of future action. Repeated "
        "protocol violations will block this task and require manual intervention.]"
    )


__all__ = [
    "build_kanban_stop_nudge",
    "kanban_stop_nudge_enabled",
    "session_called_kanban_terminal",
]
