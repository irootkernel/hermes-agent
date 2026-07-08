# Root Kernel Hermes Agent v0.17.0 carry log

## Baseline

- Upstream release: Hermes Agent `v0.17.0` / tag `v2026.6.19`
- Upstream commit: `2bd1977d8fad185c9b4be47884f7e87f1add0ce3`
- Candidate branch: `rk/v0.17.0`
- Previous downstream branch: `rk/v0.16.0`
- Previous downstream commit/tag: `c3c60ccb192526b0f459a1a6bc198dd1b9f0f554` / `rk/tag/v0.16.0`
- Release note evidence: `root-kernel/evidence/release-note-v2026.6.19.md`
- Goal: run Root Kernel on v0.17.0 while absorbing upstream features first and retaining only minimal Root Kernel-specific fail-closed/runtime seams.

## Namespace migration

Executed before D6 code carry application, after the company/project rename to Root Kernel:

- Local rollback refs created:
  - `backup/rk-namespace-migration-before-rename-20260620-183211` -> `2bd1977d8fad185c9b4be47884f7e87f1add0ce3`
  - `backup/rk-v0.16.0-before-rename-20260620-183211` -> `c3c60ccb192526b0f459a1a6bc198dd1b9f0f554`
- Local branches renamed without commit rewrite:
  - `17e/v0.16.0` -> `rk/v0.16.0`
  - `17e/v0.17.0` -> `rk/v0.17.0`
- Local tag renamed by create/delete:
  - `17e/tag/v0.16.0` -> `rk/tag/v0.16.0`
- Local release artifacts renamed:
  - `17e/` -> `root-kernel/`
  - `for_17th_earth.md` -> `for-root-kernel.md`
- Remote refs were not pushed or deleted in this step.

## Docker baseline smoke

Executed before any D-item carry patch:

- Read-only repo mount + disposable `HERMES_HOME` AST parse smoke in Docker passed for key candidate files.
- Actual CLI usability smoke in Docker passed with disposable uv environment:
  - command shape: `uv sync --frozen --no-install-project && /tmp/hermes-venv/bin/python -m hermes_cli.main --version`
  - result: `Hermes Agent v0.17.0 (2026.6.19)` returned successfully from container.
- First attempted `python -m py_compile` against a read-only mount failed because py_compile attempted `__pycache__` writes; read-only Docker smoke should use `ast.parse` or a writable temp copy for syntax checks.

## Operating decision from 주군

1. `.omx/` is local editor/agent runtime state and should be ignored by git.
2. Every D-item requires owner direction before code application: choose upstream-native adoption, upstream plus Root Kernel safety extension, local enhancement, retire, or defer.
3. Final activation goal is to migrate `~/.hermes/hermes-agent/` to the irootkernel Hermes checkout after candidate validation.
4. Before touching `~/.hermes/hermes-agent/`, candidate smoke and feature usability checks should run in Docker with disposable state.

## Release-note signals to absorb

The v0.17.0 release note describes the release as the “Reach Release.” Items that affect Root Kernel carry decisions:

- New communication surfaces: iMessage via Photon, Raft agent network gateway, official WhatsApp Business Cloud API, SimpleX.
- Desktop/dashboard upgrades: full profile builder, multi-profile management, secure dashboard auth, desktop watch windows, model selector, theme support.
- Core agent changes: background async subagents, image-to-image editing, automation blueprints, memory batch operations, curator zero-token routine pruning.
- Architecture/refactor changes: large `cli.py`, `gateway/run.py`, and `run_agent.py` refactors.
- Tool/prompt changes: `search_files` densification, removed agent-callable `send_message`, document extraction in `read_file`, compression changes, `write_approval` replacing older skill/memory write mode.
- Provider/auth changes: OpenRouter credential pool detection and xAI OAuth handling across profiles.

These are treated as first-class upstream capabilities. Root Kernel carries should not duplicate them unless a specific Root Kernel safety or workflow gap remains.

## D-item direction gates

Each D item is presented to 주군 before patching; only owner-approved items are applied and recorded below.

### D1 — Tool Search pair

- v0.16 state: upstream absorbed.
- v0.17 decision: resolved; no local carry.
- Owner direction: do not reintroduce a Root Kernel local patch. This was already resolved in v0.16.0 and is no longer a future release-carry consideration.
- Future rule: only a wholly new independent regression may create a new D-ID; do not replay D1.
- Docker evidence: `tests/tools/test_tool_search.py` passed in disposable Docker env.

### D2 — Kanban review and same-card handoff helpers

