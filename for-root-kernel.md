# Root Kernel Hermes Agent v0.18.2 carry log

## Baseline

- Upstream code base: Hermes Agent `v0.18.2` / tag `v2026.7.7.2`
- Upstream base commit: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Candidate branch: `rk/v0.18.2`
- Previous downstream branch: `rk/v0.17.0`
- Previous downstream commit/restore point: `79780a587ecb260788a23767d9996d5f7042a311` / `rk/tag/v0.17.0`, `origin/rk/v0.17.0`, `origin/rk/live`
- Evidence window:
  - `v0.18.0` / `v2026.7.1` / `7c1a029553d87c43ecff8a3821336bc95872213b` / `root-kernel/evidence/release-note-v2026.7.1.md`
  - `v0.18.1` / `v2026.7.7` / `f9eca7e15f1c2bfe5194aae5aa489af53c0a1a23` / `root-kernel/evidence/release-note-v2026.7.7.md`
  - `v0.18.2` / `v2026.7.7.2` / `9de9c25f620ff7f1ce0fd5457d596052d5159596` / `root-kernel/evidence/release-note-v2026.7.7.2.md`
- Goal: run Root Kernel on v0.18.2 while absorbing upstream features first and retaining only minimal Root Kernel-specific fail-closed/runtime seams.
- Scaffold created: `2026-07-09T16:05:24+09:00`

## Base selection decision

주군 and 흑태자 selected `v2026.7.7.2` as the code base for `rk/v0.18.2`. Earlier v0.18.0 and v0.18.1 release notes are evidence for impact analysis, not sequential merge steps. This avoids an unstable base while still preserving release-window awareness.

## Local hygiene

- `.omx/` is local editor/agent runtime state and is ignored in `.gitignore`.
- Verification: `git check-ignore -v .omx .omx/hud-config.json` matched `.gitignore`.

## Release-note signals to absorb

- v0.18.0: P0/P1 clean sweep, first-class Mixture-of-Agents, evidence-based self-verification, `/goal` completion contracts, `/learn`, `/journey`, background subagents, gateway scale-to-zero/drain coordination, desktop/dashboard growth.
- v0.18.1: infrastructure patch roll-up of roughly 660 PRs since v0.18.0, including installer/updater self-healing on Windows, dashboard/gateway fixes, WhatsApp dashboard pairing, MCP/provider fixes, and broad stability work.
- v0.18.2: WhatsApp Baileys dependency changed to published `7.0.0-rc13` for reliable installs and Docker image builds.

## D-item priority order

1. D8 — OpenAI Codex credential pinning and labelled reauth.
2. D4 — Discord owner/thread routing and role-mention fail-close.
3. D2 — Kanban review and same-card handoff helpers.
4. D6 — CLI return-code passthrough.
5. D7 — Doctor optional tool warning filter.

D1, D3, and D5 remain retired/resolved unless a new independent regression appears.

## D-item direction gates

Every D item requires owner direction before code application: choose upstream-native adoption, upstream plus Root Kernel safety extension, local enhancement, retire, or defer.

### D1 — Tool Search pair

- Previous v0.17 state: resolved; no local carry.
- v0.18.2 starting decision: retired carry-forward. Do not replay.

### D2 — Kanban review and same-card handoff helpers

- Previous v0.17 state: D2-a through D2-i applied.
- v0.18.2 state: D2-a native-overlap audit complete; D2-b unified same-card review loop applied; D2-f async review watcher applied; D2-g creator/acceptor result loop applied; D2-h through D2-i remain pending.
- Decision: use partial-native local-minimized carry. Preserve v0.18.2 native review/goal/notify/swarm/workflow foundations and add only missing Root Kernel same-card seams.
- Evidence: `root-kernel/evidence/d2-a-kanban-native-overlap.md`.
- Native foundations retained:
  - `review` status, `claim_review_task`, review dispatch, and `has_spawnable_review`;
  - `kanban_notify_subs`, notify subscribe/list/unsubscribe, dashboard home-subscribe, and gateway Kanban notifier;
  - `/goal` completion contracts and Kanban `goal_mode` / `goal_max_turns`;
  - background `delegate_task` fan-out;
  - Kanban Swarm v1 (`parallel workers -> verifier -> synthesizer`);
  - `workflow_template_id` / `current_step_key` generic workflow metadata.
- Missing Root Kernel seams to carry, without changing the user-facing D2 workflow:
  - D2-b same-card review loop applied as a unified patch, preserving former D2-b/c/d/e lineage:
    - cooperative same-card handoff / worker-facing reassign;
    - worker submit-for-review seam on top of native review;
    - reviewer request-changes return-to-rework loop;
    - creator/final gate after reviewer approval.
  - D2-f async review watcher applied:
    - `kanban_submit_review` auto-attaches a review watch subscription when a gateway/TUI delivery source is available;
    - worker response includes `review_watch` attachment metadata or `attached: false` for CLI/cron/unattached contexts;
    - gateway Kanban notifier delivers `requested_changes` and `review_accepted` review outcomes without unsubscribing before final task state.
  - D2-g creator/acceptor result submission loop applied:
    - `submit_task_result` closes worker runs as `submitted_result` / `released` and routes the same card to creator/acceptor review;
    - `kanban_submit_result` tool and CLI `submit-result` expose result acceptance without marking the task done;
    - creator/acceptor `kanban_complete` marks final `done`, while `kanban_request_changes` returns to the original worker from `submitted_result` provenance;
    - worker guidance distinguishes final completion, peer review, and creator/acceptor result acceptance.
  - D2-h mutex-key serialization;
  - D2-i closed workflow context banners.
