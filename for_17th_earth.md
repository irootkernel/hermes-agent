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

## Diff section: runtime deltas (D-items)

D-items are release-scoped runtime/code differences between upstream Hermes and the 17번째 지구 carry branch. Do not allocate a D-ID for a pure operating rule unless it introduces, changes, drops, or retires a runtime diff.

### Delta index for v0.16.0 / `v2026.6.5`

| ID | Change title | Baseline state | Per-delta work to do | Preflight evidence to verify |
|---|---|---|---|---|
| D1 | [Tool Search pair](#d1-tool-search-pair) | `upstream-absorbed` by `v2026.6.5` | Drop local D1 carry; do not apply Tool Search code patches on this release branch. | `git merge-base --is-ancestor` returned `0` for both `369075dc9` and `7427b9d58` against this branch. |
| D2 | [Kanban review and same-card handoff helpers](#d2-kanban-review-and-same-card-handoff-helpers) | D2-a audited: `partial-native`; D2-b/c/d/e/f applied | Keep native v0.16 review queue/dispatch; re-applied only missing same-card transition/tool seams in D2-b/c/d/e/f. | Native `review` claim/dispatch exists; `handoff_task`, `submit_task_for_review`, `request_changes`, final creator-gate routing, and async review watcher coverage were absent at D2-a audit. |
| D3 | [Kanban assignee alias resolution](#d3-kanban-assignee-alias-resolution) | `keep-local-carry` | Re-applied minimal dispatcher-only spawn-profile alias resolution. | v0.16.0 had no `kanban.assignee_aliases` / `resolve_assignee_profile` equivalent before this D3 commit. |
| D4 | [Discord gateway config and owner-thread routing seams](#d4-discord-gateway-config-and-owner-thread-routing-seams) | generic config fixes `upstream-absorbed`; owner-thread seam applied | Drop duplicate generic config carries; re-applied only owner-thread routing and `auto_thread_free_response` opt-in. | Generic config commits are ancestors; `ThreadOwnerTracker` / owner-thread seam absent before D4 patch. |
| D5 | [Plugin strategy retirement](#d5-plugin-strategy-retirement) | `retired` / no-code | Do not recreate `kkachi-hermes-plugin`; carry only this ledger/skill knowledge. | Repo audit found no active config/plan/plugin dependency outside this ledger/carry manifest. |
| D6 | [CLI return-code passthrough](#d6-cli-return-code-passthrough) | `keep-local-carry` | Applied bool-safe top-level integer return-code passthrough. | Missing Kanban task now exits `1`; usage error exits `2`; bool return values are ignored. |
| D7 | [Doctor actionable warning filter](#d7-doctor-actionable-warning-filter) | `keep-local-carry` | Applied config-scoped doctor Tool Availability output filtering. | Disabled optional toolsets are hidden from doctor warnings; selected/enabled missing toolsets still warn. |

## Rule section: operating rules (R-items)

R-items are durable 17번째 지구 operating rules that govern release activation, local profiles, skills, or other host-local state outside the release diff itself. R-items do not allocate D-IDs and must not be reported as runtime code carries.

| ID | Rule title | Scope | Activation impact | Next-release instruction |
|---|---|---|---|---|
| R1 | [Config/profile activation policy](#r1-configprofile-activation-policy) | Default/named profile configs, schema migration, `hermes config check`, `hermes doctor`, config policy values | Treat as host-local config and doctor triage activation gate, not a runtime diff. | Verify raw config versions, run approved migrations/checks, set activation policy values explicitly, and classify remaining doctor warnings before restart. |
| R2 | [Skill provenance, overrides, and compatibility policy](#r2-skill-provenance-overrides-and-compatibility-policy) | Bundled/upstream skills, optional skills, custom/local skills, hub-installed skills, profile-local skill copies, override/fork skills | Treat as host-local skill compatibility gate, not a runtime diff. R2 decides provenance/resolution/readiness, not release-specific usage-style rewriting. | Audit bundled skill removals, custom/local skill validity, duplicate names, and active cron skill references; preserve upstream originals and fork needed local variants into custom/override skills. Hand off profile-owned usage-style optimization to R5. |
| R3 | [Web dashboard and desktop activation gate](#r3-web-dashboard-and-desktop-activation-gate) | Web dashboard, dashboard API/status, dashboard frontend build, PTY/WebSocket chat surface, Hermes Desktop build/launch/logs | Treat as host-local GUI surface activation gate, not a runtime diff. | Verify dashboard and desktop surfaces from the candidate/live runtime before declaring activation ready. |
| R4 | [Cron and local automation assets activation gate](#r4-cron-and-local-automation-assets-activation-gate) | Active cron jobs, cron `skills[]`, cron scripts, `~/.hermes/scripts`, profile-local scripts, watcher jobs, hardcoded automation paths | Treat as host-local automation activation gate, not a runtime diff. R4 decides existence/syntax/resolution/governance/residuals, not release-specific usage-style rewriting. | Verify active cron jobs, script existence/syntax, profile-relative script resolution, and hardcoded path compatibility before activation. Hand off profile-owned cron/script usage-style optimization to R5. |
| R5 | [Profile-owned local asset usage-style optimization gate](#r5-profile-owned-local-asset-usage-style-optimization-gate) | 17H-owned/profile-owned custom skills, profile-local skills after owner review, 17H-owned cron prompts/jobs, canonical scripts, and workflow guidance that should adopt new Hermes native surfaces | Treat as a post-activation local-asset optimization gate, not a runtime diff and not a readiness substitute for R2/R4. | After activation, run ownership-first self-audit and optimize only 17H-owned/profile-owned skill/cron/script content for the new release's native usage style; route maintainer-managed assets to upstream/project lanes. |

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
- D2-d: request-changes/rework loop (`request_changes`, `kanban_request_changes`) plus final same-task-id synthetic smoke — applied in `17e/v0.16.0-re`.
- D2-e: creator/final gate after reviewer approval (`final_assignee` review payload and `review_accepted` same-card routing) — applied on `17e/live` after v0.16.0 activation.
- D2-f: async review watcher coverage (`kanban_submit_review` session-source auto-subscribe plus notifier delivery for `requested_changes` / `review_accepted`) — applied on `17e/live` after D2-e.
- D2-g: creator-accepted work result submission (`submit_task_result`, `kanban_submit_result`, CLI `submit-result`) — applied in this branch after D2-f.

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

Decision: `keep-local-carry` for cooperative same-card handoff/reassign. D2-c and D2-d are now applied.

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

Decision: `keep-local-carry` for same-card submit-for-review. D2-d is now applied.

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

### D2-d v0.16.0 patch decision

Decision: `keep-local-carry` for request-changes/rework loop. D2-b/c/d are now applied; native v0.16 review dispatch remains in use.

Applied local seams:

- `hermes_cli/kanban_db.py`: `request_changes(...)` closes the current review run as `requested_changes` / `released`, restores the original implementer from the latest `submitted_review` event unless an explicit target is provided, clears claim state, and returns the same task id to `ready`.
- `tools/kanban_tools.py`: `kanban_request_changes` tool surface with same-task ownership guard, stale-run guard via `HERMES_KANBAN_RUN_ID`, required reason, and worker session metadata stamping.
- `toolsets.py`: exposes `kanban_request_changes` through the Hermes CLI/kanban toolset list.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_request_changes_returns_review_to_original_implementer \
  tests/hermes_cli/test_kanban_db.py::test_request_changes_can_override_return_assignee \
  tests/hermes_cli/test_kanban_db.py::test_request_changes_rejects_stale_run_id_without_mutation \
  tests/hermes_cli/test_kanban_db.py::test_kanban_request_changes_tool_returns_current_review_task \
  tests/hermes_cli/test_kanban_db.py::test_same_task_review_request_changes_rework_complete_loop \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_env_var \
  tests/tools/test_kanban_tools.py::test_kanban_worker_env_overrides_profile_toolset_filter \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_toolset_config
# 8 passed, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_kanban_db.py
# 230 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py
# 250 passed, 1 skipped, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile hermes_cli/kanban_db.py tools/kanban_tools.py tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py toolsets.py
# passed

HERMES_HOME=<disposable-home> PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python - <<'PY'
# create one task id; submit_review -> review claim -> request_changes -> rework claim -> submit_review -> review claim -> complete.
PY
# {"ok": true, "task_id": "t_44cb7efb", "final_status": "done", "outcomes": ["submitted_review", "requested_changes", "submitted_review", "completed"]}

docker run --rm -i \
  -v "$PWD:/repo:ro" \
  -w /repo \
  -e HERMES_HOME=/tmp/hermes-d2d-docker-smoke \
  -e PYTHONPATH=/repo \
  hermes-17e-d3-checkpoint-smoke:py311 \
  python - <<'PY'
# read-only repo mount, disposable HERMES_HOME, no live secrets/profile DB; full D2-d same-task loop to done.
PY
# {"ok": true, "task_id": "t_4ae0b437", "final_status": "done", "outcomes": ["submitted_review", "requested_changes", "submitted_review", "completed"]}
```

### D2-e v0.16.0 patch decision

Decision: `keep-local-carry` for creator/final gate after reviewer approval. D2-b/c/d/e are now applied; native v0.16 review dispatch remains in use.

Applied local seams:

- `hermes_cli/kanban_db.py`: `submit_task_for_review(...)` records an optional `final_assignee` in the `submitted_review` event. Explicit reviewers and final assignees are validated as real spawnable profiles/aliases before recording; invalid review/final gates fail closed without changing task state. When omitted, a real profile-valued `created_by` different from the reviewer becomes the creator gate. `complete_task(...)` detects reviewer runs claimed from native `review` status; only on that active reviewer-approval path does it revalidate `final_assignee`. If a still-valid final gate exists, reviewer approval closes the review run as `review_accepted`, returns the same card to `ready` for the final assignee, and does **not** mark the task `done` or set `completed_at`. If a recorded final gate later becomes invalid while that reviewer approval is active, completion fails closed and leaves the review run active. Historical `submitted_review.final_assignee` payloads are not used as global completion state for later rework/non-review runs.
- `tools/kanban_tools.py`: `kanban_submit_review` accepts `final_assignee` and advertises creator/final gate semantics; `kanban_complete` returns the post-call task `status`/`assignee` so a reviewer can see that approval routed to a final gate rather than terminal completion, and reports an explicit final-gate drift error when an active reviewer approval fails because the recorded final assignee no longer resolves.
- `hermes_cli/kanban.py`: CLI completion prints a routed-review message when completion leaves the task non-`done`, and names active final-gate drift instead of collapsing it into the generic terminal/unknown completion error.
- `tests/hermes_cli/test_kanban_db.py`: regression tests cover reviewer approval routing to creator gate, final creator completion on the same task id, invalid explicit reviewer/final gate rejection, tool-level invalid reviewer errors, route-time final gate re-validation, stale final-gate payloads after `request_changes`/rework, and worker-facing active final-gate drift errors.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_review_approval_routes_to_creator_final_gate \
  tests/hermes_cli/test_kanban_db.py::test_review_approval_rejects_final_gate_that_became_invalid \
  tests/hermes_cli/test_kanban_db.py::test_stale_review_final_gate_does_not_wedge_rework_completion \
  tests/hermes_cli/test_kanban_db.py::test_kanban_complete_tool_reports_invalid_active_final_gate \
  tests/hermes_cli/test_kanban_db.py::test_same_task_review_request_changes_rework_complete_loop \
  tests/tools/test_kanban_tools.py::test_complete_happy_path
# 6 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/hermes_cli/test_kanban_db.py
# 237 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py
# 250 passed, 1 skipped, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  hermes_cli/kanban_db.py \
  hermes_cli/kanban.py \
  tools/kanban_tools.py \
  tests/hermes_cli/test_kanban_db.py
# passed

git diff --check -- hermes_cli/kanban_db.py tools/kanban_tools.py hermes_cli/kanban.py tests/hermes_cli/test_kanban_db.py for_17th_earth.md
# passed
```

### D2-f v0.16.0 patch decision

Decision: `keep-local-carry` for async review watcher coverage. D2-b/c/d/e/f are now applied; native v0.16 review dispatch remains in use.

Applied local seams:

- `tools/kanban_tools.py`: `kanban_submit_review` now attaches an idempotent notification subscription when a gateway/session source is available (`HERMES_SESSION_PLATFORM` + `HERMES_SESSION_CHAT_ID`, with thread/user/profile metadata when present). CLI/cron/local runs without a messaging source preserve the previous no-subscription behavior. Successful tool output includes a compact `review_watch` receipt when a watcher was attached.
- `gateway/run.py`: the Kanban notifier watches review outcome events in addition to terminal/blocked worker events: `requested_changes` notifies the originating chat that rework is required, and `review_accepted` notifies that reviewer approval routed to the creator/final gate rather than silently waiting. Subscriptions still retire only on truly terminal task state (`done` / `archived`), so request-changes and creator-gate routing keep the watcher alive for the later final outcome.
- `tests/hermes_cli/test_kanban_db.py`: regression coverage proves `kanban_submit_review` creates the session-source subscription and returns the `review_watch` receipt.
- `tests/gateway/test_kanban_notifier.py`: regression coverage proves subscribed async review waiters receive `requested_changes` and `review_accepted` messages.

Review note:

- Samaui review card `t_034347d9`: `SAMAUI_ACCEPT / STRATEGIC_RED_ACCEPT_WITH_RISK` for D2-f release scope. No mandatory D2-f fixes requested. Non-blocking risk: late-created subscriptions currently seed from `last_event_id=0`, so old watched events can replay to a newly subscribed origin; track as R4/notifier-hardening follow-up for a late-subscribe cursor-seeding mode and regression coverage.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_kanban_submit_review_tool_auto_subscribes_session_source \
  tests/gateway/test_kanban_notifier.py::test_notifier_delivers_review_request_changes \
  tests/gateway/test_kanban_notifier.py::test_notifier_delivers_review_accepted_final_gate
# 3 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/gateway/test_kanban_notifier.py \
  tests/hermes_cli/test_kanban_db.py::test_kanban_submit_review_tool_submits_current_worker_task \
  tests/hermes_cli/test_kanban_db.py::test_kanban_submit_review_tool_auto_subscribes_session_source \
  tests/hermes_cli/test_kanban_db.py::test_request_changes_returns_review_to_original_implementer \
  tests/hermes_cli/test_kanban_db.py::test_review_approval_routes_to_creator_final_gate \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_env_var \
  tests/tools/test_kanban_tools.py::test_kanban_worker_env_overrides_profile_toolset_filter \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_toolset_config
# 15 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py \
  tests/tools/test_kanban_tools.py \
  tests/hermes_cli/test_kanban_core_functionality.py \
  tests/gateway/test_kanban_notifier.py
# 496 passed, 1 skipped

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  tools/kanban_tools.py \
  gateway/run.py \
  tests/hermes_cli/test_kanban_db.py \
  tests/gateway/test_kanban_notifier.py
# passed

git diff --check -- tools/kanban_tools.py gateway/run.py tests/hermes_cli/test_kanban_db.py tests/gateway/test_kanban_notifier.py for_17th_earth.md
# passed
```

### D2-g v0.16.0 patch decision

Decision: `keep-local-carry` for creator-accepted work result submission. D2-b/c/d/e/f/g are now applied; native v0.16 review dispatch remains in use.

Applied local seams:

- `hermes_cli/kanban_db.py`: `submit_task_result(...)` closes the current worker run as `submitted_result` / `released`, records a `submitted_result` event with the original worker (`from_assignee`) and acceptor (`reviewer`), clears claim state, and moves the same task id into native `review` status for creator/acceptor approval. It intentionally does not write `final_assignee`, so the acceptor's `complete_task(...)` is terminal instead of being routed through the D2-e creator/final gate.
- `request_changes(...)`: latest-submission provenance now considers both `submitted_review` and `submitted_result`, so acceptors can return result submissions to the original worker on the same card.
- `tools/kanban_tools.py`: `kanban_submit_result` worker/orchestrator tool surface with same-task ownership guard, stale-run guard via `HERMES_KANBAN_RUN_ID`, worker session metadata stamping, and the same session-source watcher attachment behavior as review submission.
- `hermes_cli/kanban.py`: CLI `submit-result <task_id> --reviewer <profile> --summary ... [--metadata JSON]` for operator/manual acceptance routing.
- `toolsets.py` and tool visibility tests expose `kanban_submit_result`; `agent/prompt_builder.py` tells workers when to choose `kanban_complete`, `kanban_submit_result`, or `kanban_submit_review` while keeping the Kanban guidance under the existing prompt-size guard.

Review note:

- Samaui review card `t_9152144c`: `SAMAUI_ACCEPT / STRATEGIC_RED_ACCEPT_WITH_RISK` for D2-g release scope. No mandatory fixes requested. Non-blocking risks noted: add explicit negative coverage for invalid reviewer / missing creator / stale run, and add an explicit notifier regression for `kanban_submit_result` in a later hardening pass if D2-g remains long-lived local carry.

Smoke evidence:

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py::test_submit_task_result_routes_to_creator_acceptance_without_final_gate \
  tests/hermes_cli/test_kanban_db.py::test_request_changes_returns_result_submission_to_worker \
  tests/hermes_cli/test_kanban_db.py::test_kanban_submit_result_tool_submits_current_worker_result \
  tests/hermes_cli/test_kanban_cli.py::test_run_slash_submit_result_routes_to_creator_acceptance \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_env_var \
  tests/tools/test_kanban_tools.py::test_kanban_worker_env_overrides_profile_toolset_filter \
  tests/tools/test_kanban_tools.py::test_kanban_tools_visible_with_toolset_config
# 7 passed, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py \
  tests/hermes_cli/test_kanban_cli.py \
  tests/tools/test_kanban_tools.py \
  tests/hermes_cli/test_kanban_core_functionality.py
# 539 passed, 1 skipped, 1 warning

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  hermes_cli/kanban_db.py \
  hermes_cli/kanban.py \
  tools/kanban_tools.py \
  tests/hermes_cli/test_kanban_db.py \
  tests/hermes_cli/test_kanban_cli.py \
  tests/tools/test_kanban_tools.py \
  toolsets.py \
  agent/prompt_builder.py
# passed

git diff --check
# passed

HERMES_HOME=<disposable-home> PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python - <<'PY'
# submit_result -> creator review -> request_changes -> worker rework -> submit_result -> creator complete on one task id.
PY
# {"task_id": "t_3ee697ce", "after_first_submit": {"status": "review", "assignee": "creator"}, "after_changes": {"status": "ready", "assignee": "worker"}, "final": {"status": "done", "assignee": "creator", "result": "accepted"}, "outcomes": ["submitted_result", "requested_changes", "submitted_result", "completed"]}
```

### Purpose

17번째 지구 uses Kanban as a durable work bus. Worker questions, baton handoffs, review submission, request-changes, review acceptance/final-gate routing, and rework must remain on the same task id so comments, events, runs, and async notifications are auditable.

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
6. When a creator/final gate is recorded, reviewer approval must not be terminal `done`; the same card must route back to the final assignee and only the final assignee's completion closes the task.
7. When review completion may be asynchronous, review submission must attach or preserve a watcher/notification path so `requested_changes`, `review_accepted`, and final completion return to the originating chat without manual polling.
8. A worker can submit a non-review work/research result to the creator/acceptor on the same card without invoking the D2-e final-gate path; the acceptor either completes the same card or returns it with `request_changes`.

### Candidate missing surfaces to verify

- `kanban_reassign`
- `kanban_submit_review`
- `kanban_submit_result`
- `kanban_request_changes`
- DB helpers/events/outcomes for `handed_off`, `submitted_review`, `requested_changes`, `review_accepted`
- gateway notifier subscription coverage for review outcome events

### Primary files

- `hermes_cli/kanban_db.py`
- `hermes_cli/kanban.py`
- `tools/kanban_tools.py`
- `toolsets.py`
- `agent/prompt_builder.py`
- `gateway/run.py`
- `tests/hermes_cli/test_kanban_db.py`
- `tests/hermes_cli/test_kanban_cli.py`
- `tests/tools/test_kanban_tools.py`
- `tests/gateway/test_kanban_notifier.py`
- `tests/hermes_cli/test_kanban_core_functionality.py`

### Targeted smoke

```bash
python -m pytest -q \
  tests/hermes_cli/test_kanban_db.py \
  tests/tools/test_kanban_tools.py \
  tests/hermes_cli/test_kanban_core_functionality.py \
  tests/gateway/test_kanban_notifier.py
python -m py_compile \
  hermes_cli/kanban_db.py \
  tools/kanban_tools.py \
  toolsets.py \
  gateway/run.py
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

### D4 v0.16.0 patch decision

Decision: `partial-native-local-minimized-owner-thread-applied`.

Generic config carries are `upstream-absorbed` by this release branch, so do not re-apply duplicate patches for:

- `0bfe19ba1 fix(gateway): merge nested gateway.platforms configuration block`
- `44f3e5186 fix(gateway): run adapter config hooks for nested-only platform blocks`
- `6d2727ef1 fix(discord): bridge explicit allow_from configuration to env var mapping`

Absorption evidence:

```bash
git merge-base --is-ancestor 0bfe19ba1 HEAD  # rc 0
git merge-base --is-ancestor 44f3e5186 HEAD  # rc 0
git merge-base --is-ancestor 6d2727ef1 HEAD  # rc 0
```

Owner-thread routing remained a 17번째 지구 local seam before this D4 patch:

```bash
git grep -n "ThreadOwnerTracker\|auto_thread_free_response\|_is_owned_discord_thread" HEAD -- gateway plugins tests
# no matches before D4 patch
```

Applied local seams:

1. `ThreadOwnerTracker` in `gateway/platforms/helpers.py` persists Discord thread owner/default-responder mapping separately from participation.
2. Discord slash-created and auto-created threads mark both participation and ownership.
3. Mention-free thread routing uses ownership, not participation; a bot mentioned later inside another bot's thread may participate but does not take over default routing.
4. `discord.thread_require_mention: true` remains a stronger gate for every threaded message.
5. `discord.auto_thread_free_response` / `DISCORD_AUTO_THREAD_FREE_RESPONSE` defaults false and opt-in permits auto-threading from free-response command-center channels.
6. `no_thread_channels` remains an override.

Do not clone or replace the whole Discord adapter as a plugin.

### Release-candidate smoke

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest -q \
  tests/gateway/test_discord_free_response.py \
  tests/gateway/test_discord_channel_controls.py \
  tests/gateway/test_discord_thread_persistence.py \
  tests/gateway/test_config.py
# 119 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m py_compile \
  gateway/platforms/helpers.py \
  plugins/platforms/discord/adapter.py \
  tests/gateway/test_discord_free_response.py \
  tests/gateway/test_discord_channel_controls.py \
  tests/gateway/test_discord_thread_persistence.py
# passed

# Docker/read-only repo + disposable HERMES_HOME smoke:
# owned thread accepted; foreign-owned participated thread rejected;
# free-response auto-thread opt-in created an owned thread.
```

### Primary files

- `gateway/platforms/helpers.py`
- `plugins/platforms/discord/adapter.py`
- `tests/gateway/test_discord_channel_controls.py`
- `tests/gateway/test_discord_free_response.py`
- `tests/gateway/test_discord_thread_persistence.py`
- `tests/gateway/test_config.py`

Manual/live smoke only after explicit restart approval:

1. Confirm affected profile config contains `discord.auto_thread_free_response: true` only where intended.
2. Restart only affected running Discord gateways.
3. In a free-response command-center channel, send an unmentioned message and confirm the bot creates/responds in an owned thread when enabled.
4. In the created thread, confirm the owning bot can answer mention-free while another bot that was only mentioned later does not take over default routing.

## D5 Plugin strategy retirement

### v0.16.0 decision

Decision: `retired` / no-code.

Do not recreate `kkachi-hermes-plugin` or any support-only update-management plugin for this release branch. The v0.15 experiment only provided diagnostics, migration audit, and transition-contract support; it did not carry runtime Kanban or Discord behavior and did not reduce the v0.16.0 update cost enough to justify preserving a separate plugin.

No product-code patch is required. Operational knowledge stays in this ledger and the `release-carry-ledgers` skill.

Audit evidence:

```bash
git grep -n "kkachi-hermes-plugin" -- . ':!for_17th_earth.md' ':!17e/carry.yaml'
# no matches outside ledger/carry manifest

git grep -n "support-only plugin\|transition-contract\|migration audit" -- . ':!for_17th_earth.md' ':!17e/carry.yaml'
# no matches

git grep -n "kkachi\|17th.*plugin\|plugins:.*kkachi\|kkachi-hermes" -- '*.yaml' '*.yml' '*.toml' '*.json' ':!17e/carry.yaml'
# no matches

git ls-files | grep -Ei '(^|/)17e|kkachi|plugin' | grep -Ei 'kkachi|17e/.+plugin|plugin.+17e'
# no matches
```

Docker/read-only audit used the same repository-only dependency checks with a disposable `HERMES_HOME`; no live secrets, live profile config, production Kanban DB, or gateways were mounted.

### Current rule

- Do not depend on `kkachi-hermes-plugin` for runtime behavior.
- Do not recreate a support-only plugin for update management.
- Keep update knowledge in this ledger and in active skills/SOUL where operators will actually read it.
- A future plugin is acceptable only if it carries real behavior without broad new runtime hooks and demonstrably reduces the next update burden.

### Next-release instruction

Re-check for active references to `kkachi-hermes-plugin` or any successor support-only update plugin. If no runtime behavior depends on it, keep D5 retired and do not add product-code patches.

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

## D7 Doctor actionable warning filter

### v0.16.0 decision

`keep-local-carry` for `17e/v0.16.0-re`.

R1 established that activation should not add unused provider/tool API keys solely to silence doctor output. Product code still printed Tool Availability warnings for every registered optional toolset, including default-off or unselected integrations, so D7 narrows doctor output to the toolsets selected/enabled by the active config.

The filter is fail-open: if config/toolset resolution fails, doctor preserves the previous unfiltered output instead of hiding diagnostics.

### Applied local seams

- `hermes_cli/doctor.py`: add `_doctor_enabled_toolsets_for_warning_scope()` and `_filter_doctor_tool_availability_for_config(...)`.
- `hermes_cli/doctor.py`: apply the config filter after runtime-gated doctor overrides and before printing Tool Availability rows or appending the generic missing-API-key setup issue.
- `tests/hermes_cli/test_doctor.py`: cover both disabled optional toolsets and explicitly selected optional toolsets.

### Targeted smoke

```bash
PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest tests/hermes_cli/test_doctor.py::TestDoctorToolAvailabilityConfigFilter -q
# 2 passed

PYTHONPATH=$PWD /Users/draccoon/.local/bin/hermes-python -m pytest tests/hermes_cli/test_doctor.py tests/hermes_cli/test_doctor_dedicated_provider_skip.py -q
# 67 passed, 1 warning

docker run --rm -i \
  -v "$PWD:/repo:ro" \
  -w /repo \
  -e HERMES_HOME=/tmp/hermes-d7-docker-smoke \
  -e PYTHONPATH=/repo \
  hermes-17e-d3-checkpoint-smoke:py311 \
  python - <<'PY'
# stub dotenv only, import candidate doctor.py from read-only repo, and assert
# disabled optional toolsets are hidden while selected optional toolsets remain.
PY
# {'ok': True, 'available': ['web'], 'unavailable': [{'name': 'x_search', 'missing_vars': ['XAI_API_KEY'], 'tools': ['x_search']}]}
```

### Next-release instruction

Re-check whether upstream doctor now scopes Tool Availability warnings to configured toolsets. If upstream absorbs equivalent behavior, mark D7 `upstream-absorbed`; otherwise keep the smallest filter seam and preserve fail-open behavior.

## R1 Config/profile activation policy

### Rule

Config/profile readiness is the first 17번째 지구 activation operating rule. It governs default and named profile `config.yaml` files, raw `_config_version`, profile migration, `hermes config check`, `hermes doctor`, doctor warning triage, and explicit config policy values such as `curator.prune_builtins`.

Treat config/profile work as a host-local activation gate unless product code must change. Do not allocate a D-item for config migration/readiness alone.

During the approved activation window:

1. Back up default and named-profile configs before mutation.
2. Verify raw `_config_version` against the candidate runtime's `DEFAULT_CONFIG['_config_version']`.
3. Run `hermes config migrate` for the default profile and `hermes --profile <name> config migrate` for active named profiles.
4. Re-run `hermes config check` and `hermes doctor` before restarting gateways.
5. Classify every remaining doctor warning as `actionable`, `optional-unused`, or `stale-local-state`.
6. Treat actionable warnings as activation blockers unless the owner explicitly accepts the risk.
7. Do not add unused provider/tool API keys solely to silence optional doctor output; disable unused features or classify them as optional-unused.
8. Set policy-bearing config values explicitly rather than relying on stale defaults.

### Current local activation note

Read-only config audit on `17e/v0.16.0-re` observed every default/named profile at `_config_version: 27`, but all 43 checked profile configs currently have `curator.prune_builtins: true`. That is host-local activation state, not a release diff. Before live activation, back up configs and set the intended policy explicitly for active profiles.

D7 now narrows Tool Availability output so disabled/unselected optional toolsets do not create doctor warnings or the generic missing-API-key setup issue. Remaining doctor warnings still require R1 classification before restart: actionable, optional-unused, or stale-local-state.

### Next-release instruction

Re-check config schema/version, migration behavior, profile-level policy values, and doctor warning classification before activation. Keep config/profile readiness and doctor triage under R1 or a successor R-item unless a product-code change is actually required.

## R2 Skill provenance, overrides, and compatibility policy

### Rule

Skill assets are not 17번째 지구 runtime diffs by themselves. Preserve upstream bundled skill originals as upstream-owned artifacts; do not mutate bundled copies to encode local operating preference. Treat custom/local skills, hub-installed skills, profile-local copies, and explicit override/fork skills as host-local compatibility assets that must be checked before activation.

Local 17번째 지구 skill behavior should be represented as one of:

- a custom/local skill with its own provenance, or
- an explicit override/extension layer that applies on top of the bundled original without changing the upstream copy.

During activation/local-assets audit:

1. If a future upstream release removes a bundled skill, do not recreate it as a D-item product-code carry.
2. If the removed bundled skill is unused and unmodified, remove the local copy or let the official sync/repair path retire it.
3. If the removed bundled skill is actively used or locally modified, fork the needed behavior into a custom skill before removing the upstream-tracked copy.
4. If an official optional skill replaces the removed bundled skill, install/repair it profile-locally through the official skill path instead of preserving a stale bundled copy.
5. Check every runtime-visible local/custom/profile skill `SKILL.md` for valid frontmatter, name consistency, and duplicate runtime-visible skill names.
6. Check that every active cron `skills[]` entry resolves in the profile that will run the cron job; unresolved active cron skill references are activation blockers unless explicitly retired or accepted.

### Current local activation note

Read-only skill audit comparing the pre-update live/freeze commit to `v2026.6.5` found 16 bundled skills removed from `skills/`; 9 have same-slug `optional-skills/` replacements and active cron `skills[]` references to removed bundled slugs were not observed. Profile-local stale copies still require activation-time classification.

Follow-up read-only local-assets audit on the default plus named profiles observed runtime-visible skill frontmatter errors `0` and runtime-visible duplicate skill profiles `0`. This does not replace activation-time skill update/repair decisions; it only records that the current visible skill inventory parses cleanly.

R2 intentionally stops at provenance, resolver/readiness, frontmatter, duplicate-name, and upstream/override/fork decisions. Release-specific rewriting of profile-owned/custom skill content for new native Hermes usage patterns belongs to R5, even when the asset being optimized is a skill.

### Next-release instruction

Re-check bundled and optional skill movement between the previous live release and the new upstream tag. Also re-check custom/local/hub/profile skill frontmatter, duplicate runtime-visible skill names, and active cron `skills[]` resolution. Keep bundled skill provenance, optional repair/install, curator effects on skills, and local skill fork/override decisions under R2 or a successor R-item. After R2 establishes ownership/resolution boundaries, run R5 for profile-owned usage-style optimization instead of folding that work into R2.

## R3 Web dashboard and desktop activation gate

### Rule

Web dashboard and Hermes Desktop readiness are host-local activation surfaces, not release-scoped runtime diffs. They must be verified from the candidate/live runtime before declaring `17e/live` production-ready because CLI, gateway, dashboard, and desktop can fail independently after a release upgrade.

Treat R3 as an activation gate unless product code must change. Do not allocate a D-item for dashboard/desktop smoke alone.

During the approved activation window:

1. Start the dashboard from the candidate/live runtime with a safe local bind, for example `hermes dashboard --no-open --host 127.0.0.1 --port <temp>`.
2. Verify `GET /api/status` over HTTP and record the response shape/status without exposing secrets.
3. Verify the dashboard frontend is present or successfully built from the candidate checkout (`hermes_cli/web_dist` or equivalent build artifact).
4. Verify the chat surface prerequisites for PTY/WebSocket use where in scope (`ptyprocess`, Node.js, and `/api/pty` or `/api/ws` readiness), without sending live secrets through the smoke.
5. Build Hermes Desktop at least once for the candidate checkout (`hermes desktop --build-only` or equivalent packaged Electron build path) unless the owner explicitly excludes desktop from this activation.
6. If a launch smoke is run, inspect `~/.hermes/logs/desktop.log` and `~/.hermes/logs/gui.log` for errors from the same retry window.
7. Distinguish dashboard backend readiness from gateway readiness; messaging gateway restart/status remains a separate activation check.

### Current local activation note

Dashboard and desktop smoke has not yet been run for `17e/v0.16.0-re` in this R3 update. Existing release-carry guidance already treats GUI surface verification as a live activation gate after config migration and before declaring production-ready.

### Next-release instruction

Re-check dashboard server startup, `/api/status`, frontend build artifacts, PTY/WebSocket chat readiness, and desktop build/launch/log evidence for every future release activation. Keep GUI surface verification under R3 or a successor R-item unless a product-code change is actually required.

## R4 Cron and local automation assets activation gate

### Rule

Cron jobs, watcher jobs, `~/.hermes/scripts`, profile-local scripts, the shared 17번째 지구 automation script root, and cron prompt automation are host-local activation assets, not release-scoped runtime diffs. They can still break or create side effects immediately after activation, so they must be verified before declaring the release ready.

Treat R4 as an activation gate unless product code must change. Do not allocate a D-item for cron/script readiness alone.

During the approved activation window:

1. List active cron jobs for the default profile and every named profile that will remain active after activation.
2. Verify every active cron `skills[]` entry resolves in that cron job's execution profile.
3. Verify every active cron `script` exists. For the default profile, relative script paths resolve under `~/.hermes/scripts/`; for named profiles, check that profile's own `scripts/` before falling back to the default profile script directory. Also verify shared 17번째 지구 automation scripts referenced from cron prompts or wrappers under `/Users/draccoon/Workspace/Hermes/ops/scripts/`.
4. Parse every Python script with `ast.parse` or an equivalent no-write syntax check; in read-only Docker, avoid `py_compile` because `__pycache__` writes can create false failures.
5. Run `bash -n` on every shell script used by active cron/local automation.
6. Classify hardcoded checkout, Python, workdir, and vault paths in active scripts/prompts as `active-blocker`, `benign-after-in-place-activation`, or `stale-watcher-warning`.
7. Explicitly retire or pause stale watchers before activation instead of letting them fail under the new runtime.
8. Keep cron/script readiness separate from R2 skill provenance and from product-code D-items.

### Current local activation note

Read-only local-assets audit observed 20 cron jobs total, 17 active, 2 cron `skills[]` references, no missing active cron scripts, 71 Python scripts with parse errors `0`, and 26 shell scripts with `bash -n` failures `0`. The observed cron-owning profiles were `default`, `hwangchung`, `masok`, `mibang`, `songeon`, `wangpyeong`, and `wolyeong`.

Post-activation R4 residual cleanup on 2026-06-08 classified the script-governance residual 18 findings without deleting watcher/helper files:

- `cron_mibang_weekly_17thhermes_retention_cleanup.sh` is a thin wrapper through `hermes-python` into `/Users/draccoon/Workspace/Hermes/ops/scripts/`, not root-owned business logic; the audit now recognizes that marker.
- 16 inactive residual watcher/helper files are exact path+hash baselined under `allowed_runtime_residuals`; changed hashes still become violations via `changed-allowed-runtime-residual`.
- `allowed_runtime_residual()` and the top-level `audit()` loop fail closed on missing, empty, malformed, or uppercase hashes via `invalid-allowed-runtime-residual`; only non-empty lowercase 64-hex exact matches can suppress a residual.
- 7 Hwangchung/Kkachi watcher files are `project-maintainer-follow`; all referenced cards are terminal, but 17H R4 does not rewrite/delete them directly.
- 8 stale watcher residuals and 1 stale one-shot activation helper remain kept by exact hash until owner-approved removal/quarantine.

Current R4 evidence:

```bash
SMOKE_TEST=1 /Users/draccoon/.local/bin/hermes-python /Users/draccoon/Workspace/Hermes/ops/scripts/shared/governance/audit_script_governance.py --details
# OK_SCRIPT_GOVERNANCE_AUDIT violations=0 runtime_files=73 cron_scripts=16

/Users/draccoon/.local/bin/hermes-python -m py_compile /Users/draccoon/Workspace/Hermes/ops/scripts/shared/governance/audit_script_governance.py
# pass

/Users/draccoon/.local/bin/hermes-python -m json.tool /Users/draccoon/Workspace/Hermes/ops/scripts/shared/governance/script_governance_baseline.json >/dev/null
# pass

# Runtime/profile Python syntax check: {'python_scripts_checked': 25, 'syntax_failures': []}
# Runtime/profile/ops shell syntax check: {'shell_scripts_checked': 34, 'failure_count': 0}
# Direct helper fail-close regression probe: OK_ALLOWED_RUNTIME_RESIDUAL_FAIL_CLOSED
# Full audit fail-close regression probe: OK_R4_INVALID_ALLOWED_RESIDUAL_AUDIT_FAIL_CLOSED
```

Receipt: `/Users/draccoon/Workspace/Hermes/ops/scripts/inventory/2026-06-08-r4-script-governance-residual-cleanup-receipt.md`.
Ops/workspace commit: `7ac4322 chore(governance): [R4] fail-close script residual allowlist`.

Shared 17번째 지구 automation scripts are currently under `/Users/draccoon/Workspace/Hermes/ops/scripts/`; `/Users/draccoon/Workspace/Hermes/opt/` was checked and was not present in this snapshot. Treat cron wrappers in `~/.hermes/scripts/` and profile-local `scripts/` as runtime entrypoints, and the shared `ops/scripts/` tree as the durable common script source where applicable.

This audit is a readiness snapshot only. Before live activation, re-run it against the candidate/live runtime and explicitly classify stale watchers, disabled jobs, hardcoded paths, and any KSCQ/KAC/retention/diary jobs that should be kept, paused, or retired.

### Next-release instruction

Re-check active cron jobs, cron `skills[]`, cron scripts, profile-local script resolution, shared `/Users/draccoon/Workspace/Hermes/ops/scripts/` references, script syntax, hardcoded paths, and watcher retirement state for every future release activation. Keep cron/script/local automation readiness under R4 or a successor R-item unless a product-code change is actually required. After R4 establishes existence/syntax/resolution/governance boundaries, run R5 for profile-owned cron prompt/script usage-style optimization instead of folding that work into R4.

## R5 Profile-owned local asset usage-style optimization gate

### Rule

R5 is the post-activation optimization gate for 17번째 지구 profile-owned local assets after a Hermes runtime release changes native usage style. It covers whether locally owned skills, cron prompts/jobs, and canonical scripts should be rewritten to use the new release's native surfaces and operating semantics more directly.

Treat R5 as a local asset optimization gate, not a runtime diff and not a replacement for R2/R4 readiness:

- R2 remains the provenance/resolver/readiness gate for skills: bundled vs optional vs custom vs hub vs profile-local, frontmatter, duplicate names, resolver visibility, upstream-follow, override/fork decisions, and active cron `skills[]` resolution.
- R4 remains the readiness/governance gate for cron/scripts/watchers: job inventory, script existence, syntax, path resolution, stale watcher classification, residual allowlists, and local automation health.
- R5 starts only after R2/R4 have established ownership and safety boundaries. It may modify 17H-owned/profile-owned content, but it must not mutate bundled/upstream/vendor/external-maintainer/project-maintainer assets as if they were 17H-owned.

During R5:

1. Preserve the Korean source command as SOT and create an English operational brief for worker/reviewer routing.
2. Build an ownership-first inventory across runtime-visible local/custom/profile skills, 17H-owned cron prompts/jobs, and 17H-owned canonical scripts.
3. Classify each asset before editing: `17h-owned-custom`, `17h-profile-local`, `17h-cron-prompt`, `17h-canonical-script`, `runtime-wrapper`, `upstream-bundled-follow`, `vendor-or-hub-follow`, `external-maintainer-follow`, `project-maintainer-follow`, or `unknown-owner-defer`.
4. Optimize only 17H-owned/profile-owned assets for the target release's native surfaces. For v0.16 this includes Kanban `parents`, native review/claim flow, same-card handoff/reassign/request-changes seams, `goal_mode`, sticky blocks for external waits, notify subscriptions/bounded watchers, creator-final gates, and fail-closed backstops.
5. Keep copied-skill dedup/governance separate from content optimization. Shared `skills.external_dirs` rollout and `.no-bundled-skills` reseed prevention prove resolver parity; they do not prove content has been rewritten for the new release.
6. Do not edit Kkachi-family KAS/KAH/KAN/Kkachi or other project-maintainer assets under 17H authority. Route them to their maintainer lane or record upstream/project feedback.
7. Validate with separate evidence surfaces: skill/frontmatter/governance audit, resolver smoke for load-bearing skills, cron JSON/prompt/script checks, script syntax/regression harness, and targeted workflow smoke if behavior changed.
8. Use Kanban review with 사마의 for strategic risk and record 공명/creator final gate separately. Reviewer `done` is not final acceptance.

### Current local activation note

The v0.16.0 R5 first pass was completed on 2026-06-08 after shared skill-root dedup/governance stabilization:

- Inventory/queue: `/Users/draccoon/Workspace/Hermes/ops/skills/_governance/v016-skill-content-optimization-queue-20260608-045637.md`.
- Ownership boundary reference: `/Users/draccoon/Workspace/Hermes/ops/skills/dogfood/hermes-17e-update/references/17e-v016-skill-content-optimization-ownership-boundary-2026-06.md`.
- Postpatch receipt: `/Users/draccoon/Workspace/Hermes/ops/skills/_governance/v016-skill-content-optimization-postpatch-receipt-20260608-050300.md`.
- Postpatch inventory: `/Users/draccoon/Workspace/Hermes/ops/skills/_governance/v016-skill-content-optimization-postpatch-inventory-20260608-050300.json`.
- First-pass scope: 12 files patched from the 17H-owned queue: 7 skills, 4 scripts, and 1 cron prompt/job surface. Bundled/vendor/hub/external-maintainer/project-maintainer assets were excluded or routed to their owner lanes.
- Verification evidence: skill governance `status=ok`, `violation_count=0`; focused frontmatter checks passed; script `py_compile` passed; watcher/backstop regression harness `4/4 OK`; cron JSON parse passed; resolver smoke passed for representative shared and profile-local exception skills.
- Review evidence: Samaui review card `t_8f56abcf` reached `STRATEGIC_RED_ACCEPT_WITH_RISK / STRATEGIC_ACCEPT / SAMAUI_ACCEPT` after request-changes fixes, and 공명 recorded creator-gate acceptance. Script-governance residuals discovered during the pass were split to R4 and later closed through R4 review.
- Evidence precedence: if the initial queue and the postpatch receipt/inventory diverge, treat the postpatch receipt, postpatch inventory, final Samaui review, and 공명 creator gate as the final R5 completion evidence. The queue is planning/input evidence, not the final acceptance record.

### Next-release instruction

For every future Hermes runtime release, run R5 after R2/R4 establish ownership/readiness boundaries and after the live/candidate runtime surface is known. Rebuild the ownership-first inventory, optimize only 17H-owned/profile-owned skill/cron/script content for the new native usage style, preserve maintainer boundaries, validate with separate skill/cron/script evidence surfaces, and require 사마의 review plus 공명 creator gate before declaring the R5 pass complete.

## Current release-candidate baseline

```text
release candidate branch: 17e/v0.16.0-re
release base tag:         v2026.6.5
release base commit:      3c231eb39
ledger baseline purpose:  copy D1-D7 runtime-diff contracts plus R1/R2/R3/R4 operating-rule contracts into the release branch before per-delta code/decision commits
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
2. `17e/carry.yaml` records D1-D7 status/smoke evidence and R1/R2/R3/R4 operating-rule metadata separately from runtime diffs.
3. Each D1-D7 status is recorded only in its per-delta code/drop/retire commit.
4. R1/R2/R3/R4 are treated as operating-rule/activation policies, not as product-code carries.
5. No local D1 code patch is present unless D1 is proven not absorbed.
6. D2/D3 are either patched minimally or explicitly replaced by proven upstream-native behavior.
7. D4 has only the still-needed owner-thread seam, not duplicate absorbed config patches.
8. D5 remains a no-code/process decision unless active references require cleanup.
9. D6 CLI return-code passthrough is fixed and smoked if still broken.
10. Host targeted smoke passes for touched files.
11. Docker smoke passes with disposable `HERMES_HOME`.
12. `17e/live` repoint/apply is separately approved and verified.