- v0.16 state: partial-native local minimized; D2-b/c/d/e/f/g/h/i applied.
- v0.17 release note relevance: background async subagents, automation blueprints, fleet/relay/automation changes, major core refactors.
- Owner decision: keep Kanban-first for official Root Kernel work and carry the full D2 set, D2-a through D2-i. v0.17 `delegate_task(background=true)` will be used gradually as supplemental/experimental help, not as the v0.17 replacement for durable Kanban review gates.
- Direction: retain D2 on the v0.17 native base. Apply each subitem minimally and separately, with ledger updates and disposable Kanban smoke in the same unit.
- Rationale: async delegate_task now avoids synchronous waiting and can return a background handle, but it does not yet replace the durable Kanban task id, formal assignee routing, same-card review/rework loop, creator/final gate, watcher/audit trail, mutex, or workflow banner semantics used by Root Kernel operations.
- D2-a audit evidence recorded:
  - `delegate_task(background=true)` is real in v0.17 and returns a background delegation handle, but completion re-enters via the process completion queue rather than Kanban's durable board/audit model.
  - v0.17 native Kanban review has `claim_review_task`, review status handling, `has_spawnable_review`, and review dispatcher coverage.
  - Host baseline review smoke passed: selected `tests/hermes_cli/test_kanban_db.py` review claim/spawnability tests returned `6 passed`.
- Planned D2 subitems:
  - D2-a: audit and ledger native-vs-local classification.
  - D2-b: cooperative same-card handoff/reassign helper. Applied: `handoff_task` + `kanban_reassign` keep the same task id, close the active run as `handed_off` / `released`, clear claim/current-run state, return the card to `ready` for the target assignee, enforce same-task worker ownership, and use `HERMES_KANBAN_RUN_ID` as a stale-run guard.
  - D2-c: worker submit-for-review same-card transition. Applied: `submit_task_for_review` + `kanban_submit_review` keep the same task id, close the active run as `submitted_review` / `released`, move the card to native `review` for the reviewer, preserve `from_assignee` in the `submitted_review` event for later request-changes, enforce same-task worker ownership, and use `HERMES_KANBAN_RUN_ID` as a stale-run guard.
  - D2-d: reviewer request-changes/rework transition. Applied: `request_changes_task` + `kanban_request_changes` keep the same task id, close the active review run as `requested_changes` / `released`, restore the original implementer from the latest `submitted_review.from_assignee` unless an explicit rework assignee is supplied, clear claim/current-run state, enforce same-task worker ownership, require a feedback reason, and use `HERMES_KANBAN_RUN_ID` as a stale-run guard.
  - D2-e: creator/final gate separation from reviewer done. Applied: `submit_task_for_review(final_assignee=...)` + `complete_task` / `kanban_complete` final-gate routing keep the same task id; reviewer approval closes the review run as `review_accepted` / `released` and returns the card to `ready` for the creator/final assignee, while only the final assignee's later completion marks `done`. Explicit reviewer/final assignee and route-time final gate are spawnability-validated fail-closed before mutation.
  - D2-f: async review watcher/outcome notification support. Applied: `kanban_submit_review` now returns `review_watch` and best-effort auto-subscribes the originating gateway/session source; CLI/cron/unattached contexts report `review_watch={attached:false}`. Gateway Kanban notifier now sends `requested_changes` and `review_accepted` events, says `final gate required` on reviewer acceptance, and keeps the subscription until the task is truly `done`/`archived`.
  - D2-g: creator-accepted result loop. Applied: `submit_task_result` + `kanban_submit_result` + CLI `submit-result` keep the same task id, close the active worker run as `submitted_result` / `released`, move the card to native `review` for the creator/acceptor, record result provenance for later request-changes, and leave final task completion to the acceptor's later `kanban_complete`.
  - D2-h: `mutex_key` serialization for shared artifacts/resources. Applied: nullable `tasks.mutex_key` plus migration/index, `create_task(mutex_key=...)`, dispatcher deferral for running or same-tick spawned same-key tasks, direct `claim_task` mutex guard, `skipped_mutex_locked` diagnostics, `has_spawnable_ready` mutex-deferred suppression, CLI `--mutex-key`, and `kanban_create` schema/handler/output support.
  - D2-i: workflow context banners for K-style Kanban workflows. Applied: closed `workflow_type` enum, nullable `tasks.workflow_type` plus migration/index, prompt-safe worker `## Workflow context` banners, create-time fail-closed validation, invalid persisted value sanitization, CLI `--workflow-type`, and `kanban_create`/list/show tool surfaces.
