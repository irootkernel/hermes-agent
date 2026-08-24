"""Tests for multi-credential runtime pooling and rotation."""

from __future__ import annotations

import base64
import json
import stat
import time
from datetime import datetime, timezone

import pytest


def _write_auth_store(tmp_path, payload: dict) -> None:
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir(parents=True, exist_ok=True)
    (hermes_home / "auth.json").write_text(json.dumps(payload, indent=2))


def _jwt_with_claims(claims: dict) -> str:
    def _part(payload: dict) -> str:
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    return f"{_part({'alg': 'none', 'typ': 'JWT'})}.{_part(claims)}.sig"

















def test_explicit_reset_timestamp_overrides_default_429_ttl(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    # Prevent auto-seeding from Codex CLI tokens on the host
    monkeypatch.setattr(
        "hermes_cli.auth._import_codex_cli_tokens",
        lambda: None,
    )
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-1",
                        "label": "weekly-reset",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "tok-1",
                        "last_status": "exhausted",
                        "last_status_at": time.time() - 7200,
                        "last_error_code": 429,
                        "last_error_reason": "device_code_exhausted",
                        "last_error_reset_at": time.time() + 7 * 24 * 60 * 60,
                    }
                ]
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    assert pool.has_available() is False
    assert pool.select() is None




def test_billing_rotation_marks_all_entries_sharing_failed_key(tmp_path, monkeypatch):
    """A 402 must exhaust every pool entry backed by the same API key.

    Regression: the same key can back more than one pool entry — e.g. an
    explicit pool entry plus a ``model_config`` entry auto-seeded from
    ``model.api_key`` (both carry the identical ``runtime_api_key``).  When
    ``mark_exhausted_and_rotate`` is called with ``api_key_hint`` it matched
    only the *first* such entry, leaving the sibling OK.  ``_select_unlocked()``
    then kept handing back the same depleted key, so the billing-recovery
    ``continue`` loop in the conversation retry path never converged — the
    request hung ~2.5min until the client disconnected, with no 402 ever
    surfaced to the user.  All entries sharing the failed key must be
    exhausted so the pool reaches "no available entries" and the error
    propagates immediately.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    shared_key = "sk-deepseek-shared"
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "custom": [
                    {
                        "id": "cred-explicit",
                        "label": "520555",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "manual",
                        "access_token": shared_key,
                        "base_url": "https://api.deepseek.com",
                    },
                    {
                        "id": "cred-model-config",
                        "label": "model_config",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "manual",
                        "access_token": shared_key,
                        "base_url": "https://api.deepseek.com",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_EXHAUSTED

    pool = load_pool("custom")

    # First 402 on the shared key: rotation must NOT hand back a sibling
    # entry that wraps the same depleted key — it must converge to None.
    next_entry = pool.mark_exhausted_and_rotate(
        status_code=402,
        api_key_hint=shared_key,
    )
    assert next_entry is None

    # Both entries are now exhausted (not just the first match).
    statuses = {entry.id: entry.last_status for entry in pool.entries()}
    assert statuses["cred-explicit"] == STATUS_EXHAUSTED
    assert statuses["cred-model-config"] == STATUS_EXHAUSTED


def test_stale_credential_id_prefers_api_key_hint(tmp_path, monkeypatch):
    """#79156: disagreeing credential_id + api_key_hint must mark the key.

    After per-turn env refresh rewrites ``api_key`` without rebinding the
    pool entry id, recovery still passes the stale id of the healthy
    fallback together with the primary key that actually failed. The
    healthy key must not inherit the primary's 429.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", lambda: None)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "anthropic": [
                    {
                        "id": "cred-primary",
                        "label": "primary",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "manual",
                        "access_token": "sk-ant-api-primary",
                    },
                    {
                        "id": "cred-backup",
                        "label": "backup",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "manual",
                        "access_token": "sk-ant-api-backup",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_EXHAUSTED

    pool = load_pool("anthropic")
    next_entry = pool.mark_exhausted_and_rotate(
        status_code=429,
        api_key_hint="sk-ant-api-primary",
        credential_id="cred-backup",  # stale id after env refresh (#79156)
    )

    statuses = {entry.id: entry.last_status for entry in pool.entries()}
    assert statuses["cred-primary"] == STATUS_EXHAUSTED
    assert statuses["cred-backup"] != STATUS_EXHAUSTED
    # Rotation hands the healthy backup (or None if selection prefers next).
    if next_entry is not None:
        assert next_entry.id == "cred-backup"
        assert next_entry.runtime_api_key == "sk-ant-api-backup"


def test_unmatched_api_key_hint_rotates_without_benching_innocent_key(tmp_path, monkeypatch):
    """An api_key_hint matching no entry must not quarantine a healthy key.

    Regression: when the hint was unmatched (key rotated away, or a wrapper
    whose runtime key differs), mark_exhausted_and_rotate fell through to
    current()/_select_unlocked() — on a freshly loaded pool that selects the
    NEXT healthy key and benched it for the full cooldown TTL, punishing an
    innocent credential.  Now it rotates without marking anything.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    # Keep the dev machine's live ~/.claude credentials from seeding a
    # claude_code singleton entry into this pool (same isolation as the
    # other anthropic pool tests in this file).
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", lambda: None)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "anthropic": [
                    {
                        "id": "cred-1",
                        "label": "primary",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "manual",
                        "access_token": "sk-ant-api-primary",
                    },
                    {
                        "id": "cred-2",
                        "label": "secondary",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "manual",
                        "access_token": "sk-ant-api-secondary",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_DEAD, STATUS_EXHAUSTED

    # Freshly loaded pool: current() is None, exactly the shape of the bug.
    pool = load_pool("anthropic")

    next_entry = pool.mark_exhausted_and_rotate(
        status_code=429,
        api_key_hint="sk-ant-api-rotated-away",
    )

    # A fresh selection is still handed back so the caller can retry...
    assert next_entry is not None

    # ...but no credential was benched, in memory or on disk.
    assert all(
        entry.last_status not in (STATUS_EXHAUSTED, STATUS_DEAD)
        for entry in pool.entries()
    )
    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    for persisted in auth_payload["credential_pool"]["anthropic"]:
        assert persisted.get("last_status") not in (STATUS_EXHAUSTED, STATUS_DEAD)
        assert persisted.get("last_error_code") is None


def test_token_invalidated_marks_credential_dead(tmp_path, monkeypatch):
    """OpenAI Codex token_invalidated must mark the credential DEAD, not exhausted.

    Regression for #32849: when an OAuth credential is revoked upstream, the
    1-hour exhausted TTL means it re-enters rotation every hour and fails
    again with the same 401 — surfacing as "Failed to generate context
    summary" on context compression.  Terminal OAuth failures should never
    auto-recover.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-dead",
                        "label": "revoked",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "revoked-at",
                        "refresh_token": "revoked-rt",
                    },
                    {
                        "id": "cred-ok",
                        "label": "healthy",
                        "auth_type": "oauth",
                        "priority": 1,
                        "source": "manual:device_code",
                        "access_token": "healthy-at",
                        "refresh_token": "healthy-rt",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_DEAD

    pool = load_pool("openai-codex")
    assert pool.select().id == "cred-dead"

    # Simulate the exact OpenAI Codex 401 token_invalidated response shape.
    next_entry = pool.mark_exhausted_and_rotate(
        status_code=401,
        error_context={
            "reason": "token_invalidated",
            "message": "Your authentication token has been invalidated. Please try signing in again.",
        },
    )

    # Rotation still works — we hand off to the healthy credential.
    assert next_entry is not None
    assert next_entry.id == "cred-ok"

    # The revoked credential is now permanently marked DEAD.
    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted = auth_payload["credential_pool"]["openai-codex"][0]
    assert persisted["last_status"] == STATUS_DEAD
    assert persisted["last_error_code"] == 401
    assert persisted["last_error_reason"] == "token_invalidated"


def test_dead_credential_never_re_enters_rotation_after_ttl(tmp_path, monkeypatch):
    """A DEAD credential must stay excluded regardless of how much time passes.

    The exhausted TTL clears entries after 5 min (401) / 1 hour (429).
    A DEAD credential has no recovery TTL — it stays dead until either
    (a) an explicit re-auth write-side sync rewrites the tokens, or
    (b) the manual-prune TTL elapses (covered by separate tests below).
    This test verifies the core invariant in the recent-entry window.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    # DEAD entry from 2 hours ago — well past the exhausted TTLs (5min/1h)
    # but well within the 24h manual-prune window.
    two_hours_ago = time.time() - (2 * 3600)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-dead",
                        "label": "revoked",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "revoked-at",
                        "refresh_token": "revoked-rt",
                        "last_status": "dead",
                        "last_status_at": two_hours_ago,
                        "last_error_code": 401,
                        "last_error_reason": "token_invalidated",
                    },
                    {
                        "id": "cred-ok",
                        "label": "healthy",
                        "auth_type": "oauth",
                        "priority": 1,
                        "source": "manual:device_code",
                        "access_token": "healthy-at",
                        "refresh_token": "healthy-rt",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_DEAD

    pool = load_pool("openai-codex")
    selected = pool.select()
    # Should skip the dead entry and pick the healthy one — even though
    # the dead entry has priority 0 (would normally be picked first) and
    # plenty of time has passed since it was marked dead.
    assert selected is not None
    assert selected.id == "cred-ok"

    # The DEAD entry is still marked dead on disk — not cleared by TTL.
    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    dead_entry = next(e for e in auth_payload["credential_pool"]["openai-codex"]
                       if e["id"] == "cred-dead")
    assert dead_entry["last_status"] == STATUS_DEAD


def test_429_rate_limit_still_uses_exhausted_not_dead(tmp_path, monkeypatch):
    """429 rate limits must NOT be treated as terminal.

    They should keep the existing 1-hour TTL cooldown semantics so the
    credential re-enters rotation once the rate window resets.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-1",
                        "label": "primary",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "at-1",
                        "refresh_token": "rt-1",
                    },
                    {
                        "id": "cred-2",
                        "label": "secondary",
                        "auth_type": "oauth",
                        "priority": 1,
                        "source": "manual:device_code",
                        "access_token": "at-2",
                        "refresh_token": "rt-2",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_EXHAUSTED

    pool = load_pool("openai-codex")
    assert pool.select().id == "cred-1"

    next_entry = pool.mark_exhausted_and_rotate(
        status_code=429,
        error_context={"reason": "rate_limit_exceeded", "message": "Rate limit exceeded"},
    )
    assert next_entry is not None
    assert next_entry.id == "cred-2"

    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted = auth_payload["credential_pool"]["openai-codex"][0]
    # 429 stays exhausted (transient) — NOT dead.
    assert persisted["last_status"] == STATUS_EXHAUSTED
    assert persisted["last_error_code"] == 429


def test_generic_401_without_terminal_reason_still_uses_exhausted(tmp_path, monkeypatch):
    """A 401 with no specific code/reason should keep TTL semantics.

    Only specific terminal reasons (token_invalidated, token_revoked, etc.)
    transition to DEAD.  A generic 401 might be a transient server-side
    issue worth retrying after the 5-min TTL.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-1",
                        "label": "primary",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "at-1",
                        "refresh_token": "rt-1",
                    },
                    {
                        "id": "cred-2",
                        "label": "secondary",
                        "auth_type": "oauth",
                        "priority": 1,
                        "source": "manual:device_code",
                        "access_token": "at-2",
                        "refresh_token": "rt-2",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool, STATUS_EXHAUSTED

    pool = load_pool("openai-codex")
    pool.select()

    # 401 with no specific reason — stays exhausted, NOT dead.
    pool.mark_exhausted_and_rotate(
        status_code=401,
        error_context={"message": "Unauthorized"},
    )

    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted = auth_payload["credential_pool"]["openai-codex"][0]
    assert persisted["last_status"] == STATUS_EXHAUSTED
    assert persisted["last_error_code"] == 401


def test_dead_manual_entry_pruned_after_24h(tmp_path, monkeypatch):
    """A DEAD manual entry is removed from the pool after the prune TTL.

    Manual entries (``manual:*``) are independent credentials with no
    singleton to re-seed from, so we can clean them up after a quiet
    window without losing recoverability — the user can always re-add
    via ``hermes auth add``.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    # DEAD entry from > 24h ago
    long_ago = time.time() - (25 * 3600)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openai-codex": [
                    {
                        "id": "cred-old-dead",
                        "label": "ancient-dead",
                        "auth_type": "oauth",
                        "priority": 0,
                        "source": "manual:device_code",
                        "access_token": "stale",
                        "refresh_token": "stale",
                        "last_status": "dead",
                        "last_status_at": long_ago,
                        "last_error_code": 401,
                        "last_error_reason": "token_invalidated",
                    },
                    {
                        "id": "cred-ok",
                        "label": "healthy",
                        "auth_type": "oauth",
                        "priority": 1,
                        "source": "manual:device_code",
                        "access_token": "healthy-at",
                        "refresh_token": "healthy-rt",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    # Trigger _available_entries via select; that runs the prune.
    selected = pool.select()
    assert selected is not None
    assert selected.id == "cred-ok"

    # On-disk pool should have the dead entry removed.
    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted = auth_payload["credential_pool"]["openai-codex"]
    assert len(persisted) == 1
    assert persisted[0]["id"] == "cred-ok"






def test_load_pool_seeds_env_api_key(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-seeded")
    _write_auth_store(tmp_path, {"version": 1, "providers": {}})

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.source == "env:OPENROUTER_API_KEY"
    assert entry.access_token == "sk-or-seeded"



def test_load_pool_does_not_persist_env_seeded_secret_value(tmp_path, monkeypatch):
    """Runtime env keys may be used in memory but must not land in auth.json."""
    sentinel = "S3NTINEL_DO_NOT_PERSIST_OPENROUTER"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("OPENROUTER_API_KEY", sentinel)
    _write_auth_store(tmp_path, {"version": 1, "providers": {}})

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.source == "env:OPENROUTER_API_KEY"
    assert entry.access_token == sentinel

    auth_text = (tmp_path / "hermes" / "auth.json").read_text()
    assert sentinel not in auth_text
    persisted = json.loads(auth_text)["credential_pool"]["openrouter"][0]
    assert persisted["source"] == "env:OPENROUTER_API_KEY"
    assert persisted["label"] == "OPENROUTER_API_KEY"
    assert persisted["auth_type"] == "api_key"
    assert persisted["priority"] == 0
    assert "access_token" not in persisted
    assert persisted["secret_fingerprint"].startswith("sha256:")


def test_load_pool_collapses_duplicate_env_rows_to_active_key(tmp_path, monkeypatch):
    """One env source is one credential, even if auth.json contains stale duplicates."""
    key = "sk-or-active-main-key"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("OPENROUTER_API_KEY", key)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openrouter": [
                    {
                        "id": "current-row",
                        "label": "OPENROUTER_API_KEY",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "env:OPENROUTER_API_KEY",
                    },
                    {
                        "id": "stale-duplicate",
                        "label": "OPENROUTER_API_KEY",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "env:OPENROUTER_API_KEY",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")

    assert [(entry.id, entry.runtime_api_key) for entry in pool.entries()] == [
        ("current-row", key)
    ]
    persisted = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    assert [entry["id"] for entry in persisted["credential_pool"]["openrouter"]] == [
        "current-row"
    ]


def test_credential_pool_never_selects_empty_borrowed_entry():
    from agent.credential_pool import CredentialPool, PooledCredential

    pool = CredentialPool(
        "openrouter",
        [
            PooledCredential(
                provider="openrouter",
                id="metadata-only",
                label="OPENROUTER_API_KEY",
                auth_type="api_key",
                priority=0,
                source="env:OPENROUTER_API_KEY",
                access_token="",
            )
        ],
    )

    assert pool.select() is None
    assert pool.acquire_lease() is None


def test_load_pool_persists_bitwarden_origin_metadata_without_secret(tmp_path, monkeypatch):
    """Bitwarden-injected env vars retain source metadata but not raw values."""
    sentinel = "S3NTINEL_DO_NOT_PERSIST_BITWARDEN"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("OPENROUTER_API_KEY", sentinel)
    monkeypatch.setattr(
        "hermes_cli.env_loader.get_secret_source",
        lambda env_var: "bitwarden" if env_var == "OPENROUTER_API_KEY" else None,
    )
    _write_auth_store(tmp_path, {"version": 1, "providers": {}})

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.access_token == sentinel
    assert entry.source == "env:OPENROUTER_API_KEY"

    auth_text = (tmp_path / "hermes" / "auth.json").read_text()
    assert sentinel not in auth_text
    persisted = json.loads(auth_text)["credential_pool"]["openrouter"][0]
    assert persisted["source"] == "env:OPENROUTER_API_KEY"
    assert persisted["secret_source"] == "bitwarden"
    assert "access_token" not in persisted



def test_load_pool_sanitizes_legacy_raw_borrowed_entry_when_value_unchanged(tmp_path, monkeypatch):
    """Existing raw env-seeded pool entries are rewritten even if the env value matches."""
    sentinel = "S3NTINEL_DO_NOT_PERSIST_LEGACY_RAW"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("OPENROUTER_API_KEY", sentinel)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openrouter": [
                    {
                        "id": "legacy-env",
                        "label": "OPENROUTER_API_KEY",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "env:OPENROUTER_API_KEY",
                        "access_token": sentinel,
                        "base_url": "https://openrouter.ai/api/v1",
                    }
                ]
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.access_token == sentinel
    auth_text = (tmp_path / "hermes" / "auth.json").read_text()
    assert sentinel not in auth_text
    persisted = json.loads(auth_text)["credential_pool"]["openrouter"][0]
    assert persisted["id"] == "legacy-env"
    assert "access_token" not in persisted
    assert persisted["secret_fingerprint"].startswith("sha256:")



def test_pooled_credential_to_dict_strips_borrowed_secret_fields():
    from agent.credential_pool import PooledCredential

    sentinel = "S3NTINEL_DO_NOT_PERSIST_TO_DICT"
    credential = PooledCredential(
        provider="openrouter",
        id="borrowed-1",
        label="vault-ref",
        auth_type="api_key",
        priority=3,
        source="vault:openrouter/api-key",
        access_token=sentinel,
        refresh_token=f"refresh-{sentinel}",
        agent_key=f"agent-{sentinel}",
        request_count=7,
        last_status="ok",
        extra={
            "api_key": f"extra-{sentinel}",
            "client_secret": f"client-{sentinel}",
            "secret_key": f"secret-key-{sentinel}",
            "authToken": f"auth-token-{sentinel}",
            "refreshToken": f"camel-refresh-{sentinel}",
            "authorization": f"Bearer {sentinel}",
            "tokens": {"access_token": f"nested-{sentinel}"},
            "token_type": "Bearer",
            "scope": "inference",
        },
    )

    payload = credential.to_dict()
    serialized = json.dumps(payload)

    assert sentinel not in serialized
    assert "access_token" not in payload
    assert "refresh_token" not in payload
    assert "agent_key" not in payload
    assert "api_key" not in payload
    assert "client_secret" not in payload
    assert "secret_key" not in payload
    assert "authToken" not in payload
    assert "refreshToken" not in payload
    assert "authorization" not in payload
    assert "tokens" not in payload
    assert payload["source"] == "vault:openrouter/api-key"
    assert payload["label"] == "vault-ref"
    assert payload["request_count"] == 7
    assert payload["token_type"] == "Bearer"
    assert payload["scope"] == "inference"
    assert payload["secret_fingerprint"].startswith("sha256:")



@pytest.mark.parametrize("source", [
    "age://openrouter/api-key",
    "systemd",
    "keyring",
    "1password",
    "pass",
    "sops",
    "future_secret_store:openrouter",
])
def test_borrowed_source_variants_strip_secret_fields(source):
    from agent.credential_pool import PooledCredential

    sentinel = f"S3NTINEL_DO_NOT_PERSIST_{source.replace(':', '_').replace('/', '_')}"
    credential = PooledCredential(
        provider="openrouter",
        id="borrowed-variant",
        label="borrowed",
        auth_type="api_key",
        priority=0,
        source=source,
        access_token=sentinel,
        refresh_token=f"refresh-{sentinel}",
    )

    payload = credential.to_dict()
    serialized = json.dumps(payload)

    assert sentinel not in serialized
    assert "access_token" not in payload
    assert "refresh_token" not in payload
    assert payload["source"] == source
    assert payload["secret_fingerprint"].startswith("sha256:")






def test_write_credential_pool_sanitizes_borrowed_payload_at_disk_boundary(tmp_path, monkeypatch):
    """Direct dictionary callers cannot bypass the borrowed-secret guard."""
    sentinel = "S3NTINEL_DO_NOT_PERSIST_DIRECT_WRITE"
    manual_secret = "MANUAL_SECRET_STAYS_PERSISTABLE"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))

    from hermes_cli.auth import write_credential_pool

    write_credential_pool("openrouter", [
        {
            "id": "borrowed-1",
            "label": "systemd-ref",
            "auth_type": "api_key",
            "priority": 0,
            "source": "systemd://hermes/openrouter",
            "access_token": sentinel,
            "refresh_token": f"refresh-{sentinel}",
            "agent_key": f"agent-{sentinel}",
            "api_key": f"extra-{sentinel}",
        },
        {
            "id": "manual-1",
            "label": "manual",
            "auth_type": "api_key",
            "priority": 1,
            "source": "manual",
            "access_token": manual_secret,
        },
    ])

    auth_text = (tmp_path / "hermes" / "auth.json").read_text()
    assert sentinel not in auth_text
    assert manual_secret in auth_text
    entries = json.loads(auth_text)["credential_pool"]["openrouter"]
    borrowed, manual = entries
    assert borrowed["source"] == "systemd://hermes/openrouter"
    assert "access_token" not in borrowed
    assert "refresh_token" not in borrowed
    assert "agent_key" not in borrowed
    assert "api_key" not in borrowed
    assert borrowed["secret_fingerprint"].startswith("sha256:")
    assert manual["access_token"] == manual_secret



def test_write_credential_pool_treats_unowned_oauth_source_as_borrowed(tmp_path, monkeypatch):
    sentinel = "S3NTINEL_DO_NOT_PERSIST_UNOWNED_OAUTH"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))

    from hermes_cli.auth import write_credential_pool

    write_credential_pool("openrouter", [
        {
            "id": "unowned-oauth",
            "label": "unowned-oauth",
            "auth_type": "oauth",
            "priority": 0,
            "source": "oauth",
            "access_token": sentinel,
            "refresh_token": f"refresh-{sentinel}",
        }
    ])

    auth_text = (tmp_path / "hermes" / "auth.json").read_text()
    assert sentinel not in auth_text
    persisted = json.loads(auth_text)["credential_pool"]["openrouter"][0]
    assert persisted["source"] == "oauth"
    assert "access_token" not in persisted
    assert "refresh_token" not in persisted
    assert persisted["secret_fingerprint"].startswith("sha256:")



