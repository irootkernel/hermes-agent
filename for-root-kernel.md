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
  - D2-g: creator-accepted result loop.
  - D2-h: `mutex_key` serialization for shared artifacts/resources.
  - D2-i: workflow context banners for K-style Kanban workflows.
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
- Verification:
  - `tests/gateway/test_discord_free_response.py`: 49 passed.
  - Docker clean-env routing bundle: 86 passed, 1 read-only pytest-cache warning.
  - Clean Discord-env full `tests/gateway/test_discord*.py`: 412 passed, 2 pre-existing voice coroutine warnings.
- Docker/live gate: fake Discord object tests only; no live Discord token/send used.

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

## Docker smoke rule

Before moving `rk/live`, reinstalling runtime, or migrating `/Users/draccoon/.hermes/hermes-agent/`, candidate checks must run in Docker where possible:

- read-only repo mount or clean image build;
- disposable `HERMES_HOME`;
- no live `.env`, `auth.json`, tokens, gateway sockets, production profile homes, or production DBs;
- smoke must exercise actual CLI/tool behavior for the D-item, not only parse source files;
- any Docker blocker is reported separately from host-targeted test results.

## Activation boundary

This branch preparation does not authorize:

- moving `rk/live`;
- replacing or repointing `/Users/draccoon/.hermes/hermes-agent/`;
- editable reinstall of the live runtime;
- profile config migration;
- gateway restart;
- dashboard/desktop persistent launchd changes;
- live Discord/Telegram/iMessage/WhatsApp/Raft/SimpleX sends.

Those remain separate activation approvals after candidate D/R and Docker smoke evidence.