- Docker gate: disposable Kanban DB workflows and targeted Kanban tests; no production `kanban.db`.
- D2-b RED/GREEN evidence:
  - Focused RED before implementation: 5 expected failures for missing `handoff_task`, missing `_handle_reassign`, and missing `kanban_reassign` schema exposure.
  - Focused GREEN after implementation: D2-b 5-test host smoke passed.
  - Host targeted suites: `tests/tools/test_kanban_tools.py` → `91 passed, 1 warning`; `tests/hermes_cli/test_kanban_db.py` → `220 passed, 1 warning`. Warnings were pre-existing Discord `audioop` deprecation warnings.
  - Docker disposable smoke: D2-b 5-test bundle → `5 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-c evidence:
  - Focused host smoke: 7 D2-c submit-review/tool-visibility tests → `7 passed`.
  - Host targeted suites and syntax at D2-c time: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py` → `482 passed, 1 skipped, 1 warning`; `py_compile` passed for touched Python files. Warning was pre-existing Discord `audioop` deprecation.
  - Docker disposable smoke: D2-c 7-test bundle → `7 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-d evidence:
  - Focused host smoke: 7 D2-d request-changes/tool-visibility tests → `7 passed`.
  - Host targeted suites and syntax after D2-d: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py` → `487 passed, 1 skipped, 1 warning`; `py_compile` passed for touched Python files. Warning was pre-existing Discord `audioop` deprecation.
  - Docker disposable smoke: D2-d 7-test bundle → `7 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-e evidence:
  - Focused host smoke: 6 D2-e creator/final-gate tests → `6 passed`.
  - Host targeted suites and syntax after D2-e: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_core_functionality.py` → `493 passed, 1 skipped, 1 warning`; `ast.parse` passed for touched Python files. Warning was pre-existing Discord `audioop` deprecation.
  - Docker disposable smoke: D2-e 7-test bundle, including existing request-changes rework loop → `7 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-f evidence:
  - RED smoke before implementation: 4 D2-f watcher/notifier tests failed as expected: missing `review_watch` in `kanban_submit_review` output and no notifier delivery for `requested_changes` / `review_accepted`.
  - Focused host GREEN: the same 4 D2-f tests → `4 passed`.
  - Host targeted suites and syntax after D2-f: `tests/tools/test_kanban_tools.py tests/gateway/test_kanban_notifier.py` → `105 passed`; `ast.parse` passed for touched Python files.
  - Docker disposable smoke: D2-f 4-test bundle → `4 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-g evidence:
  - RED smoke before implementation: focused tests confirmed missing `submit_task_result`, missing `kanban_submit_result` schema/registry exposure, and absent result-submission tool path.
  - Focused host GREEN: D2-g DB/tool/CLI bundle → `7 passed, 1 warning`; warning was pre-existing Discord `audioop` deprecation from imported Discord player.
  - Host D2 smoke regression: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_cli.py tests/gateway/test_kanban_notifier.py` → `388 passed`.
  - Docker disposable smoke: D2-g 4-test bundle → `4 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.