def test_write_credential_pool_preserves_known_provider_owned_oauth_state(tmp_path, monkeypatch):
    sentinel = "PROVIDER_OWNED_DEVICE_CODE_STAYS_PERSISTABLE"
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))

    from hermes_cli.auth import write_credential_pool

    write_credential_pool("nous", [
        {
            "id": "nous-device",
            "label": "device-code",
            "auth_type": "oauth",
            "priority": 0,
            "source": "device_code",
            "access_token": sentinel,
            "refresh_token": f"refresh-{sentinel}",
            "agent_key": f"agent-{sentinel}",
        }
    ])

    persisted = json.loads((tmp_path / "hermes" / "auth.json").read_text())["credential_pool"]["nous"][0]
    assert persisted["access_token"] == sentinel
    assert persisted["refresh_token"] == f"refresh-{sentinel}"
    assert persisted["agent_key"] == f"agent-{sentinel}"



def test_load_pool_prefers_dotenv_over_stale_os_environ(tmp_path, monkeypatch):
    """Regression for #18254: stale OPENROUTER_API_KEY in os.environ (inherited
    from a parent shell) must NOT shadow the fresh key in ~/.hermes/.env when
    seeding the credential pool. Before the fix, `get_env_value()` preferred
    os.environ and silently wrote the stale value into auth.json, causing
    persistent 401 errors after key rotation.
    """
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    # Simulate the bug: parent shell exported a stale test key
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-STALE-from-shell")

    # User edited ~/.hermes/.env with the fresh key
    (hermes_home / ".env").write_text(
        "OPENROUTER_API_KEY=sk-or-FRESH-from-dotenv\n"
    )

    _write_auth_store(tmp_path, {"version": 1, "providers": {}})

    from agent.credential_pool import load_pool
    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.source == "env:OPENROUTER_API_KEY"
    # The fresh key from .env must win over the stale shell export
    assert entry.access_token == "sk-or-FRESH-from-dotenv", (
        f"Expected .env to win, got {entry.access_token!r}"
    )


def test_load_pool_falls_back_to_os_environ_when_dotenv_empty(tmp_path, monkeypatch):
    """When ~/.hermes/.env does not define OPENROUTER_API_KEY (typical Docker /
    K8s / systemd deployment), seeding must still pick up the key from
    os.environ. Guards against regressions that would break production
    deployments relying on runtime-injected env vars.
    """
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-from-runtime-env")

    # .env exists but does not define OPENROUTER_API_KEY
    (hermes_home / ".env").write_text("SOME_OTHER_VAR=unrelated\n")

    _write_auth_store(tmp_path, {"version": 1, "providers": {}})

    from agent.credential_pool import load_pool
    pool = load_pool("openrouter")
    entry = pool.select()

    assert entry is not None
    assert entry.access_token == "sk-or-from-runtime-env"








