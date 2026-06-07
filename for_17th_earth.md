# 17th Earth Local Change Ledger

This file is the operational source of truth for the 17번째 지구 local Hermes runtime carry set. It is agent-facing: use it as a runbook, not as background reading.

The current release-candidate branch is `17e/v0.16.0-re`, based on upstream Hermes Agent tag `v2026.6.5` (`v0.16.0`, commit `3c231eb39`). The pre-update live/freeze branch was `for_17e_earth` / `for_17th_earth` at commit `ca5432664` with D1-D6 recorded.

## Hard rules

1. Do not touch the live runtime checkout, live `.env`, production Kanban DB, or running gateways while preparing this release candidate.
2. Prefer upstream-native behavior over preserving old local APIs.
3. Do not mark a delta `absorbed`, `keep`, or `retired` in this baseline commit. Record that decision only in the same per-delta commit that applies, drops, or retires the related runtime change.
4. A future `drop` decision means: **do not delete the ledger entry**. Mark the delta as absorbed/retired with the upstream version or decision evidence in that per-delta commit, then keep it available for the next release audit.
5. Apply only the smallest generic runtime seam still required after classifying each delta.
6. Do not recreate support-only plugins. A plugin is acceptable only if it carries real behavior without broad new runtime hooks.
7. Use targeted smoke for touched deltas plus `git diff --check`; do not run the full macOS suite by default.
8. Update this ledger in the same commit as any retained, absorbed, or retired runtime delta.
9. Never report the update complete until code, smoke evidence, this ledger, and any workflow/skill wording are consistent.

## v0.16.0 update workflow

Use this order for the `17e/v0.16.0-re` worktree:

1. Copy this ledger into the release-candidate worktree and commit the ledger baseline first.
2. Produce or update `17e/carry.yaml` from the Delta index below.
3. For D1-D6, evaluate against the exact release base (`v2026.6.5`) before changing runtime code.
4. Do not write final delta status into this ledger until the per-delta code/drop/retire commit.
5. For future `upstream-absorbed` entries, mark the absorbed version/evidence and do not carry code.
6. For future `still-local seam` entries, re-apply the minimal patch and tests.
7. For future `partial-native` entries, use upstream-native code where sufficient and patch only the missing 17번째 지구 contract.
8. Run targeted host smoke for touched areas.
9. Run Docker smoke only with a disposable `HERMES_HOME` and read-only candidate assumptions.
10. Only after explicit approval, repoint/apply `17e/live` to the prepared release branch.

## Classification vocabulary

Use these labels in per-delta commits only, not as final baseline markings:

- `upstream-absorbed`: exact or equivalent upstream behavior is present in the release base; no local code carry.
- `partial-native`: upstream provides a useful base, but a smaller local seam is still required for the 17번째 지구 contract.
- `still-local seam`: no upstream equivalent; re-apply the minimal generic seam and tests.
- `retired`: the behavior or strategy should not be recreated; keep only the ledger note.
- `redesign`: upstream architecture changed enough that a straight patch is unsafe.

## Delta index for v0.16.0 / `v2026.6.5`