- D2-h evidence:
  - RED smoke before implementation: focused DB/tool/CLI tests failed 8/8 for missing `mutex_key` parameter/field/schema/CLI/dispatch diagnostics.
  - Focused host GREEN: D2-h DB/tool/CLI bundle → `8 passed`.
  - Host D2 smoke regression: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_cli.py tests/hermes_cli/test_kanban_core_functionality.py` → `552 passed, 1 skipped, 1 warning`; warning was pre-existing Discord `audioop` deprecation.
  - Docker disposable smoke: D2-h 8-test bundle → `8 passed` with read-only repo mount, disposable `HERMES_HOME`, and no live secrets.
- D2-i evidence:
  - RED smoke before implementation: focused DB/tool/CLI tests failed 10/10 for missing `workflow_type` parameter/column/field/CLI/schema/output/sanitization surfaces.
  - Focused host GREEN: D2-i DB/tool/CLI bundle → `10 passed`.
  - Host D2 smoke regression: `tests/hermes_cli/test_kanban_db.py tests/tools/test_kanban_tools.py tests/hermes_cli/test_kanban_cli.py tests/hermes_cli/test_kanban_core_functionality.py` → `561 passed, 1 skipped, 1 warning`; warning was pre-existing Discord `audioop` deprecation.
  - Docker disposable smoke: D2-i 10-test bundle → `10 passed, 1 warning`; warning was read-only `.pytest_cache` write failure on the read-only repo mount.

### D3 — Kanban assignee alias dispatch seam

- v0.16 state: retired after refactor.
- v0.17 decision: retired; use v0.17 native Kanban/profile dispatch behavior.
- Owner direction: do not restore the Root Kernel assignee alias dispatch seam.
- Future rule: D3 is no longer a future release-carry consideration. Any future alias need must be a new independent D-ID, not D3 replay.
- Docker gate: no D3 replay smoke required; native Kanban path will be covered by later D2/Kanban Docker smoke if D2 changes are retained.

### D4 — Discord owner/thread routing and role-mention fail-close

- v0.16 state: local keep with owner-thread gates, role-mention fail-close, env-only parent owner fallback.
- v0.17 release note relevance: gateway core/rendering changes and new messaging platform refactors.
- Owner decision: option B approved — adopt v0.17 Discord/gateway structure as the base, then retain only the missing Root Kernel safety guarantees.
- Applied seams:
  - `ThreadOwnerTracker` records a persistent thread-id → default owner mapping separate from participation.
  - Auto-created Discord threads are marked as both participated and owned by the current bot profile.
  - Mention-free thread replies require ownership, not mere participation; later-mentioned foreign bots do not become default responders.
  - Role mentions without this bot's direct mention fail closed so default/free-response routing cannot steal role-addressed tasks.
  - Parent text-channel free-response does not leak into ordinary child text threads; forum-thread inheritance remains allowed.
  - `DISCORD_DEFAULT_THREAD_OWNER_PARENT_CHANNELS` remains env-only for profile-local parent channels whose user-created child threads belong to this bot.
  - `DISCORD_AUTO_THREAD_FREE_RESPONSE` / `auto_thread_free_response` explicitly opt free-response channels back into owned auto-thread creation.
- Hotfix 2026-07-09:
  - Cause: `discord.auto_thread_free_response: true` existed in root config but D4's Discord plugin YAML bridge did not export it to `DISCORD_AUTO_THREAD_FREE_RESPONSE`, so the env-driven adapter treated free-response parent channels as `skip_thread=True` and replied inline.
  - Fix: bridge top-level `discord.auto_thread_free_response` into `DISCORD_AUTO_THREAD_FREE_RESPONSE`; add a regression test for the actual YAML→env path.
- Verification:
  - RED before fix: `test_discord_yaml_bridge_sets_auto_thread_free_response_env` failed with `None == 'true'`.
  - Focused GREEN: `test_discord_yaml_bridge_sets_auto_thread_free_response_env`, `test_discord_auto_thread_free_response_allows_owned_threads`, `test_discord_auto_thread_free_response_config_extra` → 3 passed.
  - `tests/gateway/test_discord_free_response.py`: 50 passed.
  - `ast/compile` smoke for `plugins/platforms/discord/adapter.py` and `tests/gateway/test_discord_free_response.py`: passed.
  - Previous Docker clean-env routing bundle: 86 passed, 1 read-only pytest-cache warning.
  - Previous clean Discord-env full `tests/gateway/test_discord*.py`: 412 passed, 2 pre-existing voice coroutine warnings.
- Docker/live gate: fake Discord object tests only; no live Discord token/send used; no gateway restart in this hotfix.

### D5 — Support-only plugin strategy

- v0.16 state: retired/no-code.
- v0.17 decision: retired/no-code; past policy only.
- Owner direction: do not restore support-only plugin strategy for v0.17.
- Future rule: D5 is no longer a future release-carry consideration. Any future plugin strategy must be a new independent D-ID with a concrete current need.
- Docker gate: no D5 replay smoke required; source dependency audit found no active dependency.

### D6 — CLI return-code passthrough

- v0.16 state: local keep.
- v0.17 decision: local keep applied as a minimal Root Kernel patch.
- Evidence:
  - current `hermes_cli/main.py` still executes `args.func(args)` and discards the returned integer;
  - upstream v0.17 test comment in `tests/hermes_cli/test_kanban_core_functionality.py` explicitly notes this limitation;
  - Docker subprocess smoke showed `kanban show definitely_missing_task` prints the error but exits `0`, expected `1`;
  - Docker subprocess smoke showed `kanban boards switch ""` prints usage error but exits `0`, expected `2`;
  - help path still exits `0` as expected.
- Applied patch: added `_exit_if_int_return_code(rc)` to `hermes_cli/main.py`, using exact `type(rc) is int` passthrough so bools are ignored, and called it after `args.func(args)`.
- Tests/docs updated: restored `tests/hermes_cli/test_main_exit_codes.py` and updated the stale Kanban test comment that assumed discarded return codes.
- Docker evidence after patch:
  - `pytest -q tests/hermes_cli/test_main_exit_codes.py -o addopts=` with `uv sync --frozen --extra dev --no-install-project`: `7 passed, 1 warning` in disposable Docker env; warning was pytest cache write blocked by read-only repo mount.
  - subprocess smoke: `kanban show definitely_missing_task` -> rc `1`; `kanban boards switch ""` -> rc `2`; `kanban --help` -> rc `0`.

### D7 — Doctor optional tool warning filter

- v0.16 state: local keep.
- v0.17 decision: local keep applied as a minimal Root Kernel patch.
- Evidence:
  - v0.17 release notes and current `hermes_cli/doctor.py` do not include an equivalent Tool Availability config-scope filter;
  - disposable Docker audit before patch showed API-key unavailable rows for `discord`, `discord_admin`, `moa`, `web`, and `x_search`; only `web` was enabled/actionable for the default CLI scope;
  - this preserves the local rule that unused/default-off integrations should stay disabled instead of requiring API keys only to silence doctor.
- Applied patch: added `_doctor_enabled_toolsets_for_warning_scope()` and `_filter_doctor_tool_availability_for_config()` to `hermes_cli/doctor.py`, then applied the filter after runtime-gated overrides and before Tool Availability output/issues are emitted. Config/toolset resolution failure returns `None` and preserves fail-open diagnostics.
- Tests updated: added `TestDoctorToolAvailabilityConfigFilter` for disabled optional suppression, explicitly selected optional warning preservation, and fail-open behavior.
- Docker evidence after patch:
  - `pytest -q tests/hermes_cli/test_doctor.py::TestDoctorToolAvailabilityConfigFilter -o addopts=` → `3 passed, 1 warning`;
  - `pytest -q tests/hermes_cli/test_doctor.py tests/hermes_cli/test_doctor_dedicated_provider_skip.py -o addopts=` → `71 passed, 1 warning`;
  - helper smoke changed API-key unavailable rows from `discord`, `discord_admin`, `moa`, `web`, `x_search` to `web` only under disposable default CLI config.
- Warning note: Docker warnings were pytest cache writes blocked by the read-only repo mount, not test failures.
- Next release: re-check upstream doctor Tool Availability scoping; if absorbed, drop the local helper.

### D8 — OpenAI Codex credential pinning and labelled reauth

- v0.16 state: local keep.
- v0.17 decision: minimized local keep applied.
- Upstream overlap retained:
  - v0.17 release notes mention provider/auth work: Codex OAuth pool accounts stay distinct on add/re-auth.
  - Current `auth_commands.py` already creates distinct `manual:device_code` pool entries for `hermes auth add openai-codex`.
  - Current `_sync_codex_pool_entries()` already avoids overwriting independent `manual:device_code` entries whose token material does not match the previous singleton.
- Remaining Root Kernel seam:
  - `HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID` / `_LABEL` are read only from profile-local `.env`, not ambient process env.
  - `ID` wins over `LABEL`; labels must be exact and unique.
  - pinned missing/duplicate/exhausted/dead/unavailable entries fail closed; no fallback to singleton or another OpenAI account.
  - main runtime and auxiliary Codex token resolution honor the same pin.
  - `hermes auth add openai-codex --label <LABEL>` updates exactly one matching refreshable pool entry, creates a labelled `manual:device_code` entry when absent, fails closed on duplicate labels, and leaves other labels plus the provider singleton unchanged.
- Files changed:
  - `agent/credential_pool.py`
  - `agent/auxiliary_client.py`
  - `hermes_cli/runtime_provider.py`
  - `hermes_cli/auth.py`
  - `hermes_cli/auth_commands.py`
  - `tests/agent/test_credential_pool.py`
  - `tests/agent/test_auxiliary_client.py`
  - `tests/hermes_cli/test_runtime_provider_resolution.py`
  - `tests/hermes_cli/test_auth_codex_provider.py`
  - `tests/hermes_cli/test_auth_commands.py`
- Host smoke:
  - D8 focused fake-token tests: `11 passed`.
  - related credential/runtime/auth command suite: `302 passed`.
  - auxiliary Codex token targeted tests: `10 passed`.
- Docker smoke:
  - D8 focused fake-token tests: `11 passed, 1 warning`.
  - related credential/runtime/auth/auxiliary targeted suite: `312 passed, 1 warning`.
  - disposable `HERMES_HOME` no-token selection smoke: `selected_label HSY`, `selected_id hsy`.
  - Docker warnings were pytest cache write attempts on a read-only repo mount.
- Live boundary: no live `.env`, `auth.json`, token, profile home, gateway process, or `rk/live` state was changed.

## R-item activation closeout

R-items are activation/local-state gates, not product-code D-item carries. They are recorded separately so `rk/tag/v0.17.0` only marks a release after both runtime carries and required local activation checks have been reconciled.

### R1 — Config/profile activation policy

- Status: completed-post-activation.
- Result: config/profile compatibility was resolved during the approved activation window.
- Applied activation fix:
  - removed deprecated/unknown `messaging` toolset entries from `platform_toolsets.cli` and `platform_toolsets.discord` for `bongchu`, `jooyoo`, `samaui`, and `wolyeong` after non-secret config backups;
  - restarted the affected running gateways only;
  - final post-activation smoke reported deprecated `messaging` toolset scan with zero hits.
- Evidence:
  - final receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/final-activation-receipt-20260708T144804Z.md`;
  - recovery backup: `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/pre-activation-config-migration/`;
  - R1 config backup: `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r1-remove-deprecated-messaging-toolset/`.