def test_load_pool_mirrors_nous_invoke_jwt_agent_key_runtime_api_key(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    expires_at = datetime.fromtimestamp(time.time() + 3600, tz=timezone.utc).isoformat()
    token = _jwt_with_claims({
        "sub": "test-user",
        "scope": ["inference:invoke"],
        "exp": int(time.time() + 3600),
    })
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "active_provider": "nous",
            "providers": {
                "nous": {
                    "portal_base_url": "https://portal.example.com",
                    "inference_base_url": "https://inference.example.com/v1",
                    "client_id": "hermes-cli",
                    "token_type": "Bearer",
                    "scope": "inference:invoke",
                    "access_token": token,
                    "refresh_token": "refresh-token",
                    "expires_at": expires_at,
                    "agent_key": token,
                    "agent_key_expires_at": expires_at,
                }
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("nous")
    entry = pool.select()

    assert entry is not None
    assert entry.source == "device_code"
    assert entry.agent_key == token
    assert entry.runtime_api_key == token

    auth_payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    pool_entry = auth_payload["credential_pool"]["nous"][0]
    assert pool_entry["agent_key"] == token
    assert pool_entry["agent_key_expires_at"] == expires_at


def test_nous_runtime_api_key_rejects_opaque_agent_key():
    from agent.credential_pool import PooledCredential

    entry = PooledCredential(
        provider="nous",
        id="nous-opaque",
        label="opaque",
        auth_type="oauth",
        priority=0,
        source="device_code",
        access_token="opaque-access-token",
        refresh_token="refresh-token",
        agent_key="opaque-agent-key",
        agent_key_expires_at=datetime.fromtimestamp(
            time.time() + 3600,
            tz=timezone.utc,
        ).isoformat(),
        extra={"scope": "inference:invoke"},
    )

    assert entry.runtime_api_key == ""














def test_load_pool_api_key_path_skips_oauth_autodiscovery(tmp_path, monkeypatch):
    """API-key auth path: autodiscovered OAuth creds must NOT be seeded.

    When the user picks "Anthropic API key" at `hermes setup`,
    `save_anthropic_api_key()` writes ANTHROPIC_API_KEY and zeros
    ANTHROPIC_TOKEN.  That env-var pattern is the explicit signal that the
    user opted into the API-key path and explicitly OUT of the OAuth
    masquerade (Claude Code identity injection + `mcp_` tool-name rewrite
    + claude-cli user-agent).  Autodiscovered Claude Code / Hermes PKCE
    tokens from other tools' credential files must NOT be silently mixed
    into the anthropic pool — otherwise rotation on a 401/429 could flip
    the session onto OAuth credentials mid-conversation.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api03-explicit-user-key")
    monkeypatch.delenv("ANTHROPIC_TOKEN", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    _write_auth_store(tmp_path, {"version": 1, "providers": {}})
    monkeypatch.setattr("hermes_cli.auth.is_provider_explicitly_configured", lambda pid: True)

    pkce_called = {"n": 0}
    cc_called = {"n": 0}

    def _fake_pkce():
        pkce_called["n"] += 1
        return {
            "accessToken": "sk-ant-oat01-pkce-token",
            "refreshToken": "pkce-refresh",
            "expiresAt": int(time.time() * 1000) + 3_600_000,
        }

    def _fake_cc():
        cc_called["n"] += 1
        return {
            "accessToken": "sk-ant-oat01-claude-code-token",
            "refreshToken": "cc-refresh",
            "expiresAt": int(time.time() * 1000) + 3_600_000,
        }

    monkeypatch.setattr("agent.anthropic_adapter.read_hermes_oauth_credentials", _fake_pkce)
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", _fake_cc)

    from agent.credential_pool import load_pool

    pool = load_pool("anthropic")
    sources = {entry.source for entry in pool.entries()}

    # Only the explicit API-key entry should be in the pool.
    assert sources == {"env:ANTHROPIC_API_KEY"}, f"got {sources}"
    # And we should not have even called the autodiscovery readers.
    assert pkce_called["n"] == 0
    assert cc_called["n"] == 0


def test_load_pool_api_key_path_prunes_stale_oauth_entries(tmp_path, monkeypatch):
    """Switching OAuth -> API key must prune stale OAuth entries from auth.json.

    Without this, a user who logs into OAuth (seeding `claude_code` or
    `hermes_pkce` into auth.json) and later switches to the API key at
    `hermes setup` would still have those OAuth entries dormant on disk.
    Pool rotation on a transient 401 could revive them and flip the
    session onto the OAuth masquerade.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api03-explicit-user-key")
    monkeypatch.delenv("ANTHROPIC_TOKEN", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)

    # Plant a stale claude_code entry in the on-disk pool (as if a previous
    # OAuth session seeded it).
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {},
            "credential_pool": {
                "anthropic": [
                    {
                        "id": "stale1",
                        "source": "claude_code",
                        "auth_type": "oauth",
                        "access_token": "sk-ant-oat01-stale-claude-code",
                        "refresh_token": "stale-refresh",
                        "expires_at_ms": int(time.time() * 1000) + 3_600_000,
                        "priority": 0,
                        "label": "stale-claude-code",
                        "request_count": 0,
                    },
                ],
            },
        },
    )
    monkeypatch.setattr("hermes_cli.auth.is_provider_explicitly_configured", lambda pid: True)
    monkeypatch.setattr("agent.anthropic_adapter.read_hermes_oauth_credentials", lambda: None)
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", lambda: None)

    from agent.credential_pool import load_pool

    pool = load_pool("anthropic")
    sources = {entry.source for entry in pool.entries()}

    # Stale claude_code entry must be gone, API key must be present.
    assert "claude_code" not in sources
    assert "env:ANTHROPIC_API_KEY" in sources


def test_load_pool_oauth_path_still_autodiscovers(tmp_path, monkeypatch):
    """OAuth path: ANTHROPIC_TOKEN set, autodiscovery still fires.

    Regression guard: the API-key gate must not affect users who chose the
    OAuth path at `hermes setup`.  When ANTHROPIC_TOKEN is set (and
    ANTHROPIC_API_KEY is empty), autodiscovered Claude Code creds should
    still be seeded into the pool as before.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_TOKEN", "sk-ant-oat01-explicit-oauth-token")
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    _write_auth_store(tmp_path, {"version": 1, "providers": {}})
    monkeypatch.setattr("hermes_cli.auth.is_provider_explicitly_configured", lambda pid: True)

    monkeypatch.setattr(
        "agent.anthropic_adapter.read_hermes_oauth_credentials",
        lambda: None,
    )
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {
            "accessToken": "sk-ant-oat01-autodiscovered-cc",
            "refreshToken": "cc-refresh",
            "expiresAt": int(time.time() * 1000) + 3_600_000,
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("anthropic")
    sources = {entry.source for entry in pool.entries()}

    # Both env OAuth token and autodiscovered Claude Code creds should be there.
    assert "env:ANTHROPIC_TOKEN" in sources
    assert "claude_code" in sources


def test_least_used_strategy_selects_lowest_count(tmp_path, monkeypatch):
    """least_used strategy should select the credential with the lowest request_count."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setattr(
        "agent.credential_pool.get_pool_strategy",
        lambda _provider: "least_used",
    )
    monkeypatch.setattr(
        "agent.credential_pool._seed_from_singletons",
        lambda provider, entries: (False, set()),
    )
    monkeypatch.setattr(
        "agent.credential_pool._seed_from_env",
        lambda provider, entries: (False, set()),
    )
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "openrouter": [
                    {
                        "id": "key-a",
                        "label": "heavy",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "manual",
                        "access_token": "sk-or-heavy",
                        "request_count": 100,
                    },
                    {
                        "id": "key-b",
                        "label": "light",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "manual",
                        "access_token": "sk-or-light",
                        "request_count": 10,
                    },
                    {
                        "id": "key-c",
                        "label": "medium",
                        "auth_type": "api_key",
                        "priority": 2,
                        "source": "manual",
                        "access_token": "sk-or-medium",
                        "request_count": 50,
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("openrouter")
    entry = pool.select()
    assert entry is not None
    assert entry.id == "key-b"
    assert entry.access_token == "sk-or-light"






def test_custom_endpoint_pool_seeds_from_config(tmp_path, monkeypatch):
    """Verify seeding from custom_providers api_key in config.yaml."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1})

    # Write config.yaml with a custom_providers entry
    config_path = tmp_path / "hermes" / "config.yaml"
    import yaml
    config_path.write_text(yaml.dump({
        "custom_providers": [
            {
                "name": "Together.ai",
                "base_url": "https://api.together.ai/v1",
                "api_key": "sk-config-seeded",
            }
        ]
    }))

    from agent.credential_pool import load_pool

    pool = load_pool("custom:together.ai")
    assert pool.has_credentials()
    entries = pool.entries()
    assert len(entries) == 1
    assert entries[0].access_token == "sk-config-seeded"
    assert entries[0].source == "config:Together.ai"


def test_custom_endpoint_pool_seeds_from_model_config(tmp_path, monkeypatch):
    """Verify seeding from model.api_key when model.provider=='custom' and base_url matches."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1})

    import yaml
    config_path = tmp_path / "hermes" / "config.yaml"
    config_path.write_text(yaml.dump({
        "custom_providers": [
            {
                "name": "Together.ai",
                "base_url": "https://api.together.ai/v1",
            }
        ],
        "model": {
            "provider": "custom",
            "base_url": "https://api.together.ai/v1",
            "api_key": "sk-model-key",
        },
    }))

    from agent.credential_pool import load_pool

    pool = load_pool("custom:together.ai")
    assert pool.has_credentials()
    entries = pool.entries()
    # Should have the model_config entry
    model_entries = [e for e in entries if e.source == "model_config"]
    assert len(model_entries) == 1
    assert model_entries[0].access_token == "sk-model-key"








    # "custom:empty" not included because it's empty








def test_load_pool_does_not_seed_claude_code_when_anthropic_not_configured(tmp_path, monkeypatch):
    """Claude Code credentials must not be auto-seeded when the user never selected anthropic."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1, "credential_pool": {}})

    # Claude Code credentials exist on disk
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {"accessToken": "sk-ant...oken", "refreshToken": "rt", "expiresAt": 9999999999999},
    )
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_hermes_oauth_credentials",
        lambda: None,
    )
    # User configured kimi-coding, NOT anthropic
    monkeypatch.setattr(
        "hermes_cli.auth.is_provider_explicitly_configured",
        lambda pid: pid == "kimi-coding",
    )

    from agent.credential_pool import load_pool
    pool = load_pool("anthropic")

    # Should NOT have seeded the claude_code entry
    assert pool.entries() == []


def test_load_pool_seeds_copilot_via_gh_auth_token(tmp_path, monkeypatch):
    """Copilot credentials from `gh auth token` should be seeded into the pool."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1, "credential_pool": {}})

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.resolve_copilot_token",
        lambda: ("gho_fake_token_abc123", "gh auth token"),
    )

    from agent.credential_pool import load_pool
    pool = load_pool("copilot")

    assert pool.has_credentials()
    entries = pool.entries()
    assert len(entries) == 1
    assert entries[0].source == "gh_cli"
    assert entries[0].access_token == "gho_fake_token_abc123"
    assert entries[0].base_url == "https://api.githubcopilot.com"


def test_load_pool_skips_exchange_for_suppressed_copilot(tmp_path, monkeypatch):
    """A suppressed copilot source must NOT run the token exchange.

    Regression test: the suppression gate used to sit AFTER
    ``get_copilot_api_token`` (which retries 3x with backoff, ~13s worst
    case), so every pool load — model picker open, /model, agent startup —
    burned the full exchange dead time for a source the user had already
    removed with ``hermes auth remove copilot gh_cli``.  The gate must run
    BEFORE the network call.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {},
            "suppressed_sources": {"copilot": ["gh_cli"]},
        },
    )

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.resolve_copilot_token",
        lambda: ("gho_fake_token_abc123", "gh auth token"),
    )

    exchange_called = False

    def _boom(token):
        nonlocal exchange_called
        exchange_called = True
        raise AssertionError("exchange must not run for a suppressed source")

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.get_copilot_api_token",
        _boom,
    )

    from agent.credential_pool import load_pool
    pool = load_pool("copilot")

    assert not exchange_called
    assert not pool.has_credentials()
    assert pool.entries() == []


def test_load_pool_respects_env_var_copilot_suppression(tmp_path, monkeypatch):
    """Suppressing env:GH_TOKEN must gate a GH_TOKEN-sourced token.

    Regression test for the source_name classification: a substring match
    (``"gh" in source.lower()``) classified GH_TOKEN/GITHUB_TOKEN as gh_cli,
    so a user's env-var-specific suppression was silently bypassed and the
    exchange ran anyway.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {},
            "suppressed_sources": {"copilot": ["env:GH_TOKEN"]},
        },
    )

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.resolve_copilot_token",
        lambda: ("gho_fake_token_env", "GH_TOKEN"),
    )

    exchange_called = False

    def _boom(token):
        nonlocal exchange_called
        exchange_called = True
        raise AssertionError("exchange must not run for a suppressed env source")

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.get_copilot_api_token",
        _boom,
    )

    from agent.credential_pool import load_pool
    pool = load_pool("copilot")

    assert not exchange_called
    assert pool.entries() == []


def test_load_pool_gh_cli_suppression_does_not_block_env_tokens(tmp_path, monkeypatch):
    """Suppressing gh_cli must NOT swallow an env-var-sourced token.

    The inverse of the substring bug: GH_TOKEN misclassified as gh_cli meant
    suppressing the CLI path also silently dropped env tokens.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {},
            "suppressed_sources": {"copilot": ["gh_cli"]},
        },
    )

    monkeypatch.setattr(
        "hermes_cli.copilot_auth.resolve_copilot_token",
        lambda: ("gho_fake_token_env", "GH_TOKEN"),
    )
    monkeypatch.setattr(
        "hermes_cli.copilot_auth.get_copilot_api_token",
        lambda token: ("capi_exchanged_token", None),
    )

    from agent.credential_pool import load_pool
    pool = load_pool("copilot")

    assert [e.source for e in pool.entries()] == ["env:GH_TOKEN"]


def test_load_pool_skips_resolve_when_all_copilot_sources_suppressed(tmp_path, monkeypatch):
    """With every copilot source suppressed, resolve_copilot_token (which
    shells out to ``gh auth token``) must not run at all."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    from hermes_cli.copilot_auth import COPILOT_ENV_VARS
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {},
            "suppressed_sources": {
                "copilot": ["gh_cli"] + [f"env:{v}" for v in COPILOT_ENV_VARS],
            },
        },
    )

    def _boom():
        raise AssertionError("resolve_copilot_token must not run when all sources are suppressed")

    monkeypatch.setattr("hermes_cli.copilot_auth.resolve_copilot_token", _boom)

    from agent.credential_pool import load_pool
    pool = load_pool("copilot")

    assert pool.entries() == []