- Audit smoke:
  - Symbol probe: D2 handoff/submit-review/request-changes/submit-result symbols absent; native review/workflow metadata present; `mutex_key` / `workflow_type` absent.
  - Native review focused pytest slice: `10 passed in 0.76s`.
  - Review/goal/notify overlap pytest slice: `15 passed in 1.37s`.
- D2-b RED evidence:
  - Focused same-card review-loop tests failed on v0.18.2 base because `handoff_task`, `submit_task_for_review`, `request_changes_task`, and `kanban_reassign` / `kanban_submit_review` / `kanban_request_changes` registrations were absent: `7 failed`.
- D2-b GREEN evidence:
  - Focused DB/tool same-card review loop tests: `18 passed in 1.31s`.
  - Worker/orchestrator Kanban tool visibility tests: `4 passed in 0.91s`.
  - `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py`: `338 passed in 27.70s`.
- D2-f RED evidence:
  - Focused review watcher tests failed on v0.18.2+D2-b because `kanban_submit_review` returned no `review_watch` receipt/subscription and notifier watched neither `requested_changes` nor `review_accepted`: `5 failed`.
- D2-f GREEN evidence:
  - Focused review watcher tests: `5 passed in 0.66s`.
  - `tests/tools/test_kanban_tools.py tests/gateway/test_kanban_notifier.py`: `113 passed in 10.38s`.
- D2-g RED evidence:
  - Focused result-submission tests failed on v0.18.2+D2-b/f because `submit_task_result`, `kanban_submit_result`, CLI `submit-result`, toolset visibility, request-changes result provenance, and worker prompt guidance were absent: `9 failed`.
- D2-g GREEN evidence:
  - Focused DB/tool/CLI/prompt result-submission tests: `9 passed in 2.90s`.
  - `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_cli.py tests/gateway/test_kanban_notifier.py`: `407 passed in 34.13s`.
- Boundary: no live profile state, gateway, token, production Kanban DB, `rk/live`, push, or tag was mutated.
- Next action: implement D2-h mutex-key serialization, preserving D2-b same-card review loop, D2-f async review-outcome notifications, and D2-g result acceptance semantics.

### D3 — Kanban assignee alias dispatch seam

- Previous v0.17 state: retired.
- v0.18.2 starting decision: retired carry-forward. Do not replay.

### D4 — Discord owner/thread routing and role-mention fail-close

- Previous v0.17 state: local keep applied, including free-response auto-thread config bridge hotfix.
- v0.18.2 state: local-minimized carry applied after owner selected option A.
- Decision: preserve v0.18.2 upstream Discord improvements, then reapply only Root Kernel-specific thread-owner/free-response/role-mention seams.
- Upstream retained:
  - current v0.18.2 channel-key matching and parent/name handling;
  - auto-thread failure visible-error/no-agent fallback;
  - auto-thread rename metadata;
  - Discord liveness/reconnect improvements.
- Local D4 seams added:
  - persistent `ThreadOwnerTracker` (`discord_thread_owners.json`) for thread default responder ownership;
  - mention-free thread replies require this bot to own the thread, not merely have participated;
  - auto-created threads are marked as participated and owned by the creating bot;
  - `DISCORD_AUTO_THREAD_FREE_RESPONSE` and config-extra `auto_thread_free_response` allow selected free-response channels to spawn owned auto-threads;
  - top-level `discord.auto_thread_free_response` bridges through the plugin `_apply_yaml_config()` hook;
  - env-only `DISCORD_DEFAULT_THREAD_OWNER_PARENT_CHANNELS` can claim unowned user-created child threads under approved single-owner parents;
  - role mentions fail closed unless this bot is explicitly mentioned;
  - `thread_require_mention=true` still gates owned/default parent-thread fallback.
- Files changed:
  - `gateway/platforms/helpers.py`
  - `plugins/platforms/discord/adapter.py`
  - `tests/gateway/test_discord_free_response.py`
  - `tests/gateway/test_discord_channel_controls.py`
  - `tests/e2e/conftest.py`
- RED evidence:
  - D4 focused tests failed on v0.18.2 base: missing `_thread_owners`, role mentions processed, free-response auto-thread option ignored, YAML bridge absent.
- GREEN evidence:
  - `tests/gateway/test_discord_free_response.py`: `66 passed`.
  - `tests/gateway/test_discord_free_response.py tests/gateway/test_discord_channel_controls.py`: `82 passed`, with 2 upstream dependency deprecation warnings.
  - `tests/e2e/test_discord_adapter.py`: `7 passed`.
  - Combined D4 Discord suite: `89 passed`, with 2 upstream dependency deprecation warnings.
  - Isolation check: gateway/e2e Discord tests now use temp/no-op tracker state; live `/Users/draccoon/.hermes/discord_threads.json` and `discord_thread_owners.json` stat unchanged across final run and fake IDs absent.