- Tag blocker: none remaining for R1 unless new config drift is discovered.

### R2 — Skill provenance, overrides, and compatibility policy

- Status: completed-scoped-activation-check.
- Result: no activation-blocking skill provenance/metadata issue found in the scoped R2 audit; representative load-bearing skill-load smoke passed.
- Read-only audit evidence:
  - audit output: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r2-skill-audit-20260708T154010Z/r2-skill-audit.json`.
- Audit summary:
  - repo bundled skills: 73 names, 0 duplicate names, 0 malformed frontmatter;
  - repo optional skills: 100 names, 0 duplicate names, 0 malformed frontmatter;
  - shared ops skills: 95 names, 0 duplicate names, 0 malformed frontmatter;
  - active cron skill refs observed by this R2 audit: 0;
  - explicit skill-load smoke passed for `default` + `hermes-17e-update`, `default` + `release-carry-ledgers`, `hwangchung` + `kanban-worker`, and `samaui` + `kanban-worker`.
- Upstream skill-tree note:
  - v0.16 to v0.17 changed `skills/` and `optional-skills/` materially;
  - removed or moved upstream bundled skills were not restored as D-item runtime carries;
  - broader profile-owned skill/cron/script usage-style optimization belongs to R5, not R2.
- Tag blocker: none remaining for R2.

### R3 — Web dashboard and desktop activation gate

- Status: completed-dashboard-verified-desktop-unused.
- Dashboard result: verified on the activated v0.17.0 runtime.
- Dashboard evidence:
  - audit output: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r3-dashboard-desktop-audit-20260708T154614Z/`;
  - `hermes dashboard --status` reported one dashboard process running;
  - `/api/status` on port `9119` was reachable and reported version `0.17.0`, config version `30`, `gateway_running=true`, and connected Telegram/Discord gateway state.