def test_load_pool_seeds_qwen_oauth_via_cli_tokens(tmp_path, monkeypatch):
    """Qwen OAuth credentials from ~/.qwen/oauth_creds.json should be seeded into the pool."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1, "credential_pool": {}})

    monkeypatch.setattr(
        "hermes_cli.auth.resolve_qwen_runtime_credentials",
        lambda **kw: {
            "provider": "qwen-oauth",
            "base_url": "https://portal.qwen.ai/v1",
            "api_key": "qwen_fake_token_xyz",
            "source": "qwen-cli",
            "expires_at_ms": 1900000000000,
            "auth_file": str(tmp_path / ".qwen" / "oauth_creds.json"),
        },
    )

    from agent.credential_pool import load_pool
    pool = load_pool("qwen-oauth")

    assert pool.has_credentials()
    entries = pool.entries()
    assert len(entries) == 1
    assert entries[0].source == "qwen-cli"
    assert entries[0].access_token == "qwen_fake_token_xyz"


def test_load_pool_does_not_seed_qwen_oauth_when_no_token(tmp_path, monkeypatch):
    """Qwen OAuth pool should be empty when no CLI credentials exist."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(tmp_path, {"version": 1, "credential_pool": {}})

    from hermes_cli.auth import AuthError

    monkeypatch.setattr(
        "hermes_cli.auth.resolve_qwen_runtime_credentials",
        lambda **kw: (_ for _ in ()).throw(
            AuthError("Qwen CLI credentials not found.", provider="qwen-oauth", code="qwen_auth_missing")
        ),
    )

    from agent.credential_pool import load_pool
    pool = load_pool("qwen-oauth")

    assert not pool.has_credentials()
    assert pool.entries() == []


def test_nous_seed_from_singletons_preserves_obtained_at_timestamps(tmp_path, monkeypatch):
    """Regression test for #15099 secondary issue.

    When ``_seed_from_singletons`` materialises a device_code pool entry from
    the ``providers.nous`` singleton, it must carry the mint/refresh
    timestamps (``obtained_at``, ``agent_key_obtained_at``, ``expires_in``,
    etc.) into the pool entry.  Without them, freshness-sensitive consumers
    (self-heal hooks, pool pruning by age) treat just-minted credentials as
    older than they actually are and evict them.
    """
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "nous": {
                    "access_token": "at_XXXXXXXX",
                    "refresh_token": "rt_YYYYYYYY",
                    "client_id": "hermes-cli",
                    "portal_base_url": "https://portal.nousresearch.com",
                    "inference_base_url": "https://inference.nousresearch.com/v1",
                    "token_type": "Bearer",
                    "scope": "openid profile",
                    "obtained_at": "2026-04-24T10:00:00+00:00",
                    "expires_at": "2026-04-24T11:00:00+00:00",
                    "expires_in": 3600,
                    "agent_key": "sk-nous-AAAA",
                    "agent_key_id": "ak_123",
                    "agent_key_expires_at": "2026-04-25T10:00:00+00:00",
                    "agent_key_expires_in": 86400,
                    "agent_key_reused": False,
                    "agent_key_obtained_at": "2026-04-24T10:00:05+00:00",
                    "tls": {"insecure": False, "ca_bundle": None},
                },
            },
        },
    )

    from agent.credential_pool import load_pool

    pool = load_pool("nous")
    entries = pool.entries()

    device_entries = [e for e in entries if e.source == "device_code"]
    assert len(device_entries) == 1, f"expected single device_code entry; got {len(device_entries)}"
    e = device_entries[0]

    # Direct dataclass fields — must survive the singleton → pool copy.
    assert e.access_token == "at_XXXXXXXX"
    assert e.refresh_token == "rt_YYYYYYYY"
    assert e.expires_at == "2026-04-24T11:00:00+00:00"
    assert e.agent_key == "sk-nous-AAAA"
    assert e.agent_key_expires_at == "2026-04-25T10:00:00+00:00"

    # Extra fields — this is what regressed.  These must be carried through
    # via ``extra`` dict or __getattr__, NOT silently dropped.
    assert e.obtained_at == "2026-04-24T10:00:00+00:00", (
        f"obtained_at was dropped during seed; got {e.obtained_at!r}. This breaks "
        f"downstream pool-freshness consumers (#15099)."
    )
    assert e.agent_key_obtained_at == "2026-04-24T10:00:05+00:00"
    assert e.expires_in == 3600
    assert e.agent_key_id == "ak_123"
    assert e.agent_key_expires_in == 86400
    assert e.agent_key_reused is False


class TestLeastUsedStrategy:
    """Regression: least_used strategy must increment request_count on select."""

    def test_request_count_increments(self):
        """Each select() call should increment the chosen entry's request_count."""
        from unittest.mock import patch as _patch
        from agent.credential_pool import CredentialPool, PooledCredential, STRATEGY_LEAST_USED

        entries = [
            PooledCredential(provider="test", id="a", label="a", auth_type="api_key",
                             source="a", access_token="tok-a", priority=0, request_count=0),
            PooledCredential(provider="test", id="b", label="b", auth_type="api_key",
                             source="b", access_token="tok-b", priority=1, request_count=0),
        ]
        with _patch("agent.credential_pool.get_pool_strategy", return_value=STRATEGY_LEAST_USED):
            pool = CredentialPool("test", entries)

        # First select should pick entry with lowest count (both 0 → first)
        e1 = pool.select()
        assert e1 is not None
        count_after_first = e1.request_count
        assert count_after_first == 1, f"Expected 1 after first select, got {count_after_first}"

        # Second select should pick the OTHER entry (now has lower count)
        e2 = pool.select()
        assert e2 is not None
        assert e2.id != e1.id or e2.request_count == 2, (
            "least_used should alternate or increment"
        )


# ── PR #10160 salvage: Nous OAuth cross-process sync tests ─────────────────





# ── OpenAI Codex OAuth cross-process sync tests ────────────────────────────










# ---------------------------------------------------------------------------
# xAI OAuth terminal error quarantine
# ---------------------------------------------------------------------------


def _xai_auth_store(access_token: str, refresh_token: str) -> dict:
    return {
        "version": 1,
        "active_provider": "xai-oauth",
        "providers": {
            "xai-oauth": {
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "discovery": {"token_endpoint": "https://accounts.x.ai/oauth2/token"},
                "redirect_uri": "http://localhost:12345/callback",
            }
        },
    }










# ---------------------------------------------------------------------------
# Codex OAuth terminal error quarantine
# ---------------------------------------------------------------------------


def _codex_auth_store(access_token: str, refresh_token: str) -> dict:
    return {
        "version": 1,
        "active_provider": "openai-codex",
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }
        },
    }








def test_persist_preserves_concurrent_disk_only_entry(tmp_path, monkeypatch):
    """Regression for #19566: stale rotation writes keep concurrent entries."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    # Block external-credential autodiscovery: a real ~/.claude/.credentials.json
    # on a dev machine would seed an extra claude_code entry and break the
    # exact-id assertions below (passes on CI where no such file exists).
    monkeypatch.setattr("agent.anthropic_adapter.read_hermes_oauth_credentials", lambda: None)
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", lambda: None)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "anthropic": [
                    {
                        "id": "cred-A",
                        "label": "primary",
                        "auth_type": "api_key",
                        "priority": 0,
                        "source": "manual",
                        "access_token": "sk-A",
                    },
                    {
                        "id": "cred-B",
                        "label": "secondary",
                        "auth_type": "api_key",
                        "priority": 1,
                        "source": "manual",
                        "access_token": "sk-B",
                    },
                ]
            },
        },
    )

    from agent.credential_pool import load_pool
    from hermes_cli.auth import read_credential_pool, write_credential_pool

    pool = load_pool("anthropic")
    assert {entry.id for entry in pool.entries()} == {"cred-A", "cred-B"}

    disk_snapshot = read_credential_pool("anthropic")
    disk_snapshot.append(
        {
            "id": "cred-C",
            "label": "added-concurrently",
            "auth_type": "api_key",
            "priority": 2,
            "source": "manual",
            "access_token": "sk-C",
        }
    )
    write_credential_pool("anthropic", disk_snapshot)

    pool.mark_exhausted_and_rotate(status_code=429)

    final = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    final_ids = [entry["id"] for entry in final["credential_pool"]["anthropic"]]
    assert set(final_ids) == {"cred-A", "cred-B", "cred-C"}
    persisted_a = next(
        entry
        for entry in final["credential_pool"]["anthropic"]
        if entry["id"] == "cred-A"
    )
    assert persisted_a["last_status"] == "exhausted"




# ---------------------------------------------------------------------------
# _sync_anthropic_entry_from_credentials_file — parity fix tests
# ---------------------------------------------------------------------------

def _make_anthropic_claude_code_pool(tmp_path, monkeypatch, *, access_token, refresh_token, expires_at_ms=9_999_999_999_000):
    """Helper: load an Anthropic pool seeded with a single claude_code entry."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_TOKEN", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    _write_auth_store(tmp_path, {"version": 1, "credential_pool": {}})
    monkeypatch.setattr("hermes_cli.auth.is_provider_explicitly_configured", lambda pid: pid == "anthropic")
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_hermes_oauth_credentials",
        lambda: None,
    )
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {"accessToken": access_token, "refreshToken": refresh_token, "expiresAt": expires_at_ms},
    )
    from agent.credential_pool import load_pool
    pool = load_pool("anthropic")
    entry = pool.select()
    assert entry is not None
    assert entry.source == "claude_code"
    return pool, entry






def test_sync_anthropic_entry_tokens_unchanged_no_op(tmp_path, monkeypatch):
    """Sync must be a no-op when credentials file matches the pool entry."""
    pool, entry = _make_anthropic_claude_code_pool(
        tmp_path, monkeypatch,
        access_token="same-access",
        refresh_token="same-refresh",
    )

    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {"accessToken": "same-access", "refreshToken": "same-refresh", "expiresAt": 9_999_999_999_000},
    )

    synced = pool._sync_anthropic_entry_from_credentials_file(entry)

    assert synced is entry, "no-op sync must return the original entry object"


def test_sync_anthropic_entry_clears_all_error_fields(tmp_path, monkeypatch):
    """Syncing fresh tokens must clear all six error/status fields on the entry.

    Before the fix, last_error_reason / last_error_message / last_error_reset_at
    were left set, so a previously-exhausted entry could stay stuck even after
    fresh tokens arrived from the credentials file.
    """
    from dataclasses import replace as dc_replace
    from agent.credential_pool import STATUS_EXHAUSTED

    pool, entry = _make_anthropic_claude_code_pool(
        tmp_path, monkeypatch,
        access_token="stale-access",
        refresh_token="stale-refresh",
    )

    now = time.time()
    exhausted = dc_replace(
        entry,
        last_status=STATUS_EXHAUSTED,
        last_status_at=now,
        last_error_code=401,
        last_error_reason="token_expired",
        last_error_message="Access token has expired",
        last_error_reset_at=now + 300,
    )
    pool._replace_entry(entry, exhausted)

    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {"accessToken": "fresh-access", "refreshToken": "fresh-refresh", "expiresAt": 9_999_999_999_000},
    )

    synced = pool._sync_anthropic_entry_from_credentials_file(exhausted)

    assert synced is not exhausted
    assert synced.access_token == "fresh-access"
    assert synced.last_status is None
    assert synced.last_status_at is None
    assert synced.last_error_code is None
    assert synced.last_error_reason is None
    assert synced.last_error_message is None
    assert synced.last_error_reset_at is None


def _load_two_ok_pool(tmp_path, monkeypatch):
    """A pool with two OK anthropic entries, current = cred-1."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "credential_pool": {
                "anthropic": [
                    {
                        "id": "cred-1", "label": "primary", "auth_type": "api_key",
                        "priority": 0, "source": "manual", "access_token": "***",
                        "last_status": "ok", "last_status_at": None, "last_error_code": None,
                    },
                    {
                        "id": "cred-2", "label": "secondary", "auth_type": "api_key",
                        "priority": 1, "source": "manual", "access_token": "***",
                        "last_status": "ok", "last_status_at": None, "last_error_code": None,
                    },
                ]
            },
        },
    )
    from agent.credential_pool import load_pool

    return load_pool("anthropic")


def _fresh_entry(pool):
    """A copy of the pool's first entry under a new id, for add_entry()."""
    from dataclasses import replace as dc_replace

    return dc_replace(pool.entries()[0], id="cred-new")