- Boundary: no live Discord token, profile env, gateway process, `rk/live`, push, or tag was mutated.

### D5 — Support-only plugin strategy

- Previous v0.17 state: retired/no-code.
- v0.18.2 starting decision: retired carry-forward. Do not replay.

### D6 — CLI return-code passthrough

- Previous v0.17 state: local keep applied.
- v0.18.2 state: not yet evaluated.
- Next action: audit top-level CLI dispatch process return codes before carrying exact-int passthrough.

### D7 — Doctor optional tool warning filter

- Previous v0.17 state: local keep applied.
- v0.18.2 state: not yet evaluated.
- Next action: audit doctor Tool Availability warning scoping before carrying optional-warning filter.

### D8 — OpenAI Codex credential pinning and labelled reauth

- Previous v0.17 state: minimized local keep applied.
- v0.18.2 state: local-minimized carry applied on top of upstream native account-split behavior.
- Decision: keep v0.18.2 upstream independent `openai-codex` pool behavior, then add only Root Kernel-specific account-affinity seams.
- Upstream retained:
  - `hermes auth add openai-codex` already creates independent `manual:device_code` pool entries instead of collapsing through the provider singleton.
  - `_sync_codex_pool_entries()` preserves independent manual entries and only refreshes singleton/legacy aliases.
- Local D8 seams added:
  - profile-local `.env` pins: `HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID`, `HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL`, and bare prefix-as-label convenience;
  - ambient process env is ignored for pins;
  - ID wins over label; label matching is exact and unique across the whole pool;
  - missing/duplicate/exhausted/dead/unavailable pinned credentials fail closed;
  - main runtime and auxiliary Codex paths do not fall back to singleton `auth.json` when a pin is configured but unavailable;
  - `hermes auth add openai-codex --label <LABEL>` updates exactly one matching device-code/manual-device-code pool entry and fails closed on duplicate labels.
- Files changed:
  - `agent/credential_pool.py`
  - `agent/auxiliary_client.py`
  - `hermes_cli/runtime_provider.py`
  - `hermes_cli/auth_commands.py`
  - `tests/agent/test_credential_pool.py`
  - `tests/agent/test_auxiliary_client.py`
  - `tests/hermes_cli/test_runtime_provider_resolution.py`
  - `tests/hermes_cli/test_auth_commands.py`
- RED evidence:
  - D8 pin/auth tests failed on v0.18.2 base before implementation: label pin selected `JYH` instead of pinned `HSY`, duplicate label did not fail closed, auxiliary/runtime fell back to singleton auth.
- GREEN evidence:
  - D8-focused command: `28 passed, 80 deselected`.
  - `tests/hermes_cli/test_auth_commands.py tests/hermes_cli/test_runtime_provider_resolution.py`: `204 passed`.
  - `tests/agent/test_auxiliary_client.py`: `299 passed`.
  - Disposable no-token host selection smoke: `selected_label HSY`, `selected_id hsy`.
  - Docker pilot, read-only candidate mount + disposable `HERMES_HOME`: 4 D8 `credential_pool` tests passed.
  - Docker pilot functional smoke: `docker-pilot-positive pinned PINNED`, `docker-pilot-unavailable None`.
  - Owner-approved Docker actual-JYH smoke with minimal temporary auth copy: `selected_label JYH`, `selected_id 253e66`, `response_text hi`, `smoke_ok True`, `container_removed true`, `temp_cleanup true`.
- Boundary: no live `.env`, `auth.json`, token, profile home, gateway process, `rk/live`, push, or tag was mutated.

## R-item activation boundary

R-items are activation/local-state gates, not product-code D-item carries. They remain pending until the candidate code branch stabilizes.

- R1: config/profile migration and doctor/check gate — pending R-pre.
- R2: skill provenance and resolver compatibility — pending R-pre.
- R3: dashboard/desktop gate — pending R-pre; Desktop remains unused unless 주군 changes scope.
- R4: cron/script/watcher/local automation gate — pending R-pre.
- R5: profile-owned local asset optimization — post-activation/non-blocking unless 주군 scopes it as blocker.

## Docker smoke rule

Before moving `rk/live`, reinstalling runtime, or migrating `/Users/draccoon/.hermes/hermes-agent/`, retained D-items need targeted smoke with disposable boundaries where possible:

- read-only repo mount or clean disposable checkout;
- disposable `HERMES_HOME`;
- no live `.env`, `auth.json`, tokens, production profile homes, gateway sockets, or production databases;
- smoke must exercise actual CLI/tool/runtime behavior for the D-item, not only parse source files.

## Activation boundary

This scaffold does not authorize moving `rk/live`, replacing or repointing `/Users/draccoon/.hermes/hermes-agent/`, editable runtime reinstall, profile config migration, gateway restart, dashboard/desktop persistent launchd changes, live platform sends, push, or tag creation.