- Desktop decision: intentionally unused in this environment.
- Desktop cleanup evidence:
  - cleanup receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r3-desktop-unused-cleanup-20260708T160712Z/receipt.txt`.
- Cleanup result:
  - no `/Applications` or `~/Applications` Hermes Desktop install was present;
  - live checkout desktop artifacts were ignored build outputs, not tracked repo files;
  - removed ignored paths: `apps/desktop/node_modules`, `apps/desktop/dist`, `apps/desktop/build`, `apps/desktop/release`, and `apps/desktop/tsconfig.tsbuildinfo`;
  - preserved source paths: `apps/desktop/package.json` and `apps/desktop/electron`.
- Tag blocker: none remaining for R3. Desktop build/install/usability is out of scope unless 주군 later re-enables Desktop use.

### R4 — Cron, automation blueprints, and local script activation gate

- Status: completed-read-only-activation-check.
- Result: no active cron/script/local automation blocker remains for `rk/tag/v0.17.0`.
- Read-only audit evidence:
  - audit output: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r4-cron-script-audit-20260708T161109Z/r4-cron-script-audit.json`;
  - active script embedded path checks: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r4-cron-script-audit-20260708T161109Z/r4-active-script-embedded-path-checks.json`;
  - closeout classification: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r4-cron-script-audit-20260708T161109Z/r4-closeout-classification.json`.
- Audit summary:
  - 14 profiles had cron files;
  - 15 active jobs were observed across `mibang`, `songeon`, `wolong`, and `wolyeong`;
  - all 15 active job scripts existed and parsed cleanly;
  - active cron skill refs were 0;
  - all active jobs reported `last_status=ok`;
  - four `songeon` retention warnings were diagnostic false positives caused by prompt-text path matching, not missing active scripts.
- Hwangchung cleanup evidence:
  - selection cleanup manifest: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hwangchung-selection-cleanup-20260708T162600Z/manifest.json`;
  - Kanban admin closeout summary: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hwangchung-kanban-admin-closeout-20260708T163035Z/postclose-summary.json`.
- Hwangchung cleanup summary:
  - stale inactive watcher `watch_dagsm005_red_plan_t_4a8ff082.py` had zero active cron references and was quarantined;
  - post-cleanup parse sweep found 234 Hwangchung profile scripts and 0 parse failures;
  - Hwangchung gateway service definition was repaired to match the current v0.17 install and verified loaded/running;
  - Hwangchung active Kanban WIP was administratively archived to 0 remaining open cards.
- Tag blocker: none remaining for R4 unless new live automation drift is discovered.

### R5 — Profile-owned local asset optimization after v0.17 activation