class TestCredentialPoolQueryLocking:
    """Public pool-state methods must run under ``self._lock``.

    ``has_available``/``peek``/``current``/``entries`` all touch
    ``self._entries`` (and ``_available_entries`` even prunes + persists),
    and the management surface (``has_credentials``/``reset_statuses``/
    ``remove_index``/``resolve_target``/``add_entry``) reads or rebinds
    ``self._entries`` and persists auth.json, so they must all hold the
    same lock every mutating entry point uses.  A naive fix would deadlock
    because the lock is non-reentrant and ``peek`` calls ``current`` +
    ``_available_entries``; these tests guard both the no-deadlock and the
    actually-locked properties.
    """

    def test_query_methods_do_not_deadlock(self, tmp_path, monkeypatch):
        pool = _load_two_ok_pool(tmp_path, monkeypatch)
        pool.select()  # set a current entry

        # peek() internally calls current() + _available_entries(); if any of
        # these re-acquired the non-reentrant lock we'd hang here forever.
        assert pool.current() is not None
        assert pool.peek() is not None
        assert pool.has_available() is True
        assert pool.has_credentials() is True
        assert pool.resolve_target("cred-1")[1] is not None
        # (env may seed extra singleton entries; just assert ours are present)
        assert {"cred-1", "cred-2"} <= {e.id for e in pool.entries()}
        # try_refresh_matching's no-hint branch resolves the current entry
        # while already holding the lock — must use _current_unlocked(), not
        # current(), or it deadlocks on the non-reentrant lock (found when
        # rebasing this fix over the #69843 salvage which added the method).
        pool.try_refresh_matching()

    @pytest.mark.parametrize(
        "method,get_args",
        [
            ("has_available", lambda pool: ()),
            ("peek", lambda pool: ()),
            ("current", lambda pool: ()),
            ("entries", lambda pool: ()),
            ("has_credentials", lambda pool: ()),
            ("reset_statuses", lambda pool: ()),
            ("resolve_target", lambda pool: ("cred-1",)),
            ("remove_index", lambda pool: (1,)),
            ("add_entry", lambda pool: (_fresh_entry(pool),)),
        ],
    )
    def test_query_method_acquires_lock(self, tmp_path, monkeypatch, method, get_args):
        import threading

        pool = _load_two_ok_pool(tmp_path, monkeypatch)
        pool.select()
        args = get_args(pool)

        inner = pool._lock

        class _InstrumentedLock:
            """Probe that records acquire attempts, so the test can prove the
            worker actually reached ``self._lock`` before asserting that it
            blocks (a plain timed wait passes spuriously if the worker is
            simply never scheduled)."""

            def __init__(self):
                self.attempted = threading.Event()

            def acquire(self, *args, **kwargs):
                self.attempted.set()
                return inner.acquire(*args, **kwargs)

            def release(self):
                inner.release()

            def __enter__(self):
                self.acquire()
                return self

            def __exit__(self, *exc):
                self.release()

        probe = _InstrumentedLock()
        pool._lock = probe

        done = threading.Event()

        def _call():
            getattr(pool, method)(*args)
            done.set()

        # Hold the real lock (without tripping the probe), then fire the query
        # on another thread. If the method acquires self._lock (as it must),
        # it blocks until we release.
        inner.acquire()
        try:
            worker = threading.Thread(target=_call, daemon=True)
            worker.start()
            assert probe.attempted.wait(timeout=2.0), (
                f"{method}() never attempted to acquire self._lock"
            )
            assert not done.wait(timeout=0.5), (
                f"{method}() returned while the pool lock was held — it is not "
                f"blocking on self._lock"
            )
        finally:
            inner.release()

        assert done.wait(timeout=2.0), f"{method}() did not complete after lock release"


def _d3_codex_entry(
    entry_id: str,
    label: str,
    priority: int,
    *,
    status: str | None = None,
    access_token: str | None = None,
) -> dict:
    entry = {
        "id": entry_id,
        "label": label,
        "auth_type": "oauth",
        "priority": priority,
        "source": "manual:device_code",
        "access_token": access_token if access_token is not None else f"token-{entry_id}",
        "refresh_token": f"refresh-{entry_id}",
        "base_url": "https://chatgpt.com/backend-api/codex",
    }
    if status:
        entry.update(
            {
                "last_status": status,
                "last_status_at": time.time(),
                "last_error_code": 429,
                "last_error_reset_at": time.time() + 3600,
            }
        )
    return entry


def _load_d3_codex_pool(tmp_path, monkeypatch, entries: list[dict], pin: str = ""):
    hermes_home = tmp_path / "hermes"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    _write_auth_store(
        tmp_path,
        {"version": 1, "credential_pool": {"openai-codex": entries}},
    )
    if pin:
        (hermes_home / ".env").write_text(pin)
    from agent.credential_pool import load_pool

    return load_pool("openai-codex")


def test_d3_credential_pin_controls_select_peek_and_lease(tmp_path, monkeypatch):
    entries = [
        _d3_codex_entry("first", "FIRST", 0),
        _d3_codex_entry("pinned", "PINNED", 1),
    ]
    pin = "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=PINNED\n"

    selected = _load_d3_codex_pool(tmp_path, monkeypatch, entries, pin).select()
    peeked = _load_d3_codex_pool(tmp_path, monkeypatch, entries, pin).peek()
    leased = _load_d3_codex_pool(tmp_path, monkeypatch, entries, pin).acquire_lease()

    assert selected is not None and selected.id == "pinned"
    assert peeked is not None and peeked.id == "pinned"
    assert leased == "pinned"


def test_d3_credential_id_pin_wins_and_rejects_sibling_lease(tmp_path, monkeypatch):
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [
            _d3_codex_entry("first", "FIRST", 0),
            _d3_codex_entry("pinned", "PINNED", 1),
        ],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned\n"
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=FIRST\n",
    )

    selected = pool.select()
    assert selected is not None and selected.id == "pinned"
    assert pool.acquire_lease("first") is None


@pytest.mark.parametrize(
    "entries",
    [
        [
            _d3_codex_entry("duplicate-a", "PINNED", 0),
            _d3_codex_entry("duplicate-b", "PINNED", 1),
        ],
        [_d3_codex_entry("first", "FIRST", 0)],
        [
            _d3_codex_entry("pinned", "PINNED", 0, status="exhausted"),
            _d3_codex_entry("first", "FIRST", 1),
        ],
        [
            _d3_codex_entry("pinned", "PINNED", 0, access_token=""),
            _d3_codex_entry("first", "FIRST", 1),
        ],
    ],
)
def test_d3_credential_invalid_pin_fails_closed(tmp_path, monkeypatch, entries):
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        entries,
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=PINNED\n",
    )

    assert pool.has_available() is False
    if any(entry.get("last_status") == "exhausted" for entry in entries):
        assert pool.next_available_at() is not None
    assert pool.select() is None
    assert pool.peek() is None
    assert pool.acquire_lease() is None


def test_d3_credential_pin_ignores_ambient_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL", "PINNED")
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [
            _d3_codex_entry("first", "FIRST", 0),
            _d3_codex_entry("pinned", "PINNED", 1),
        ],
    )

    selected = pool.select()
    assert selected is not None and selected.id == "first"


def test_d3_credential_current_rechecks_profile_pin(tmp_path, monkeypatch):
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [
            _d3_codex_entry("first", "FIRST", 0),
            _d3_codex_entry("pinned", "PINNED", 1),
        ],
    )
    selected = pool.select()
    assert selected is not None and selected.id == "first"

    hermes_home = tmp_path / "hermes"
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=PINNED\n"
    )
    from hermes_cli.config import invalidate_env_cache

    invalidate_env_cache()
    current = pool.current()
    assert current is not None and current.id == "pinned"


def test_d3_credential_pin_source_error_fails_closed(tmp_path, monkeypatch):
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [_d3_codex_entry("first", "FIRST", 0)],
    )
    monkeypatch.setattr(
        "agent.credential_pool.load_env",
        lambda: (_ for _ in ()).throw(PermissionError("profile .env unreadable")),
    )

    with pytest.raises(PermissionError, match="unreadable"):
        pool.select()


def test_d3_credential_pin_does_not_refresh_sibling(tmp_path, monkeypatch):
    pinned = _d3_codex_entry("pinned", "PINNED", 0)
    sibling = _d3_codex_entry("sibling", "SIBLING", 1)
    pinned["access_token"] = _jwt_with_claims({"exp": int(time.time() + 3600)})
    sibling["access_token"] = _jwt_with_claims({"exp": int(time.time() + 1)})
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [pinned, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=PINNED\n",
    )
    refreshed = []
    monkeypatch.setattr(
        pool,
        "_refresh_entry",
        lambda entry, *, force=False: refreshed.append(entry.id) or entry,
    )

    selected = pool.select()

    assert selected is not None and selected.id == "pinned"
    assert refreshed == []


def test_d3_credential_canonical_pin_fails_closed_on_duplicate_canonical_rows(
    tmp_path, monkeypatch
):
    sibling = _d3_codex_entry("canonical-sibling", "SIBLING", 0)
    pinned = _d3_codex_entry("canonical-pinned", "PINNED", 1)
    sibling["source"] = "device_code"
    pinned["source"] = "device_code"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [sibling, pinned],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=canonical-pinned\n",
    )

    assert pool.has_available() is False
    assert pool.select() is None
    assert pool.peek() is None
    assert pool.acquire_lease() is None


def test_d3_credential_recovery_apis_do_not_touch_stale_sibling(tmp_path, monkeypatch):
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [
            _d3_codex_entry("first", "FIRST", 0),
            _d3_codex_entry("pinned", "PINNED", 1),
        ],
    )
    selected = pool.select()
    assert selected is not None and selected.id == "first"

    hermes_home = tmp_path / "hermes"
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned\n"
    )
    from hermes_cli.config import invalidate_env_cache

    invalidate_env_cache()
    refreshed = []
    monkeypatch.setattr(
        pool,
        "_refresh_entry",
        lambda entry, *, force=False: refreshed.append(entry.id) or entry,
    )

    assert pool.entry_id_for_api_key(selected.runtime_api_key) is None
    current = pool.try_refresh_current()
    assert current is not None and current.id == "pinned"
    assert refreshed == ["pinned"]

    refreshed.clear()
    assert pool.try_refresh_matching(credential_id="first") is None
    assert refreshed == []

    rotated = pool.mark_exhausted_and_rotate(
        status_code=429,
        credential_id="first",
    )
    assert rotated is not None and rotated.id == "pinned"
    first = next(entry for entry in pool.entries() if entry.id == "first")
    assert first.last_status is None


def test_d3_credential_manual_pin_does_not_adopt_singleton_account(
    tmp_path, monkeypatch
):
    manual = _d3_codex_entry("manual-pinned", "PINNED", 0)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [manual],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=manual-pinned\n",
    )
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": "singleton-account-token",
                        "refresh_token": "singleton-account-refresh",
                    }
                }
            },
            "credential_pool": {"openai-codex": [manual]},
        },
    )

    selected = pool.select()
    assert selected is not None and selected.id == "manual-pinned"
    refresh_inputs = []
    monkeypatch.setattr(
        "hermes_cli.auth.refresh_codex_oauth_pure",
        lambda access_token, refresh_token: refresh_inputs.append(
            (access_token, refresh_token)
        )
        or {
            "access_token": "manual-refreshed-token",
            "refresh_token": "manual-refreshed-refresh",
        },
    )

    refreshed = pool.try_refresh_current()

    assert refreshed is not None and refreshed.id == "manual-pinned"
    assert refresh_inputs == [
        (manual["access_token"], manual["refresh_token"])
    ]


def test_d3_credential_load_pool_does_not_seed_unpinned_singleton_sibling(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=manual-pinned\n"
    )
    manual = _d3_codex_entry("manual-pinned", "PINNED", 0)
    canonical = _d3_codex_entry("canonical-sibling", "SIBLING", 1)
    canonical["source"] = "device_code"
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": "singleton-new-token",
                        "refresh_token": "singleton-new-refresh",
                    }
                }
            },
            "credential_pool": {"openai-codex": [manual, canonical]},
        },
    )
    from agent.credential_pool import load_pool

    selected = load_pool("openai-codex").select()

    assert selected is not None and selected.id == "manual-pinned"
    payload = json.loads((hermes_home / "auth.json").read_text())
    persisted = next(
        entry
        for entry in payload["credential_pool"]["openai-codex"]
        if entry["id"] == "canonical-sibling"
    )
    assert persisted["access_token"] == canonical["access_token"]
    assert persisted["refresh_token"] == canonical["refresh_token"]