| ID | Change title | Baseline state | Per-delta work to do | Preflight evidence to verify |
|---|---|---|---|---|
| D1 | [Tool Search pair](#d1-tool-search-pair) | `upstream-absorbed` by `v2026.6.5` | Drop local D1 carry; do not apply Tool Search code patches on this release branch. | `git merge-base --is-ancestor` returned `0` for both `369075dc9` and `7427b9d58` against this branch. |
| D2 | [Kanban review and same-card handoff helpers](#d2-kanban-review-and-same-card-handoff-helpers) | D2-a audited: `partial-native`; D2-b/c applied; D2-d pending | Keep native v0.16 review queue/dispatch; re-apply only missing same-card transition/tool seams in D2-b/c/d. | Native `review` claim/dispatch exists; `handoff_task`, `submit_task_for_review`, `request_changes`, and tool surfaces were absent at D2-a audit. |
| D3 | [Kanban assignee alias resolution](#d3-kanban-assignee-alias-resolution) | `keep-local-carry` | Re-applied minimal dispatcher-only spawn-profile alias resolution. | v0.16.0 had no `kanban.assignee_aliases` / `resolve_assignee_profile` equivalent before this D3 commit. |
| D4 | [Discord gateway config and owner-thread routing seams](#d4-discord-gateway-config-and-owner-thread-routing-seams) | pending per-delta decision | Separate absorbed generic config fixes from any still-needed owner-thread seam in the D4 commit. | Check `0bfe19ba1`, `44f3e5186`, `6d2727ef1`; inspect Discord owner tracking. |
| D5 | [Plugin strategy retirement](#d5-plugin-strategy-retirement) | pending per-delta decision | Reconfirm the support-only plugin strategy remains non-actionable; record the decision in the D5 commit. | Process decision; no runtime patch expected unless references/config still point to plugin behavior. |
| D6 | [CLI return-code passthrough](#d6-cli-return-code-passthrough) | `keep-local-carry` | Applied bool-safe top-level integer return-code passthrough. | Missing Kanban task now exits `1`; usage error exits `2`; bool return values are ignored. |

## D1 Tool Search pair

### v0.16.0 decision

`upstream-absorbed` by upstream tag `v2026.6.5` / release `v0.16.0`.

Do not re-apply local D1 commits on `17e/v0.16.0-re`. Keep this ledger section so the next release audit can re-check whether the Tool Search behavior remains native.

Decision evidence:

```bash
git merge-base --is-ancestor 369075dc9 HEAD  # rc 0
git merge-base --is-ancestor 7427b9d58 HEAD  # rc 0
```

### Purpose

- Progressive disclosure of MCP/plugin tools through Tool Search.
- Bridge catalog scope and dispatch must match the active session toolsets.

### Original upstream commits

- `369075dc9 feat(tools): progressive tool disclosure for MCP and plugin tools`
- `7427b9d58 fix(tool-search): scope bridge catalog + dispatch to the session's toolsets`

### Per-delta decision procedure

In the D1 commit, verify whether both original upstream commits or equivalent behavior are present in `v2026.6.5`. If yes, mark D1 as absorbed by that release and carry no local code. If only one side is present, inspect upstream follow-up commits before carrying anything.

### Release-candidate smoke

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_tool_search.py
# 39 passed, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  tools/tool_search.py \
  model_tools.py \
  agent/tool_executor.py \
  agent/agent_runtime_helpers.py \
  hermes_cli/config.py
# passed

git diff --check
# passed
```

### Smoke if D1 is touched again

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_tool_search.py
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  tools/tool_search.py \
  model_tools.py \
  agent/tool_executor.py \
  agent/agent_runtime_helpers.py \
  hermes_cli/config.py
```

## D2 Kanban review and same-card handoff helpers

### D2-a v0.16.0 audit decision

Decision: `partial-native`; do not replace v0.16.0's native review queue/dispatcher.

Re-apply D2 as smaller local-minimize subitems:

- D2-b: cooperative same-card handoff/reassign (`handoff_task`, `kanban_reassign`) — applied in `17e/v0.16.0-re`.
- D2-c: same-card submit-for-review (`submit_task_for_review`, `kanban_submit_review`) — applied in `17e/v0.16.0-re`.
- D2-d: request-changes/rework loop (`request_changes`, `kanban_request_changes`) plus final same-task-id synthetic smoke.

Audit evidence:

```bash
# Native v0.16 surfaces present in this branch:
git grep -n "def claim_review_task" -- hermes_cli/kanban_db.py
git grep -n "status = 'review'\|sdlc-review\|has_spawnable_review" -- hermes_cli/kanban_db.py tests/hermes_cli/test_kanban_db.py

# Old D2 local seams absent at D2-a audit time, before the D2-b patch:
git grep -n "def handoff_task\|def submit_task_for_review\|def request_changes" -- hermes_cli tools toolsets.py tests
# no matches
git grep -n "kanban_reassign\|kanban_submit_review\|kanban_request_changes" -- tools toolsets.py tests
# no matches

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_transitions_to_running \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_fails_on_non_review \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_fails_when_already_claimed \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_dry_run \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_spawns_with_correct_skills \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_skips_unassigned \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_skips_nonspawnable \
  tests/hermes_cli/test_kanban_db.py::test_has_spawnable_review_true \
  tests/hermes_cli/test_kanban_db.py::test_has_spawnable_review_false_on_empty \
  tests/hermes_cli/test_kanban_db.py::test_review_status_in_valid_statuses
# 10 passed
```

### D2-b v0.16.0 patch decision

Decision: `keep-local-carry` for cooperative same-card handoff/reassign. D2-c is now applied; D2-d remains pending.

Applied local seams:

- `hermes_cli/kanban_db.py`: `handoff_task(...)` closes the current run as `handed_off` / `released`, clears the claim, resets failure counters, and returns the same task id to `ready` for the target assignee.
- `tools/kanban_tools.py`: `kanban_reassign` worker/orchestrator tool surface with same-task ownership guard, stale-run guard via `HERMES_KANBAN_RUN_ID`, and worker session metadata stamping.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_handoff_task_closes_run_and_returns_same_card_to_ready \
  tests/hermes_cli/test_kanban_db.py::test_handoff_task_rejects_stale_run_id_without_mutation \
  tests/hermes_cli/test_kanban_db.py::test_kanban_reassign_tool_handoffs_current_worker_task
# 3 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_kanban_db.py
# 220 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py
# 250 passed, 1 skipped, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile hermes_cli/kanban_db.py tools/kanban_tools.py tests/hermes_cli/test_kanban_db.py
# passed

HERMES_HOME=<disposable-home> PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python - <<'PY'
# create running task, call tools.kanban_tools._handle_reassign, assert same task returns ready for target assignee
PY
# {"ok": true, "status": "ready", "assignee": "samaui", "event_count": 1}

docker run --rm -i \
  -v "$PWD:/repo:ro" \
  -w /repo \
  -e HERMES_HOME=/tmp/hermes-d2b-docker-smoke \
  -e PYTHONPATH=/repo \
  hermes-17e-d3-checkpoint-smoke:py311 \
  python - <<'PY'
# create two disposable profiles, create one Kanban task assigned to worker-a,
# dispatch worker-a, call kanban_reassign to worker-b, dispatch worker-b, and
# complete the same task id.
PY
# {"ok": true, "profiles": ["d2b-worker-a", "d2b-worker-b"], "task_id": "t_2ecfb7b2", "run_outcomes": ["handed_off", "completed"], "final_status": "done"}
```

### D2-c v0.16.0 patch decision

Decision: `keep-local-carry` for same-card submit-for-review. D2-d remains pending.

Applied local seams:

- `hermes_cli/kanban_db.py`: `submit_task_for_review(...)` closes the current worker run as `submitted_review` / `released`, preserves the implementer in the `submitted_review` event, clears claim state, and moves the same task id into native `review` status for the reviewer.
- `tools/kanban_tools.py`: `kanban_submit_review` worker/orchestrator tool surface with same-task ownership guard, stale-run guard via `HERMES_KANBAN_RUN_ID`, and worker session metadata stamping.
- `toolsets.py`: exposes `kanban_submit_review`; also exposes the D2-b `kanban_reassign` registration through the Hermes CLI/kanban toolset list.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_submit_task_for_review_moves_same_card_to_review \
  tests/hermes_cli/test_kanban_db.py::test_submit_task_for_review_defaults_to_profile_created_by \
  tests/hermes_cli/test_kanban_db.py::test_submit_task_for_review_fails_without_real_reviewer \
  tests/hermes_cli/test_kanban_db.py::test_submit_task_for_review_rejects_stale_run_id_without_mutation \
  tests/hermes_cli/test_kanban_db.py::test_kanban_submit_review_tool_submits_current_worker_task \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_env_var \
  tests/tools/test_kanban_tools.py::test_kanban_worker_env_overrides_profile_toolset_filter \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_toolset_config
# 8 passed, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_kanban_db.py
# 225 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py
# 250 passed, 1 skipped, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile hermes_cli/kanban_db.py tools/kanban_tools.py tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py toolsets.py
# passed

HERMES_HOME=<disposable-home> PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python - <<'PY'
# create running task, call tools.kanban_tools._handle_submit_review, assert same task enters review, then native claim_review_task claims the same id.
PY
# {"ok": true, "task_id": "t_86726e78", "review_claim_status": "running", "events": ["created", "claimed", "submitted_review", "claimed"]}

docker run --rm -i \
  -v "$PWD:/repo:ro" \
  -w /repo \
  -e HERMES_HOME=/tmp/hermes-d2c-docker-smoke \
  -e PYTHONPATH=/repo \
  hermes-17e-d3-checkpoint-smoke:py311 \
  python - <<'PY'
# read-only repo mount, disposable HERMES_HOME, no live secrets/profile DB; submit review and claim native review on same task id.
PY
# {"ok": true, "task_id": "t_a2d7d069", "run_outcome": "submitted_review", "review_claim_status": "running"}
```

### Purpose

17번째 지구 uses Kanban as a durable work bus. Worker questions, baton handoffs, review submission, request-changes, and rework must remain on the same task id so comments, events, and runs are auditable.

### Native behavior to inspect first

Before patching D2, inspect v0.16.0's native review queue/dispatcher path, including:

- `claim_review_task(...)`
- `has_spawnable_review(...)`
- review queue dispatch and review skill loading

Do not duplicate native review dispatch logic if it is sufficient. Patch only missing same-card transition behavior.

### 17번째 지구 contract

Required behavior:

1. A worker can hand the current card to another assignee without creating a replacement card.
2. A worker can submit the current card for review while preserving the original implementer.
3. A reviewer can request changes and send the same card back to the implementer/target assignee.
4. Provenance is recorded through events/outcomes, not by losing history in a new task.
5. Native v0.16 review dispatch should be used where possible instead of replacing it.

### Candidate missing surfaces to verify

- `kanban_reassign`
- `kanban_submit_review`
- `kanban_request_changes`
- DB helpers/events/outcomes for `handed_off`, `submitted_review`, `requested_changes`

### Primary files

- `hermes_cli/kanban_db.py`
- `tools/kanban_tools.py`
- `toolsets.py`
- `tests/hermes_cli/test_kanban_db.py`
- `tests/tools/test_kanban_tools.py`
- `tests/hermes_cli/test_kanban_core_functionality.py`

### Targeted smoke

```bash
python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py \
  tests/tools/test_kanban_tools.py \
  tests/hermes_cli/test_kanban_core_functionality.py
python -m py_compile \
  hermes_cli/kanban_db.py \
  tools/kanban_tools.py \
  toolsets.py
```

Manual/synthetic pass criteria:

1. Create a disposable worker task.
2. Worker comments and hands off the same card to another assignee.
3. Assignee comments and hands the same card back.
4. Worker submits the same card for review.
5. Reviewer claims review and requests changes.
6. Worker resubmits review.
7. Reviewer completes the same card.
8. One task id contains all comments/events/runs and never forks into a replacement card.

## D3 Kanban assignee alias resolution

### v0.16.0 decision

`keep-local-carry` for `17e/v0.16.0-re`.

Upstream `v2026.6.5` has native Kanban review dispatch and spawnability checks, but not the 17번째 지구 assignee-lane to spawn-profile alias seam. This commit adds only the missing dispatcher seam: durable `tasks.assignee` remains the board/audit lane, while `kanban.assignee_aliases` is resolved for spawnability checks and `_default_spawn` profile selection.

Decision evidence:

```bash
git grep -n "assignee_aliases\|resolve_assignee_profile" e895d0ecf -- hermes_cli tests
# no matches
```

### Purpose

The board-facing assignee name and the actual spawnable Hermes profile can differ. In this deployment, `wolong` can be the durable board/audit lane for Gongmyeong while the actual runnable profile is `default`.

### Config contract

```yaml
kanban:
  assignee_aliases:
    wolong: default
```

Required behavior:

1. Preserve `tasks.assignee` as the board/audit lane.
2. Resolve aliases only for dispatcher spawnability checks and `_default_spawn` profile selection.
3. Apply alias resolution to ready dispatch, review dispatch, `has_spawnable_ready`, and `has_spawnable_review`.
4. Fail closed on missing targets, cycles, or excessive alias chains.
5. Do not implement this as a plugin unless upstream provides a narrow `resolve_assignee_profile` hook; plugins are too late for dispatcher spawn decisions.

### Per-delta decision procedure

In the D3 commit, verify whether v0.16.0 has an upstream equivalent for spawn-profile aliasing. If absent, re-apply the minimal dispatcher seam. Resolve D3 after D2 review/handoff analysis because review dispatch also needs alias resolution.

### Primary files

- `hermes_cli/kanban_db.py`
- `tests/hermes_cli/test_kanban_db.py`

### Targeted smoke

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_kanban_db.py
# 217 passed

PYTHONPATH=$PWD HERMES_HOME=<disposable-home> /Users/draccoon/.local/bin/hermes-python -m hermes_cli.main kanban dispatch --dry-run --max 5 --json
# spawned task kept assignee "wolong"; skipped_nonspawnable []

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile hermes_cli/kanban_db.py tests/hermes_cli/test_kanban_db.py
# passed

git diff --check
# passed
```

Manual pass criteria:

- A task assigned to `wolong` is not bucketed as `skipped_nonspawnable` solely because the runnable profile is `default`.
- The persisted board assignee remains `wolong`.
- Alias cycle/depth-limit tests pass.

## D4 Discord gateway config and owner-thread routing seams

### Purpose

Multiple Discord bot/profile gateways can see the same server, channel, and thread. Participation must not equal ownership. Only the bot that created/owns a Discord thread should receive mention-free follow-ups in that thread.

### Generic config commits to inspect

- `0bfe19ba1 fix(gateway): merge nested gateway.platforms configuration block`
- `44f3e5186 fix(gateway): run adapter config hooks for nested-only platform blocks`
- `6d2727ef1 fix(discord): bridge explicit allow_from configuration to env var mapping`

In the D4 commit, mark these as absorbed only if verified against the release base. Do not carry duplicate config patches if upstream already includes them.

### Owner-thread contract to inspect

Required behavior:

1. Participation is not ownership.
2. A bot explicitly mentioned later in another bot's thread may participate but must not become the default mention-free responder.
3. `discord.thread_require_mention: true` remains a stronger gate.
4. `discord.auto_thread_free_response` defaults false.
5. `discord.auto_thread_free_response` / `DISCORD_AUTO_THREAD_FREE_RESPONSE` permits auto-threading from free-response command-center channels only when explicitly enabled.
6. `no_thread_channels` remains an override.

### Candidate patch surfaces

Patch these only if still missing after v0.16.0 inspection:

- `ThreadOwnerTracker` in `gateway/platforms/helpers.py`
- Discord adapter ownership marking for created/auto-created threads
- mention-free thread routing based on ownership, not participation
- `auto_thread_free_response` toggle

Do not clone or replace the whole Discord adapter as a plugin.

### Primary files

- `gateway/platforms/helpers.py`
- `plugins/platforms/discord/adapter.py`
- `tests/gateway/test_discord_channel_controls.py`
- `tests/gateway/test_discord_free_response.py`
- `tests/gateway/test_discord_thread_persistence.py`

Config regression tests may still be run for confidence if generic config behavior is inspected:

- `tests/gateway/test_config.py`

### Targeted smoke

```bash
python -m pytest -q \
  tests/gateway/test_discord_free_response.py \
  tests/gateway/test_discord_channel_controls.py \
  tests/gateway/test_discord_thread_persistence.py \
  tests/gateway/test_config.py
python -m py_compile \
  gateway/platforms/helpers.py \
  plugins/platforms/discord/adapter.py
```

Manual/live smoke only after explicit restart approval:

1. Confirm affected profile config contains `discord.auto_thread_free_response: true` only where intended.
2. Restart only affected running Discord gateways.
3. In a free-response command-center channel, send an unmentioned message and confirm the bot creates/responds in an owned thread when enabled.
4. In the created thread, confirm the owning bot can answer mention-free while another bot that was only mentioned later does not take over default routing.

## D5 Plugin strategy retirement

### Decision background

The v0.15 plugin experiment did not move actual Kanban or Discord behavior out of the local runtime branch. It only provided diagnostics, migration audit, and transition-contract support. That did not materially reduce runtime update cost.

### Current rule

- Do not depend on `kkachi-hermes-plugin` for runtime behavior.
- Do not recreate a support-only plugin for update management.
- Keep update knowledge in this ledger and in active skills/SOUL where operators will actually read it.
- A future plugin is acceptable only if it carries real behavior without broad new runtime hooks and demonstrably reduces the next update burden.

### Per-delta decision procedure

In the D5 commit, verify no active v0.16.0 plan/config depends on the retired support-only plugin. Then record the retirement decision there. Do not mark it in this baseline.

## D6 CLI return-code passthrough

### v0.16.0 decision

`keep-local-carry` for `17e/v0.16.0-re`.

The release-candidate branch still ignored integer return codes from command handlers at the top-level CLI dispatch boundary. This commit patches only the final dispatch point and uses `type(rc) is int`, not `isinstance(rc, int)`, so `True`/`False` are not converted into shell exit codes.

Pre-patch reproduction:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m hermes_cli.main kanban show definitely_missing_task
# rc 0; stderr: no such task: definitely_missing_task
```

### Observed risk to verify

The top-level CLI command dispatcher may ignore integer return codes from subcommand handlers.

Candidate smoke:

```bash
PYTHONPATH=$PWD python -m hermes_cli.main kanban show definitely_missing_task
# expected after fix: rc 1, not rc 0
```

### Required behavior if still broken

Scripts, cron jobs, CI checks, and release smoke must be able to distinguish command failure from success at the shell/process boundary.

Patch the final top-level command dispatch point only:

```python
rc = args.func(args)
if type(rc) is int:
    sys.exit(rc)
```

Do **not** use `isinstance(rc, int)`: Python `bool` is an `int` subclass, so `True` could otherwise become exit code `1` by mistake.

### Primary files

- `hermes_cli/main.py`
- targeted tests/smoke for CLI process return codes

### Targeted smoke

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m hermes_cli.main kanban show definitely_missing_task
# rc 1; stderr: no such task: definitely_missing_task

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m hermes_cli.main kanban boards switch ""
# rc 2; stderr: kanban boards switch: slug is required

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_main_exit_codes.py tests/hermes_cli/test_kanban_db.py
# 224 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile hermes_cli/main.py tests/hermes_cli/test_main_exit_codes.py
# passed

git diff --check
# passed
```

Additional unit coverage should verify that a fake command returning `True` or `False` is not converted into `SystemExit(1)` or `SystemExit(0)` by the passthrough logic.

## Current release-candidate baseline

```text
release candidate branch: 17e/v0.16.0-re
release base tag:         v2026.6.5
release base commit:      3c231eb39
ledger baseline purpose:  copy D1-D6 contracts into the release branch before per-delta code/decision commits
```

Initial preflight observations already collected, but not yet ledger-final decisions:

```text
D1: check whether original upstream commits are ancestors of v2026.6.5.
D2/D3: old local commit 576ec47d9 is not an ancestor; compare manually with v0.16 native Kanban.
D4: check whether generic config commits are ancestors; inspect owner-thread behavior separately.
D6: verify missing-task CLI smoke before patching.
```

Patch-application preflight:

```text
D2/D3 old patch may conflict in hermes_cli/kanban_db.py; manual minimal re-application is expected.
D4 old patch may conflict in plugins/platforms/discord/adapter.py; manual owner-thread-only re-application is expected.
```

## Completion gates for this release candidate

Do not mark `17e/v0.16.0-re` ready until all applicable gates are complete:

1. This ledger is committed on the release-candidate branch.
2. `17e/carry.yaml` records D1-D6 status and smoke evidence.
3. Each D1-D6 status is recorded only in its per-delta code/drop/retire commit.
4. No local D1 code patch is present unless D1 is proven not absorbed.
5. D2/D3 are either patched minimally or explicitly replaced by proven upstream-native behavior.
6. D4 has only the still-needed owner-thread seam, not duplicate absorbed config patches.
7. D5 remains a no-code/process decision unless active references require cleanup.
8. D6 CLI return-code passthrough is fixed and smoked if still broken.
9. Host targeted smoke passes for touched files.
10. Docker smoke passes with disposable `HERMES_HOME`.
11. `17e/live` repoint/apply is separately approved and verified.