- Status: in-progress-approved-profile-archive-and-project-skill-purge-non-tag-blocking.
- Result: broader profile-owned skill/cron/script usage-style optimization is in progress. 주군 approved deletion of storage-only profile skill `.archive` directories and stale project wrapper/overlay KAS skills superseded by recent project updates; R5 remains non-blocking for `rk/tag/v0.17.0`.
- R5 inventory evidence:
  - JSON inventory: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-profile-owned-local-asset-inventory-20260708T165501Z/r5-inventory.json`;
  - summary: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-profile-owned-local-asset-inventory-20260708T165501Z/r5-inventory.md`;
  - candidate triage: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-profile-owned-local-asset-inventory-20260708T165501Z/r5-candidate-triage.json`;
  - refined edit queue: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-profile-owned-local-asset-inventory-20260708T165501Z/r5-refined-edit-queue.json`;
  - profile skill archive purge receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-profile-skill-archive-purge-20260708T173354Z/receipt-after-delete.json`;
  - profile skill archive purge rollback backup: `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-profile-skill-archive-purge-20260708T173354Z/`;
  - KAS/project wrapper-overlay skill purge receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-kas-project-skill-wrapper-overlay-purge-20260708T174342Z/receipt-after-delete.json`;
  - KAS/project wrapper-overlay skill purge rollback backup: `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-kas-project-skill-wrapper-overlay-purge-20260708T174342Z/`;
  - canonical skill inspection after `research-paper-writing` patch: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-canonical-skill-inspection-20260708T175000Z.json`;
  - immediate canonical skill patch receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-immediate-canonical-skill-patches-20260708T181500Z.json`;
  - active cron prompt inspection receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-active-cron-prompt-inspection-20260709T000000Z/receipt.json`;
  - script wrapper/retirement review receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-script-wrapper-retirement-review-20260709T000000Z/receipt.json`;
  - live launchctl reference check for script retirement candidates: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-script-wrapper-retirement-review-20260709T000000Z/live-launchctl-reference-check.json`;
  - root runtime watcher delete manifest: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-root-runtime-watcher-delete-20260709T001500Z/manifest-before-delete.json`;
  - root runtime watcher delete receipt: `/Users/draccoon/Workspace/Hermes/17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/r5-root-runtime-watcher-delete-20260709T001500Z/receipt-after-delete.json`;
  - root runtime watcher delete rollback backup: `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-root-runtime-watcher-delete-20260709T001500Z/`.
- Inventory summary:
  - skills: 868 total; classes include 89 `17h-owned-custom`, 452 `17h-profile-local-owner-review`, 149 `project-maintainer-follow`, 173 `upstream-bundled-follow`, and 5 `vendor-or-hub-follow`;
  - cron jobs: 70 total, 15 active; 14 classified as `17h-cron-prompt`, 41 as `project-maintainer-follow`, and 15 inactive/deferred;
  - scripts: 727 total; 98 `17h-canonical-script`, 113 `runtime-wrapper-or-profile-local-owner-review`, and 516 `project-maintainer-follow`.
- Refined queue summary:
  - Wave 1 actual patch candidates: 3, all `research-paper-writing` copies with stale `send_message` tool guidance; only the shared ops custom copy is an immediate R5 patch candidate, while bundled/upstream and archived profile-local copies are follow/owner-review surfaces;
  - Wave 2 canonical operations-skill inspection candidates: 6 (`release-carry-ledgers`, `team-profile-activation`, `kanban-orchestrator`, `hermes-operations`, `hermes-17e-update`, `hermes-team-operations`);
  - active cron prompt inspection candidates: 13;
  - script wrapper or retirement review candidates: 23;
  - 30 high-priority regex hits were deferred as false positives or low-priority normal sleep/polling contexts.
- Approved profile skill archive purge:
  - removed 6 `~/.hermes/profiles/<profile>/skills/.archive` directories: `bongchu`, `goong`, `jalong`, `kangyoo`, `macho`, and `mibang`;
  - rollback backup stored 1,106 archived files including 199 archived `SKILL.md` files under `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-profile-skill-archive-purge-20260708T173354Z/`;
  - post-delete verification found 0 remaining profile `skills/.archive` directories;
  - affected profile `skills list` smoke passed for all 6 profiles;
  - no gateways, providers, auth, tokens, runtime config, commits, pushes, or tags were changed.