def test_d3_credential_recovery_does_not_return_unavailable_pin_for_sibling_failure(
    tmp_path, monkeypatch
):
    pinned = _d3_codex_entry("pinned-id", "PINNED", 0, status="exhausted")
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [pinned, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    recovered = pool.mark_exhausted_and_rotate(
        status_code=429,
        credential_id="sibling-id",
        api_key_hint=sibling["access_token"],
    )

    assert pool.has_available() is False
    assert recovered is None


def test_d3_credential_pinned_refresh_preserves_concurrent_sibling_tokens(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    assert pool.select() is not None

    from hermes_cli.auth import write_credential_pool

    concurrent_rows = [entry.to_dict() for entry in pool.entries()]
    concurrent_sibling = next(
        entry for entry in concurrent_rows if entry["id"] == "sibling-id"
    )
    concurrent_sibling["access_token"] = "sibling-concurrent-access"
    concurrent_sibling["refresh_token"] = "sibling-concurrent-refresh"
    write_credential_pool("openai-codex", concurrent_rows)

    monkeypatch.setattr(
        "agent.credential_pool.auth_mod.refresh_codex_oauth_pure",
        lambda *_args, **_kwargs: {
            "access_token": "target-refreshed-access",
            "refresh_token": "target-refreshed-refresh",
        },
    )
    assert pool.try_refresh_current() is not None

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted_sibling = next(
        entry
        for entry in payload["credential_pool"]["openai-codex"]
        if entry["id"] == "sibling-id"
    )
    assert persisted_sibling["access_token"] == "sibling-concurrent-access"
    assert persisted_sibling["refresh_token"] == "sibling-concurrent-refresh"


def test_d3_credential_pinned_add_persists_new_entry_and_preserves_sibling(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from agent.credential_pool import PooledCredential
    from hermes_cli.auth import write_credential_pool

    concurrent_rows = [entry.to_dict() for entry in pool.entries()]
    concurrent_sibling = next(
        entry for entry in concurrent_rows if entry["id"] == "sibling-id"
    )
    concurrent_sibling["access_token"] = "sibling-concurrent-access"
    concurrent_sibling["refresh_token"] = "sibling-concurrent-refresh"
    write_credential_pool("openai-codex", concurrent_rows)

    added = pool.add_entry(
        PooledCredential.from_dict(
            "openai-codex",
            {
                "id": "new-id",
                "label": "NEW",
                "auth_type": "oauth",
                "source": "manual:device_code",
                "access_token": "new-access",
                "refresh_token": "new-refresh",
            },
        )
    )
    assert added.id == "new-id"

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert {entry["id"] for entry in entries} == {"pinned-id", "sibling-id", "new-id"}
    persisted_sibling = next(entry for entry in entries if entry["id"] == "sibling-id")
    assert persisted_sibling["access_token"] == "sibling-concurrent-access"
    assert persisted_sibling["refresh_token"] == "sibling-concurrent-refresh"


def test_d3_credential_pinned_add_uses_latest_disk_priority(tmp_path, monkeypatch):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from agent.credential_pool import PooledCredential
    from hermes_cli.auth import write_credential_pool

    concurrent = _d3_codex_entry("concurrent-id", "CONCURRENT", 2)
    write_credential_pool("openai-codex", [target, sibling, concurrent])

    added = pool.add_entry(
        PooledCredential.from_dict(
            "openai-codex",
            {
                "id": "new-id",
                "label": "NEW",
                "auth_type": "oauth",
                "source": "manual:device_code",
                "access_token": "new-access",
                "refresh_token": "new-refresh",
            },
        )
    )

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert [entry["priority"] for entry in entries] == [0, 1, 2, 3]
    assert added.priority == 3


def test_d3_credential_pinned_reset_statuses_persists_all_rows(tmp_path, monkeypatch):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    for entry in (target, sibling):
        entry["last_status"] = "rate_limited"
        entry["last_status_at"] = 123.0
        entry["last_error_code"] = "rate_limit_exceeded"
        entry["last_error_reason"] = "rate_limit_exceeded"
        entry["last_error_message"] = "limited"
        entry["last_error_reset_at"] = 456.0
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    assert pool.reset_statuses() == 2

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert {entry["id"] for entry in entries} == {"pinned-id", "sibling-id"}
    for entry in entries:
        assert not any(
            entry.get(key)
            for key in (
                "last_status",
                "last_status_at",
                "last_error_code",
                "last_error_reason",
                "last_error_message",
                "last_error_reset_at",
            )
        )


def test_d3_credential_pinned_reset_failure_keeps_memory_unchanged(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="exhausted")
    target["last_error_code"] = "429"
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1, status="dead")
    sibling["last_error_reason"] = "invalid_grant"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import AuthError

    def fail_reset():
        raise AuthError("write failed", code="codex_pool_write_failed")

    monkeypatch.setattr(
        "agent.credential_pool.auth_mod._reset_codex_pool_statuses_atomic",
        fail_reset,
    )

    with pytest.raises(AuthError) as excinfo:
        pool.reset_statuses()

    assert excinfo.value.code == "codex_pool_write_failed"
    entries = pool.entries()
    assert [entry.last_status for entry in entries] == ["exhausted", "dead"]
    assert entries[0].last_error_code == "429"
    assert entries[1].last_error_reason == "invalid_grant"


def test_d3_credential_pinned_reset_reads_latest_disk_statuses(tmp_path, monkeypatch):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    exhausted_sibling = _d3_codex_entry("exhausted-id", "EXHAUSTED", 1)
    exhausted_sibling["last_status"] = "exhausted"
    exhausted_sibling["last_error_code"] = "429"
    reason_only_sibling = _d3_codex_entry("reason-id", "REASON", 2)
    reason_only_sibling["last_error_reason"] = "invalid_grant"
    reason_only_sibling["last_error_message"] = "refresh failed"
    reason_only_sibling["last_error_reset_at"] = 789.0
    write_credential_pool(
        "openai-codex",
        [target, exhausted_sibling, reason_only_sibling],
    )

    assert pool.reset_statuses() == 2

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert {entry["id"] for entry in entries} == {
        "pinned-id",
        "exhausted-id",
        "reason-id",
    }
    for entry in entries:
        assert not any(
            entry.get(key)
            for key in (
                "last_status",
                "last_status_at",
                "last_error_code",
                "last_error_reason",
                "last_error_message",
                "last_error_reset_at",
            )
        )


def test_d3_credential_pinned_reset_reconciles_latest_disk_before_followup_write(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="exhausted")
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    latest_target = dict(target)
    latest_target["access_token"] = "latest-target-access"
    latest_target["refresh_token"] = "latest-target-refresh"
    latest_sibling = _d3_codex_entry("latest-id", "LATEST", 1)
    write_credential_pool("openai-codex", [latest_target, latest_sibling])

    assert pool.reset_statuses() == 1
    assert [entry.id for entry in pool.entries()] == ["pinned-id", "latest-id"]
    assert pool.entries()[0].access_token == "latest-target-access"
    assert pool.entries()[0].refresh_token == "latest-target-refresh"

    pool._mark_exhausted(pool.entries()[0], 429)
    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted_target = next(
        entry
        for entry in payload["credential_pool"]["openai-codex"]
        if entry["id"] == "pinned-id"
    )
    assert persisted_target["access_token"] == "latest-target-access"
    assert persisted_target["refresh_token"] == "latest-target-refresh"


def test_d3_credential_pinned_status_write_merges_latest_disk_tokens(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    latest_target = dict(target)
    latest_target["access_token"] = "latest-status-access"
    latest_target["refresh_token"] = "latest-status-refresh"
    write_credential_pool("openai-codex", [latest_target])

    updated = pool._mark_exhausted(pool.entries()[0], 429)

    assert updated.last_status == "exhausted"
    assert updated.access_token == "latest-status-access"
    assert updated.refresh_token == "latest-status-refresh"
    assert pool.entries()[0] == updated
    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted = payload["credential_pool"]["openai-codex"][0]
    assert persisted["access_token"] == "latest-status-access"
    assert persisted["refresh_token"] == "latest-status-refresh"
    assert persisted["last_status"] == "exhausted"


def test_d3_credential_pinned_codex_sync_failure_keeps_memory_and_disk_atomic(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": target["access_token"],
                        "refresh_token": target["refresh_token"],
                    }
                }
            },
            "credential_pool": {"openai-codex": [target]},
        },
    )
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n"
    )
    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    before_memory = pool.entries()
    auth_path = hermes_home / "auth.json"
    payload = json.loads(auth_path.read_text())
    payload["providers"]["openai-codex"]["tokens"] = {
        "access_token": "canonical-new-access",
        "refresh_token": "canonical-new-refresh",
    }
    auth_path.write_text(json.dumps(payload))
    before_disk = auth_path.read_text()

    from hermes_cli.auth import AuthError
    import agent.credential_pool as credential_pool_module

    def reject_atomic_sync(_credential_id):
        raise AuthError(
            "synthetic exact save failure",
            provider="openai-codex",
            code="codex_target_credential_changed",
            relogin_required=False,
        )

    monkeypatch.setattr(
        credential_pool_module.auth_mod,
        "_sync_codex_pool_credential_from_provider_exact",
        reject_atomic_sync,
    )

    for _attempt in range(2):
        returned = pool._sync_codex_entry_from_auth_store(pool.entries()[0])
        assert returned == before_memory[0]
        assert pool.entries() == before_memory
        assert auth_path.read_text() == before_disk


def test_d3_credential_pinned_codex_sync_reconciles_authoritative_siblings(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": target["access_token"],
                        "refresh_token": target["refresh_token"],
                    }
                }
            },
            "credential_pool": {"openai-codex": [target, sibling]},
        },
    )
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n"
    )
    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    auth_path = hermes_home / "auth.json"
    payload = json.loads(auth_path.read_text())
    payload["providers"]["openai-codex"]["tokens"] = {
        "access_token": "canonical-new-access",
        "refresh_token": "canonical-new-refresh",
    }
    persisted_sibling = next(
        row
        for row in payload["credential_pool"]["openai-codex"]
        if row["id"] == "sibling-id"
    )
    persisted_sibling["access_token"] = "sibling-concurrent-access"
    persisted_sibling["refresh_token"] = "sibling-concurrent-refresh"
    persisted_sibling["last_status"] = "exhausted"
    auth_path.write_text(json.dumps(payload))

    synced = pool._sync_codex_entry_from_auth_store(pool.entries()[0])

    assert synced.access_token == "canonical-new-access"
    assert synced.refresh_token == "canonical-new-refresh"
    live_rows = {entry.id: entry for entry in pool.entries()}
    assert live_rows["sibling-id"].access_token == "sibling-concurrent-access"
    assert live_rows["sibling-id"].refresh_token == "sibling-concurrent-refresh"
    assert live_rows["sibling-id"].last_status == "exhausted"
    disk_rows = {
        row["id"]: row
        for row in json.loads(auth_path.read_text())["credential_pool"]["openai-codex"]
    }
    assert list(live_rows) == list(disk_rows)
    for entry_id, live in live_rows.items():
        assert live.access_token == disk_rows[entry_id].get("access_token")
        assert live.refresh_token == disk_rows[entry_id].get("refresh_token")
        assert live.last_status == disk_rows[entry_id].get("last_status")


def test_d3_credential_pinned_codex_sync_uses_single_auth_store_transaction(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": "canonical-latest-access",
                        "refresh_token": "canonical-latest-refresh",
                    }
                }
            },
            "credential_pool": {"openai-codex": [target]},
        },
    )
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n"
    )
    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    before = pool.entries()[0]

    def reject_split_lock_commit(_payload):
        raise AssertionError("canonical sync must not use split-lock exact replacement")

    monkeypatch.setattr(
        "agent.credential_pool.auth_mod._replace_codex_pool_credential_exact",
        reject_split_lock_commit,
    )

    synced = pool._sync_codex_entry_from_auth_store(before)

    assert synced.access_token == "canonical-latest-access"
    assert synced.refresh_token == "canonical-latest-refresh"
    assert pool.entries()[0] == synced


def test_d3_credential_pinned_codex_refresh_rejects_ambiguous_identity_atomically(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": target["access_token"],
                        "refresh_token": target["refresh_token"],
                    }
                }
            },
            "credential_pool": {"openai-codex": [target, sibling]},
        },
    )
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n"
    )
    from agent.credential_pool import load_pool
    from hermes_cli.auth import AuthError
    import agent.credential_pool as credential_pool_module

    pool = load_pool("openai-codex")
    pool._current_id = "pinned-id"
    before_memory = pool.entries()
    auth_path = hermes_home / "auth.json"
    payload = json.loads(auth_path.read_text())
    payload["credential_pool"]["openai-codex"].append(dict(target))
    auth_path.write_text(json.dumps(payload))
    before_disk = auth_path.read_text()

    def must_not_refresh(*_args, **_kwargs):
        raise AssertionError("refresh must not start after identity rejection")

    monkeypatch.setattr(
        credential_pool_module.auth_mod,
        "refresh_codex_oauth_pure",
        must_not_refresh,
    )
    with pytest.raises(AuthError) as excinfo:
        pool._refresh_entry_impl(pool.entries()[0], force=True)

    assert excinfo.value.code == "codex_target_credential_changed"
    assert pool.entries() == before_memory
    assert pool._current_id == "pinned-id"
    assert auth_path.read_text() == before_disk


def test_d3_credential_pinned_codex_sync_clears_failure_reason(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setattr("hermes_cli.auth._import_codex_cli_tokens", lambda: None)
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target.update(
        {
            "source": "device_code",
            "last_status": "exhausted",
            "last_error_code": 429,
            "failure_reason": "billing",
        }
    )
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": "canonical-access-current",
                        "refresh_token": "canonical-refresh-current",
                    }
                }
            },
            "credential_pool": {"openai-codex": [target]},
        },
    )
    (hermes_home / ".env").write_text(
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n"
    )
    from agent.credential_pool import load_pool

    pool = load_pool("openai-codex")
    synced = pool._sync_codex_entry_from_auth_store(pool.entries()[0])
    persisted = json.loads((hermes_home / "auth.json").read_text())[
        "credential_pool"
    ]["openai-codex"][0]

    assert synced.last_status is None
    assert "failure_reason" not in persisted


