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
- v0.18.2 state: not yet evaluated.
- Next action: audit v0.18.2 Kanban, `/goal`, background subagents, review/final-gate/watcher/mutex/workflow native behavior before carrying code.

### D3 — Kanban assignee alias dispatch seam

- Previous v0.17 state: retired.
- v0.18.2 starting decision: retired carry-forward. Do not replay.

### D4 — Discord owner/thread routing and role-mention fail-close

- Previous v0.17 state: local keep applied, including free-response auto-thread config bridge hotfix.
- v0.18.2 state: not yet evaluated.
- Next action: audit v0.18.2 Discord/gateway routing and auto-thread behavior before applying minimal safety seams.

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
- v0.18.2 state: selected as first audit item.
- Next action: audit v0.18.2 `agent/credential_pool.py`, `agent/auxiliary_client.py`, `hermes_cli/runtime_provider.py`, `hermes_cli/auth.py`, and `hermes_cli/auth_commands.py` against the Root Kernel D8 requirements.
- Smoke boundary: fake-token/disposable-state only; no live `.env`, `auth.json`, token, profile home, gateway process, or `rk/live` mutation.

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
