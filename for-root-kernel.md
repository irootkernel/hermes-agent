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

No D item below is approved for code application yet. Each will be presented to 주군 before patching.

### D1 — Tool Search pair

- v0.16 state: upstream absorbed.
- v0.17 decision: resolved; no local carry.
- Owner direction: do not reintroduce a Root Kernel local patch. This was already resolved in v0.16.0 and is no longer a future release-carry consideration.
- Future rule: only a wholly new independent regression may create a new D-ID; do not replay D1.
- Docker evidence: `tests/tools/test_tool_search.py` passed in disposable Docker env.

### D2 — Kanban review and same-card handoff helpers

- v0.16 state: partial-native local minimized; D2-b/c/d/e/f/g/h/i applied.
- v0.17 release note relevance: background async subagents, automation blueprints, fleet/relay/automation changes, major core refactors.
- Initial recommendation: audit v0.17 native Kanban/team/automation surfaces first; retain only Root Kernel creator-gate, same-card, watcher, mutex, or workflow-context gaps that remain.
- Docker gate: disposable Kanban DB workflows and targeted Kanban tests; no production `kanban.db`.

### D3 — Kanban assignee alias dispatch seam

- v0.16 state: retired after refactor.
- v0.17 decision: retired; use v0.17 native Kanban/profile dispatch behavior.
- Owner direction: do not restore the Root Kernel assignee alias dispatch seam.
- Future rule: D3 is no longer a future release-carry consideration. Any future alias need must be a new independent D-ID, not D3 replay.
- Docker gate: no D3 replay smoke required; native Kanban path will be covered by later D2/Kanban Docker smoke if D2 changes are retained.

### D4 — Discord owner/thread routing and role-mention fail-close

- v0.16 state: local keep with owner-thread gates, role-mention fail-close, env-only parent owner fallback.
- v0.17 release note relevance: gateway core/rendering changes and new messaging platform refactors.
- Initial recommendation: adopt v0.17 gateway/Discord structure as base; retain only explicit Root Kernel safety guarantees if upstream still lacks them.
- Docker gate: fake Discord routing tests; no live Discord token/send.

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
- v0.17 release note relevance: new toolsets, write approval, curator behavior, more optional surfaces.
- Initial recommendation: audit v0.17 doctor output first; only retain filtering for disabled/default-off optional tool warnings if needed.
- Docker gate: disposable config doctor smoke and targeted doctor tests.

### D8 — OpenAI Codex credential pinning and labelled reauth

- v0.16 state: local keep.
- v0.17 release note relevance: provider/auth changes including credential pool behavior.
- Initial recommendation: audit v0.17 provider/auth pool changes; switch to native if it now covers multi-account profile affinity, otherwise keep Root Kernel profile-local `.env` pin fail-close semantics and labelled reauth scoping.
- Docker gate: fake-token credential pool and auth command tests; no live `auth.json` or tokens.

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