def test_d3_codex_sync_rejects_ineligible_canonical_target(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target.update({"source": "manual:device_code", "auth_type": "api_key"})
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": "canonical-new-access",
                        "refresh_token": "canonical-new-refresh",
                    }
                }
            },
            "credential_pool": {"openai-codex": [target]},
        },
    )
    from hermes_cli.auth import (
        AuthError,
        _sync_codex_pool_credential_from_provider_exact,
    )

    auth_path = hermes_home / "auth.json"
    before = auth_path.read_text()
    with pytest.raises(AuthError) as excinfo:
        _sync_codex_pool_credential_from_provider_exact("pinned-id")
    assert excinfo.value.code == "codex_target_credential_changed"
    assert auth_path.read_text() == before


def test_d3_codex_quarantine_rejects_distinct_canonical_sibling(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    sibling = _d3_codex_entry("canonical-sibling", "SIBLING", 1)
    sibling["source"] = "device_code"
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {
                        "access_token": target["access_token"],
                        "refresh_token": target["refresh_token"],
                    }
                }
            },
            "credential_pool": {"openai-codex": [target, sibling]},
        },
    )
    from hermes_cli.auth import AuthError, _quarantine_codex_pool_credential_exact

    auth_path = hermes_home / "auth.json"
    before = auth_path.read_text()
    with pytest.raises(AuthError) as excinfo:
        _quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {},
        )
    assert excinfo.value.code == "codex_target_credential_changed"
    assert auth_path.read_text() == before


def test_d3_codex_quarantine_preserves_access_only_provider_rotation(
    tmp_path, monkeypatch
):
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    old_access = target["access_token"]
    old_refresh = target["refresh_token"]
    _write_auth_store(
        tmp_path,
        {
            "version": 1,
            "providers": {
                "openai-codex": {
                    "tokens": {"access_token": "canonical-new-access"}
                }
            },
            "credential_pool": {"openai-codex": [target]},
        },
    )
    from hermes_cli.auth import (
        _quarantine_codex_pool_credential_exact,
        _sync_codex_pool_credential_from_provider_exact,
    )

    synced = _sync_codex_pool_credential_from_provider_exact("pinned-id")
    assert synced[0]["access_token"] == "canonical-new-access"
    rows, quarantined = _quarantine_codex_pool_credential_exact(
        "pinned-id", old_access, old_refresh, {}
    )
    persisted = json.loads((hermes_home / "auth.json").read_text())
    assert quarantined is False
    assert rows[0]["id"] == "pinned-id"
    assert persisted["providers"]["openai-codex"]["tokens"][
        "access_token"
    ] == "canonical-new-access"


def test_d3_codex_quarantine_updates_global_fallback_source(tmp_path, monkeypatch):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_path.write_text(
        json.dumps(
            {
                "version": 1,
                "providers": {},
                "credential_pool": {"openai-codex": [target]},
            }
        )
    )
    global_path.write_text(
        json.dumps(
            {
                "version": 1,
                "providers": {
                    "openai-codex": {
                        "tokens": {
                            "access_token": target["access_token"],
                            "refresh_token": target["refresh_token"],
                        }
                    }
                },
            }
        )
    )
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)

    rows, quarantined = auth_module._quarantine_codex_pool_credential_exact(
        "pinned-id",
        target["access_token"],
        target["refresh_token"],
        {"reason": "synthetic-terminal"},
    )

    profile = json.loads(profile_path.read_text())
    root = json.loads(global_path.read_text())
    assert quarantined is True
    assert rows == []
    assert profile["credential_pool"]["openai-codex"] == []
    assert "access_token" not in root["providers"]["openai-codex"]["tokens"]
    assert "refresh_token" not in root["providers"]["openai-codex"]["tokens"]


def test_d3_codex_quarantine_global_source_failure_restores_profile_pool(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_payload = {
        "version": 1,
        "providers": {},
        "credential_pool": {"openai-codex": [target]},
    }
    global_payload = {
        "version": 1,
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": target["access_token"],
                    "refresh_token": target["refresh_token"],
                }
            }
        },
    }
    profile_path.write_text(json.dumps(profile_payload))
    global_path.write_text(json.dumps(global_payload))
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)

    def reject_source_save(*_args, **_kwargs):
        raise OSError("source save failed")

    monkeypatch.setattr(
        auth_module,
        "_save_provider_state_to_source",
        reject_source_save,
    )

    with pytest.raises(OSError, match="source save failed"):
        auth_module._quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {"reason": "synthetic-terminal"},
        )

    assert json.loads(profile_path.read_text()) == profile_payload
    assert json.loads(global_path.read_text()) == global_payload


def test_d3_codex_quarantine_post_commit_source_failure_restores_both_stores(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_payload = {
        "version": 1,
        "providers": {},
        "credential_pool": {"openai-codex": [target]},
    }
    global_payload = {
        "version": 1,
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": target["access_token"],
                    "refresh_token": target["refresh_token"],
                }
            }
        },
    }
    profile_path.write_text(json.dumps(profile_payload))
    global_path.write_text(json.dumps(global_payload))
    profile_before = profile_path.read_bytes()
    global_before = global_path.read_bytes()
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    real_source_save = auth_module._save_provider_state_to_source

    def commit_then_raise(*args, **kwargs):
        real_source_save(*args, **kwargs)
        raise OSError("post-commit source save failed")

    monkeypatch.setattr(
        auth_module,
        "_save_provider_state_to_source",
        commit_then_raise,
    )

    with pytest.raises(OSError, match="post-commit source save failed"):
        auth_module._quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {"reason": "synthetic-terminal"},
        )

    assert profile_path.read_bytes() == profile_before
    assert global_path.read_bytes() == global_before


def test_d3_codex_quarantine_post_commit_active_failure_restores_both_stores(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_payload = {
        "version": 1,
        "providers": {},
        "credential_pool": {"openai-codex": [target]},
    }
    global_payload = {
        "version": 1,
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": target["access_token"],
                    "refresh_token": target["refresh_token"],
                }
            }
        },
    }
    profile_path.write_text(json.dumps(profile_payload))
    global_path.write_text(json.dumps(global_payload))
    profile_before = profile_path.read_bytes()
    global_before = global_path.read_bytes()
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    real_active_save = auth_module._save_auth_store

    def commit_then_raise(store, target_path=None):
        result = real_active_save(store, target_path=target_path)
        if target_path is None:
            raise OSError("post-commit active save failed")
        return result

    monkeypatch.setattr(auth_module, "_save_auth_store", commit_then_raise)

    with pytest.raises(OSError, match="post-commit active save failed"):
        auth_module._quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {"reason": "synthetic-terminal"},
        )

    assert profile_path.read_bytes() == profile_before
    assert global_path.read_bytes() == global_before


@pytest.mark.parametrize("rollback_target", ["source", "active"])
def test_d3_codex_quarantine_rollback_failure_preserves_operation_error(
    tmp_path, monkeypatch, caplog, rollback_target
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_payload = {
        "version": 1,
        "providers": {},
        "credential_pool": {"openai-codex": [target]},
    }
    global_payload = {
        "version": 1,
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": target["access_token"],
                    "refresh_token": target["refresh_token"],
                }
            }
        },
    }
    profile_path.write_text(json.dumps(profile_payload))
    global_path.write_text(json.dumps(global_payload))
    profile_before = profile_path.read_bytes()
    global_before = global_path.read_bytes()
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    real_source_save = auth_module._save_provider_state_to_source
    real_restore = auth_module._restore_auth_store_bytes

    def commit_then_raise(*args, **kwargs):
        real_source_save(*args, **kwargs)
        raise OSError("post-commit source save failed")

    def fail_selected_rollback(path, payload):
        if (rollback_target == "source" and path == global_path) or (
            rollback_target == "active" and path == profile_path
        ):
            raise OSError(f"{rollback_target} rollback failed")
        real_restore(path, payload)

    monkeypatch.setattr(
        auth_module, "_save_provider_state_to_source", commit_then_raise
    )
    monkeypatch.setattr(
        auth_module, "_restore_auth_store_bytes", fail_selected_rollback
    )

    with caplog.at_level("CRITICAL"), pytest.raises(
        OSError, match="post-commit source save failed"
    ) as exc_info:
        auth_module._quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {"reason": "synthetic-terminal"},
        )

    assert (profile_path.read_bytes() == profile_before) is (
        rollback_target == "source"
    )
    assert (global_path.read_bytes() == global_before) is (
        rollback_target == "active"
    )
    assert any(
        f"{rollback_target} rollback failed" in note
        for note in exc_info.value.__notes__
    )
    assert "credential quarantine rollback failed" in caplog.text
    assert str(profile_path) in caplog.text
    assert str(global_path) in caplog.text