- Approved KAS/project wrapper-overlay skill purge:
  - removed 48 profile-local project skill directories matching `~/.hermes/profiles/<profile>/skills/<project>/<project>-wrapper` and `<project>-overlay`;
  - affected 12 profiles: `hahuyeon`, `hwangchung`, `ijeok`, `jingung`, `jonghoe`, `macho`, `manchong`, `seohwang`, `taesaja`, `wiyeon`, `yeomong`, and `yuyeop`;
  - affected 6 projects: `atn-control`, `atn-plugin`, `kkachi-agent-helper`, `kkachi-agent-skills`, `kkachi-agent-tester`, and `space-compiler`;
  - rollback backup stored 544 files under `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-kas-project-skill-wrapper-overlay-purge-20260708T174342Z/`;
  - active cron direct skill references were 0 before deletion;
  - post-delete verification found 0 remaining matching wrapper/overlay project skill directories;
  - affected profile `skills list` smoke passed for all 12 profiles;
  - no gateways, providers, auth, tokens, runtime config, commits, pushes, or tags were changed.
- Approved `research-paper-writing` ops custom patch and canonical skill inspection:
  - patched `/Users/draccoon/Workspace/Hermes/ops/skills/research/research-paper-writing/SKILL.md` to remove stale positive `send_message` guidance and replace it with current final-response, cronjob delivery, and `terminal(background=True, notify_on_complete=True)` patterns;
  - verification found 0 remaining `send_message` mentions in the ops custom copy;
  - canonical inspection found immediate namespace/tooling wording candidates in `release-carry-ledgers`, `hermes-operations`, and `hermes-17e-update`;
  - user-approved immediate patches converted active release examples and update-routing guidance from legacy `17e` / `for_17th_earth` wording to current `rk/*`, `root-kernel/carry.yaml`, and `for-root-kernel.md` wording while preserving historical/reference `17e` notes;
  - verification found 0 remaining positive stale candidates across the six inspected canonical skills;
  - `team-profile-activation` and `hermes-team-operations` need no immediate R5 patch;
  - `kanban-orchestrator` remains maintainer-lane, not an opportunistic R5 patch target.
- Active cron prompt inspection:
  - covered 13 enabled jobs across `mibang`, `songeon`, `wolong`, and `wolyeong`;
  - all 13 passed no-edit with scripts resolving and no positive stale v0.17/R5 prompt guidance.
- Script wrapper/retirement review:
  - covered 23 script candidates;
  - 14 were backup snapshots excluded from edit;
  - 1 canonical governance script was kept no-edit;
  - 8 unreferenced root runtime watcher scripts were classified as retirement candidates;
  - live launchctl ProgramArguments scan found 0 matches for the 8 retirement candidates;
  - with 주군 approval, backed up and deleted the 8 unreferenced root `~/.hermes/scripts` watcher files;
  - backup verification passed, post-delete verification found all 8 absent, and rollback material is under `/Users/draccoon/Workspace/Hermes/update-backups/20260709-rk-v017/r5-root-runtime-watcher-delete-20260709T001500Z/`;
  - no cron jobs, launchd plists, gateways, providers, auth, tokens, runtime config, commits, pushes, or tags were changed by this inspection/delete pass.
- Boundary:
  - R2 already covered skill provenance/resolver readiness for activation;
  - R4 already covered active cron/script existence, syntax, stale watcher cleanup, and local automation blockers for activation;
  - R5 starts from ownership-first classification and must not rewrite bundled, vendor, external-maintainer, or project-maintainer assets without a maintainer-lane decision;
  - the initial inventory and triage did not mutate files, profiles, gateways, providers, auth, tokens, runtime config, commits, pushes, or tags; the later user-approved `.archive` and project wrapper/overlay purges mutated only storage-only profile skill directories and kept rollback backups.
- Next action: R5 is complete and remains non-tag-blocking; proceed with final R1-R5 SOT validation and then request explicit approval before any Root Kernel commit, push, `rk/live` movement, or `rk/tag/v0.17.0` creation.
- Tag blocker: no. R5 is complete and is not a `rk/tag/v0.17.0` blocker.

## Docker smoke rule

Before moving `rk/live`, reinstalling runtime, or migrating `/Users/draccoon/.hermes/hermes-agent/`, candidate checks must run in Docker where possible:

- read-only repo mount or clean image build;
- disposable `HERMES_HOME`;
- no live `.env`, `auth.json`, tokens, gateway sockets, production profile homes, or production DBs;
- smoke must exercise actual CLI/tool behavior for the D-item, not only parse source files;
- any Docker blocker is reported separately from host-targeted test results.

## Activation boundary

Historical pre-activation boundary: branch preparation alone did not authorize moving `rk/live`, replacing or repointing `/Users/draccoon/.hermes/hermes-agent/`, editable runtime reinstall, profile config migration, gateway restart, dashboard/desktop persistent launchd changes, or live platform sends.

Activation was later explicitly approved and completed for `rk/v0.17.0`; see the R-item closeout above and the final activation receipt under `17thHermes/50_health/team/heuktaeja/hermes-agent-update/rk-v0.17.0/`. Live platform sends and persistent dashboard/desktop launchd changes remain outside this branch-preparation log unless separately approved.