def test_d3_restore_auth_store_bytes_fsyncs_file_and_parent_directory(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    target_path = tmp_path / "auth.json"
    target_path.write_bytes(b"old")
    observed = []
    real_fsync = auth_module.os.fsync

    def record_fsync(fd):
        observed.append(stat.S_ISDIR(auth_module.os.fstat(fd).st_mode))
        real_fsync(fd)

    monkeypatch.setattr(auth_module.os, "fsync", record_fsync)

    auth_module._restore_auth_store_bytes(target_path, b"restored")

    assert target_path.read_bytes() == b"restored"
    assert observed == [False, True]


@pytest.mark.parametrize("failed_restore", ["source", "active"])
def test_d3_codex_quarantine_restore_directory_fsync_failure_is_diagnosed(
    tmp_path, monkeypatch, caplog, failed_restore
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_path.write_text(
        json.dumps(
            {
                "version": 1,
                "providers": {},
                "credential_pool": {"openai-codex": [target]},
            }
        )
    )
    global_path.write_text(
        json.dumps(
            {
                "version": 1,
                "providers": {
                    "openai-codex": {
                        "tokens": {
                            "access_token": target["access_token"],
                            "refresh_token": target["refresh_token"],
                        }
                    }
                },
            }
        )
    )
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    real_source_save = auth_module._save_provider_state_to_source
    real_fsync = auth_module.os.fsync
    directory_fsyncs = 0

    def commit_then_raise(*args, **kwargs):
        real_source_save(*args, **kwargs)
        raise OSError("post-commit source save failed")

    def fail_selected_directory_fsync(fd):
        nonlocal directory_fsyncs
        if stat.S_ISDIR(auth_module.os.fstat(fd).st_mode):
            directory_fsyncs += 1
            failed_index = 3 if failed_restore == "source" else 4
            if directory_fsyncs == failed_index:
                raise OSError(f"{failed_restore} restore directory fsync failed")
        real_fsync(fd)

    monkeypatch.setattr(
        auth_module, "_save_provider_state_to_source", commit_then_raise
    )
    monkeypatch.setattr(auth_module.os, "fsync", fail_selected_directory_fsync)

    with caplog.at_level("CRITICAL"), pytest.raises(
        OSError, match="post-commit source save failed"
    ) as exc_info:
        auth_module._quarantine_codex_pool_credential_exact(
            "pinned-id",
            target["access_token"],
            target["refresh_token"],
            {"reason": "synthetic-terminal"},
        )

    assert directory_fsyncs == 4
    assert any(
        f"{failed_restore} restore directory fsync failed" in note
        for note in exc_info.value.__notes__
    )
    assert "credential quarantine rollback failed" in caplog.text


def test_d3_pinned_codex_refresh_source_commit_failure_restores_both_stores(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    profile_path = tmp_path / "hermes" / "auth.json"
    global_path = tmp_path / "global-auth.json"
    global_path.write_text(
        json.dumps(
            {
                "version": 1,
                "providers": {
                    "openai-codex": {
                        "tokens": {
                            "access_token": target["access_token"],
                            "refresh_token": target["refresh_token"],
                        }
                    }
                },
            }
        )
    )
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    profile_before = profile_path.read_bytes()
    global_before = global_path.read_bytes()
    previous = pool.entries()[0]
    updated_payload = previous.to_dict()
    updated_payload["access_token"] = "new-access"
    updated_payload["refresh_token"] = "new-refresh"
    updated = type(previous).from_dict("openai-codex", updated_payload)
    pool._current_id = previous.id
    real_source_save = auth_module._save_provider_state_to_source

    def commit_then_raise(*args, **kwargs):
        real_source_save(*args, **kwargs)
        raise OSError("post-commit refresh source save failed")

    monkeypatch.setattr(
        auth_module, "_save_provider_state_to_source", commit_then_raise
    )

    with pytest.raises(OSError, match="post-commit refresh source save failed"):
        pool._commit_credential_update(previous, updated)

    assert profile_path.read_bytes() == profile_before
    assert global_path.read_bytes() == global_before
    assert pool.entries()[0].access_token == previous.access_token
    assert pool.entries()[0].refresh_token == previous.refresh_token
    assert pool._current_id == previous.id


def test_d3_pinned_codex_refresh_global_success_preserves_active_providers(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    profile_path = tmp_path / "hermes" / "auth.json"
    profile_payload = json.loads(profile_path.read_text())
    profile_payload["active_provider"] = "profile-provider"
    profile_payload["providers"] = {
        "profile-provider": {"metadata": "profile-preserved"}
    }
    profile_path.write_text(json.dumps(profile_payload))
    global_path = tmp_path / "global-auth.json"
    global_path.write_text(
        json.dumps(
            {
                "version": 1,
                "active_provider": "global-provider",
                "providers": {
                    "global-provider": {"metadata": "global-preserved"},
                    "openai-codex": {
                        "tokens": {
                            "access_token": target["access_token"],
                            "refresh_token": target["refresh_token"],
                        },
                        "last_refresh": 1.0,
                    },
                },
            }
        )
    )
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    previous = pool.entries()[0]
    updated_payload = previous.to_dict()
    updated_payload.update(
        access_token="new-access",
        refresh_token="new-refresh",
        last_refresh=2.0,
    )
    updated = type(previous).from_dict("openai-codex", updated_payload)

    committed = pool._commit_credential_update(previous, updated)

    persisted_profile = json.loads(profile_path.read_text())
    persisted_global = json.loads(global_path.read_text())
    assert committed.access_token == "new-access"
    assert persisted_profile["active_provider"] == "profile-provider"
    assert persisted_profile["providers"] == {
        "profile-provider": {"metadata": "profile-preserved"}
    }
    assert persisted_global["active_provider"] == "global-provider"
    assert persisted_global["providers"]["global-provider"] == {
        "metadata": "global-preserved"
    }
    assert persisted_global["providers"]["openai-codex"] == {
        "tokens": {
            "access_token": "new-access",
            "refresh_token": "new-refresh",
        },
        "last_refresh": 2.0,
    }


def test_d3_pinned_codex_refresh_active_commit_failure_restores_exact_store(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    profile_path = tmp_path / "hermes" / "auth.json"
    profile_payload = json.loads(profile_path.read_text())
    profile_payload["providers"] = {
        "openai-codex": {
            "tokens": {
                "access_token": target["access_token"],
                "refresh_token": target["refresh_token"],
            },
            "last_refresh": 1.0,
        }
    }
    profile_path.write_text(json.dumps(profile_payload))
    profile_before = profile_path.read_bytes()
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: None)
    previous = pool.entries()[0]
    updated_payload = previous.to_dict()
    updated_payload.update(
        access_token="new-access",
        refresh_token="new-refresh",
        last_refresh=2.0,
    )
    updated = type(previous).from_dict("openai-codex", updated_payload)
    pool._current_id = previous.id
    real_active_save = auth_module._save_auth_store

    def commit_then_raise(*args, **kwargs):
        real_active_save(*args, **kwargs)
        raise OSError("post-commit active refresh save failed")

    monkeypatch.setattr(auth_module, "_save_auth_store", commit_then_raise)

    with pytest.raises(OSError, match="post-commit active refresh save failed"):
        pool._commit_credential_update(previous, updated)

    assert profile_path.read_bytes() == profile_before
    assert pool.entries()[0].access_token == previous.access_token
    assert pool.entries()[0].refresh_token == previous.refresh_token
    assert pool._current_id == previous.id


def test_d3_pinned_codex_refresh_active_success_persists_provider_metadata(
    tmp_path, monkeypatch
):
    import hermes_cli.auth as auth_module

    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    profile_path = tmp_path / "hermes" / "auth.json"
    profile_payload = json.loads(profile_path.read_text())
    profile_payload["providers"] = {
        "openai-codex": {
            "tokens": {
                "access_token": target["access_token"],
                "refresh_token": target["refresh_token"],
            },
            "last_refresh": 1.0,
        }
    }
    profile_path.write_text(json.dumps(profile_payload))
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: None)
    previous = pool.entries()[0]
    updated_payload = previous.to_dict()
    updated_payload.update(
        access_token="new-access",
        refresh_token="new-refresh",
        last_refresh=2.0,
    )
    updated = type(previous).from_dict("openai-codex", updated_payload)

    committed = pool._commit_credential_update(previous, updated)

    persisted = json.loads(profile_path.read_text())
    persisted_row = persisted["credential_pool"]["openai-codex"][0]
    persisted_provider = persisted["providers"]["openai-codex"]
    assert committed.access_token == "new-access"
    assert persisted_row["access_token"] == "new-access"
    assert persisted_row["refresh_token"] == "new-refresh"
    assert persisted_row["last_refresh"] == 2.0
    assert persisted_provider["tokens"] == {
        "access_token": "new-access",
        "refresh_token": "new-refresh",
    }
    assert persisted_provider["last_refresh"] == 2.0


@pytest.mark.parametrize("operation", ["sync", "quarantine"])
def test_d3_codex_global_source_disappearance_fails_closed(
    tmp_path, monkeypatch, operation
):
    import hermes_cli.auth as auth_module

    profile_path = tmp_path / "profile-auth.json"
    global_path = tmp_path / "global-auth.json"
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    target["source"] = "device_code"
    profile_payload = {
        "version": 1,
        "providers": {},
        "credential_pool": {"openai-codex": [target]},
    }
    global_payload = {"version": 1, "providers": {}}
    profile_path.write_text(json.dumps(profile_payload))
    global_path.write_text(json.dumps(global_payload))
    profile_before = profile_path.read_bytes()
    global_before = global_path.read_bytes()
    monkeypatch.setattr(auth_module, "_auth_file_path", lambda: profile_path)
    monkeypatch.setattr(auth_module, "_global_auth_file_path", lambda: global_path)
    monkeypatch.setattr(
        auth_module,
        "_load_provider_state_with_source",
        lambda _store, _provider: (
            {
                "tokens": {
                    "access_token": target["access_token"],
                    "refresh_token": target["refresh_token"],
                }
            },
            global_path,
        ),
    )

    with pytest.raises(
        auth_module.AuthError,
        match="provider source changed",
    ) as exc_info:
        if operation == "sync":
            auth_module._sync_codex_pool_credential_from_provider_exact(
                "pinned-id"
            )
        else:
            auth_module._quarantine_codex_pool_credential_exact(
                "pinned-id",
                target["access_token"],
                target["refresh_token"],
                {"reason": "synthetic-terminal"},
            )

    assert exc_info.value.code == "codex_target_credential_changed"
    assert profile_path.read_bytes() == profile_before
    assert global_path.read_bytes() == global_before


def test_d3_credential_pinned_remove_preserves_latest_disk_siblings(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0)
    removed = _d3_codex_entry("remove-id", "REMOVE", 1)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 2)
    stale_deleted = _d3_codex_entry("stale-id", "STALE", 3)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, removed, sibling, stale_deleted],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    target["access_token"] = "target-concurrent-access"
    target["refresh_token"] = "target-concurrent-refresh"
    sibling["access_token"] = "sibling-concurrent-access"
    sibling["refresh_token"] = "sibling-concurrent-refresh"
    write_credential_pool(
        "openai-codex",
        [target, removed, sibling],
        removed_ids=["stale-id"],
    )

    deleted = pool.remove_index(2)
    assert deleted is not None and deleted.id == "remove-id"

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert {entry["id"] for entry in entries} == {"pinned-id", "sibling-id"}
    persisted_sibling = next(entry for entry in entries if entry["id"] == "sibling-id")
    assert persisted_sibling["access_token"] == "sibling-concurrent-access"
    assert persisted_sibling["refresh_token"] == "sibling-concurrent-refresh"
    assert [entry.id for entry in pool.entries()] == ["pinned-id", "sibling-id"]
    assert pool.entries()[0].access_token == "target-concurrent-access"
    assert pool.entries()[1].access_token == "sibling-concurrent-access"

    pool._mark_exhausted(pool.entries()[0], 429)
    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    persisted_target = next(
        entry
        for entry in payload["credential_pool"]["openai-codex"]
        if entry["id"] == "pinned-id"
    )
    assert persisted_target["access_token"] == "target-concurrent-access"
    assert persisted_target["refresh_token"] == "target-concurrent-refresh"


def test_d3_credential_pinned_remove_failure_keeps_memory_and_disk_atomic(
    tmp_path, monkeypatch
):
    pinned = _d3_codex_entry("pinned-id", "PINNED", 0)
    target = _d3_codex_entry("remove-id", "REMOVE", 1)
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 2)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [pinned, target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    auth_path = tmp_path / "hermes" / "auth.json"
    payload = json.loads(auth_path.read_text())
    duplicate = dict(payload["credential_pool"]["openai-codex"][1])
    duplicate["label"] = "DUPLICATE"
    payload["credential_pool"]["openai-codex"].append(duplicate)
    auth_path.write_text(json.dumps(payload))

    from hermes_cli.auth import AuthError

    for _attempt in range(2):
        with pytest.raises(AuthError) as excinfo:
            pool.remove_index(2)

        assert excinfo.value.code == "codex_target_credential_changed"
        assert [entry.id for entry in pool.entries()] == [
            "pinned-id",
            "remove-id",
            "sibling-id",
        ]
        assert [entry.priority for entry in pool.entries()] == [0, 1, 2]
        persisted = json.loads(auth_path.read_text())["credential_pool"][
            "openai-codex"
        ]
        assert [entry["id"] for entry in persisted].count("remove-id") == 2


def test_d3_credential_pinned_cooldown_clear_reconciles_latest_disk(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="exhausted")
    target["last_status_at"] = 1.0
    target["last_error_reset_at"] = 1.0
    sibling = _d3_codex_entry("sibling-id", "SIBLING", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    target["access_token"] = "target-concurrent-access"
    target["refresh_token"] = "target-concurrent-refresh"
    sibling["access_token"] = "sibling-concurrent-access"
    sibling["refresh_token"] = "sibling-concurrent-refresh"
    sibling["last_status"] = "exhausted"
    sibling["last_error_code"] = "429"
    write_credential_pool("openai-codex", [target, sibling])
    monkeypatch.setattr(pool, "_sync_codex_entry_from_auth_store", lambda entry: entry)

    selected = pool.select()
    assert selected is not None and selected.id == "pinned-id"
    assert selected.access_token == "target-concurrent-access"
    assert selected.refresh_token == "target-concurrent-refresh"
    assert selected.last_status == "ok"

    payload = json.loads((tmp_path / "hermes" / "auth.json").read_text())
    entries = payload["credential_pool"]["openai-codex"]
    assert [entry.id for entry in pool.entries()] == [
        entry["id"] for entry in entries
    ]
    persisted_target = next(entry for entry in entries if entry["id"] == "pinned-id")
    assert persisted_target["access_token"] == "target-concurrent-access"
    assert persisted_target["refresh_token"] == "target-concurrent-refresh"
    assert persisted_target["last_status"] == "ok"
    persisted_sibling = next(entry for entry in entries if entry["id"] == "sibling-id")
    assert persisted_sibling["access_token"] == "sibling-concurrent-access"
    assert persisted_sibling["refresh_token"] == "sibling-concurrent-refresh"
    assert persisted_sibling["last_status"] == "exhausted"
    assert persisted_sibling["last_error_code"] == "429"


def test_d3_credential_pinned_cooldown_clear_failure_keeps_memory_and_disk_atomic(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="exhausted")
    target["last_status_at"] = 1.0
    target["last_error_reset_at"] = 1.0
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )
    auth_path = tmp_path / "hermes" / "auth.json"
    before_memory = pool.entries()
    before_disk = auth_path.read_text()

    from hermes_cli.auth import AuthError
    import agent.credential_pool as credential_pool_module

    def reject_status_merge(_payload):
        raise AuthError(
            "synthetic merge failure",
            provider="openai-codex",
            code="codex_target_credential_changed",
            relogin_required=False,
        )

    monkeypatch.setattr(
        credential_pool_module.auth_mod,
        "_merge_codex_pool_credential_status_exact",
        reject_status_merge,
    )

    for _attempt in range(2):
        with pytest.raises(AuthError) as excinfo:
            pool.select()
        assert excinfo.value.code == "codex_target_credential_changed"
        assert pool.entries() == before_memory
        assert auth_path.read_text() == before_disk


def test_d3_credential_pinned_aged_dead_prune_rejects_duplicate_disk_target(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="dead")
    target["last_status_at"] = 1.0
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    auth_path = tmp_path / "hermes" / "auth.json"
    payload = json.loads(auth_path.read_text())
    duplicate = dict(payload["credential_pool"]["openai-codex"][0])
    duplicate["label"] = "DUPLICATE"
    payload["credential_pool"]["openai-codex"].append(duplicate)
    auth_path.write_text(json.dumps(payload))

    from hermes_cli.auth import AuthError

    for _attempt in range(2):
        with pytest.raises(AuthError) as excinfo:
            pool.select()

        assert excinfo.value.code == "codex_target_credential_changed"
        assert [entry.id for entry in pool.entries()] == ["pinned-id"]


def test_d3_credential_pinned_aged_dead_prune_reconciles_latest_disk(
    tmp_path, monkeypatch
):
    target = _d3_codex_entry("pinned-id", "PINNED", 0, status="dead")
    target["last_status_at"] = 1.0
    stale_sibling = _d3_codex_entry("stale-id", "STALE", 1)
    pool = _load_d3_codex_pool(
        tmp_path,
        monkeypatch,
        [target, stale_sibling],
        "HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=pinned-id\n",
    )

    from hermes_cli.auth import write_credential_pool

    latest_sibling = _d3_codex_entry("latest-id", "LATEST", 1)
    latest_sibling["access_token"] = "latest-sibling-access"
    write_credential_pool(
        "openai-codex",
        [target, latest_sibling],
        removed_ids=["stale-id"],
    )

    assert pool.select() is None
    assert [entry.id for entry in pool.entries()] == ["latest-id"]
    assert pool.entries()[0].access_token == "latest-sibling-access"
