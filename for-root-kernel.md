# Root Kernel Hermes Agent v0.19.1

## Release state

- Status: `task5-d1-verification-pass-awaiting-owner-acceptance`
- Candidate branch: `rk/v0.19.1`
- Candidate worktree: `/Users/draccoon/Workspace/Hermes/17th-hermes-agent-worktree`
- Tag blocker: `true`
- Live activation: not started
- Previous Task 2 commit: `509ae0f6d1c5ea9f7dfb9a77a965614dd91b16ff`
- Task 3 ledger commit: `53e6060682a8dc98df6a30ef671b2ecb53c2384e`
- Current D1 commit: this ledger commit; exact SHA is recorded in Git and the excluded D1 evidence
- Task 4 evidence: local progress-only and Git-excluded; accumulated ledger updates are included in the authorized D1 commit scope
- Task 4 accepted by owner at `2026-08-02T19:33:32+09:00`, including the recorded 47-profile YAML formatting caveat
- Tag, push, and remote-ref movement: not authorized
- Scaffolded at: `2026-08-02T17:24:26+09:00`

This document is the human-readable release ledger. `root-kernel/carry.yaml` is the machine-readable operational ledger. Both must be updated together after every approved D-item direction or verified result.

## Exact release baseline

| Field | Observed value |
|---|---|
| Direct update | v0.18.2 → v0.19.1 |
| Previous upstream tag | `v2026.7.7.2` |
| Previous upstream commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Target upstream tag | `v2026.7.30` |
| Target tag object | `d25e2dbdbc40b49808c0a0e9cfed21cc90cffab3` |
| Target upstream commit | `cc4cab2f592e60a197e796506de9168f74baf3ea` |
| Target package version | `0.19.1` |
| Previous downstream branch | `rk/v0.18.2` |
| Previous downstream head | `75a1faf0eb49b6bd465d80c02775b024afa521e8` |
| Local live clone | `/Users/draccoon/.hermes/hermes-agent` |
| Local live branch before activation | `rk/live` |
| Local live head before activation | `75a1faf0eb49b6bd465d80c02775b024afa521e8` |
| Preserved rollback branch | `rk/rollback/pre-v0.18.2-20260801T014431` at `79780a587ecb260788a23767d9996d5f7042a311` |

The target tag was refreshed from upstream and its SSH signature was verified against fingerprint `SHA256:x9xNOpeJhoEAY2gWhmWHZROC3QF3VjOEbmNo9vQ8y2A`.

### Remote refs observed on 2026-08-02

- `origin/rk/live` → `75a1faf0eb49b6bd465d80c02775b024afa521e8`
- `origin/rk/v0.18.2` → `75a1faf0eb49b6bd465d80c02775b024afa521e8`
- `origin/rk/tag/v0.18.2^{}` → `75a1faf0eb49b6bd465d80c02775b024afa521e8`
- annotated tag object `origin/rk/tag/v0.18.2` → `bfa6743ec69e28ce73c9634e5d792fc5422c7ca1`
- `origin/rk/v0.19.1` → absent

Remote state is recorded as observed, not inferred. No remote ref was changed.

## Update path and evidence boundaries

- v0.19.0 / `v2026.7.20` is analysis-only. It is not a merge, runtime, migration, or activation step.
- v0.19.1 / `v2026.7.30` is the only candidate and activation target.
- Captured local progress release-note evidence:
  - `root-kernel/evidence/release-note-v2026.7.20.md`
  - `root-kernel/evidence/release-note-v2026.7.30.md`
- Captured local progress exact-delta evidence:
  - `root-kernel/evidence/upstream-delta-v2026.7.7.2-to-v2026.7.30.md`
  - `root-kernel/evidence/upstream-delta-v2026.7.7.2-to-v2026.7.30.json`
  - `root-kernel/evidence/v0.19.1-config-state-skill-signals.md`
- Captured local progress config-impact evidence:
  - `root-kernel/evidence/v0.19.1-config-impact.md`
  - `root-kernel/evidence/v0.19.1-config-impact.json`
- Captured local progress config-application evidence:
  - `root-kernel/evidence/v0.19.1-config-application.md`
  - `root-kernel/evidence/v0.19.1-config-application.json`
- Captured local progress state-schema evidence:
  - `root-kernel/evidence/v0.19.1-state-schema-canary.json`
  - `root-kernel/evidence/v0.19.1-d1-cjk-recovery.json`

Task 3 captured all five files and verified their source tags, GitHub release bodies, exact Git delta, semantic source signals, hashes, and no-live-mutation boundary.

## Candidate and live-mutation boundary

The candidate started from the clean peeled upstream tag. Task 2 added and committed only:

- `for-root-kernel.md`
- `root-kernel/carry.yaml`

Task 3 created five local progress files under Git-excluded `root-kernel/evidence/` and updated both ledgers. Evidence files are not repository commit material unless separately approved. No carry code, test port, state database, skill installation, plugin, cron job, live checkout, remote ref, or tag was changed.

Task 4 changed only the four owner-approved typed config outcomes across 49 profile configs: `approvals.mode: smart`, integer `approvals.timeout: 300`, retained `approvals.cron_mode: deny`, and empty-string `stt.language`. `.env`, `auth.json`, credentials, gateways, live code, and candidate code were not changed. The non-secret rollback package is `/Users/draccoon/Workspace/Hermes/update-backups/20260802T185328-rk-v0191-task4-smart-stt/`.

Task 5 and D1 verification used only synthetic databases beneath disposable `/private/var/folders/.../rk-v0191-task5-*` roots. The final process-wide SQLite connection guard observed 73 connections, all inside the disposable root or in memory. No real profile `state.db`, sidecar, or backup was opened or copied. D1 changed only candidate `hermes_cli/session_recovery.py`, its regression test, and the paired ledgers; live code, config, gateway, remote ref, and tag remain unchanged.

Rollback for the scaffold is to discard these two files before commit or revert the ledger-only Task 2 commit afterward. Rollback for later code work remains branch switch to `rk/v0.18.2`. Live rollback remains anchored by the separate live clone and preserved release refs.

## Config, state, and skill signals

These values are the completed planning baseline. Fleet values must be refreshed read-only in their dedicated tasks before activation.

### Configuration

- Task 4 read-only audit first proved all 49 configs unchanged and captured the typed rollback source.
- Owner then approved the 49-profile target: `approvals.mode: smart`, integer `approvals.timeout: 300`, retained `approvals.cron_mode: deny`, and empty-string `stt.language`.
- Final explicit state: all four target values and types pass on 49/49.
- Target v0.19.1 `config check`: 49 passed, 0 failed.
- Smart auxiliary route remains configured on 49/49; auxiliary failure escalates to the owner and cron deny runs before smart verdicts.
- Exact existing `agent.max_turns`, compression semantics, reasoning display, multiplex/profile-route isolation, model/provider, and non-target config semantics are retained on 49/49.
- Canary `jinrim` stopped on a formatting-only diff from the first writer, then recovered its exact original hash, mode, owner, and mtime before a corrected canary passed.
- The fleet writer normalized YAML quoting, wrapping, or list indentation on 47 generated comment-free configs. Parsed non-target semantics, modes, owners, `.env`, and `auth.json` hashes remain unchanged on 49/49.
- Typed semantic rollback is verified on 49/49. Exact pre-change byte reconstruction is available on 2/49; 47/49 retain normalized YAML formatting after semantic rollback.
- Non-secret rollback package: `/Users/draccoon/Workspace/Hermes/update-backups/20260802T185328-rk-v0191-task4-smart-stt/`; archive SHA-256 `7edd8c4b96c9ea7e38959860891aba82611db0d61ee24052dd157f38387ee088`.
- `gateway.multiplex_profiles` and `profile_routes` remain inactive. Gateway PID `68805` is unchanged and no gateway was restarted.
- Root default still has non-empty `TELEGRAM_BOT_TOKEN` and `DISCORD_BOT_TOKEN` variable names. Values were not read or changed; root messaging activation remains forbidden.

### State

- Planning baseline: 12 databases at schema 19 and 37 at schema 16.
- v0.19.1 source target: schema 23, verified at `hermes_state_common.py::SCHEMA_VERSION`.
- The first planned eight-file run passed 79 tests with 0 failures; after adding the D1 regression the same set passed 80 tests with 0 failures.
- Genuine historical schema 16 (`d62979a6...`) and schema 19 (`rk/v0.18.2`) fixtures both migrated directly to 23 with 2 sessions and 5 messages preserved, nonzero files, `integrity_check=ok`, and working Korean and English search.
- External-content FTS conversion, three-index rebuild, index-only recovery, malformed-schema repair, read-only preflight, outside-home refusal, WAL fallback, zeroed-file quarantine, and exact backup-only rollback passed.
- RED finding: with `cjk_unicode61` enabled, `recover_session_database()` created CJK triggers through `SessionDB`, then reopened the destination through plain `sqlite3.connect` without loading the tokenizer. Message copying failed `5→0`, verification reported `complete: false`, and the source remained unchanged.
- D1 implementation: load the existing CJK extension helper on the destination copy and verification connections; no config default or profile config changed.
- GREEN result: schema 16→23 and 19→23 each preserve 2 sessions and 5 of 5 messages under the default CJK-enabled recovery path, report `complete: true`, pass CJK integrity and Korean search, and leave the source unchanged.
- Current linked SQLite is 3.50.4 and falls in the WAL-reset vulnerability range; v0.19.1 correctly fails safe to `journal_mode=DELETE`.
- Task 5 technical verification now passes and awaits owner acceptance. No inactive real-profile canary was authorized or required because the synthetic paths and strict SQLite path guard provide sufficient D1 evidence.
- Owner direction: retain this minimal candidate runtime fix as current v0.19.1 D1, commit it as `[D1] CJK-aware offline session recovery`, and retire it after an exact upstream replacement is proven. Because no inherited D item had started, the provisional D1–D5 mapping shifted to D2–D6 to preserve actual execution order.

### Skills

- v0.19.1 bundled source contains exactly 70 `SKILL.md` files; this count was rechecked on the candidate.
- Final fleet allowlist and provenance reconciliation remain pending the dedicated skill/plugin task.
- No skill tree was installed, reseeded, removed, or changed in Task 2.

## v0.19.1 active D items

Inherited carry lineages remain `pending-re-audit`. The new D1 is implemented and technically verified on the candidate, but Task 5 owner acceptance remains pending. A familiar v0.18.2 patch is not authority to replay it.

| Current ID | Work item | Previous release | Current status | Next action |
|---|---|---|---|---|
| D1 | CJK-aware offline session recovery | New v0.19.1 defect discovered in Task 5 | `verification-pass-awaiting-owner-acceptance` | Commit the authorized candidate change, capture final local evidence, and request Task 5 acceptance. |
| D2 | OpenAI Codex credential pinning and labelled reauth | `v0.18.2/D8` | `pending-re-audit` | Capture v0.19.1 overlap and missing pin/fail-close behavior, then request one owner direction. |
| D3 | Discord thread ownership and role-mention fail-close | `v0.18.2/D4` | `pending-re-audit` | Probe ownership/free-response/mention safety against new Discord recovery and media paths. |
| D4 | Kanban same-card review and workflow seams | `v0.18.2/D2` | `pending-re-audit` | Audit native review/repair/model/worktree behavior before testing remaining Root Kernel seams. |
| D5 | CLI return-code passthrough | `v0.18.2/D6` | `pending-re-audit` | Trace the v0.19.1 process boundary and reproduce exact integer/bool behavior. |
| D6 | Doctor optional tool warning filter | `v0.18.2/D7` | `pending-re-audit` | Probe enabled versus disabled/default-off tool diagnostics without hiding new doctor checks. |

D1 retirement requires an exact later upstream target where CJK-enabled `hermes sessions recover` preserves canonical counts, reports `complete: true`, passes an equivalent CJK recovery regression, and leaves no Root Kernel-only behavior gap. A nearby CJK change, issue closure, or symbol match alone does not retire it.

For every D item:

1. Record upstream v0.19.1 symbols and behavior.
2. State the current Root Kernel requirement.
3. Identify exact overlap and remaining gap.
4. Stop for owner direction: adopt, replace, retain-minimal, retire, or defer.
5. Require clean-base RED evidence before retaining code.
6. Record GREEN and integrated smoke evidence after implementation.
7. Keep live mutation false throughout candidate work.
8. Update this document and `carry.yaml` together.

## Historical retired v0.18.2 entries

These entries remain historical and are not active v0.19.1 D items:

- `v0.18.2/D1` — Tool Search pair — retired; do not replay without a new independent regression.
- `v0.18.2/D3` — Kanban assignee alias dispatch seam — retired; do not replay without a new independent regression.
- `v0.18.2/D5` — Support-only plugin strategy — retired; do not replay without a new current consumer and independent decision.

The v0.19.1 numbers D1, D3, and D5 identify different active work items from the identically numbered v0.18.2 history. Historical and current numbering must never be conflated.

## Post-live R gates

R gates are not candidate-construction tasks. All are reset to `pending` and remain blocked until `rk/live` activation.

| Gate | Scope | Status | Acceptance |
|---|---|---|---|
| R1 | Config/profile activation policy | `pending` | Separate owner acceptance required |
| R2 | Skill provenance, overrides, and compatibility | `pending` | Separate owner acceptance required |
| R3 | Dashboard and Desktop | `pending` | Separate owner acceptance required |
| R4 | Cron, local scripts, watchers, and automation | `pending` | Separate owner acceptance required |
| R5 | Profile-owned local asset optimization | `pending` | Separate owner acceptance required |

Only one R gate may be active at a time. Technical success is not acceptance.

## Activation and rollback boundaries

Activation remains blocked until all of the following pass:

- D1–D6 each have an explicit owner direction and current evidence.
- Candidate-focused, state, skill, automation, gateway, and rollback smokes pass.
- The 49-profile semantic config outcome is approved, including STT language.
- A typed, non-secret rollback package is created and restored in a disposable path.
- Any real state database backup/canary has separate sensitive-data approval.
- External control is ready for the root no-self-restart boundary.

No `.env`, `auth.json`, token, credential pool, private key, or real state database may be copied into this repository or ordinary evidence.

## Ledger parity checklist

Before every commit-ready report, compare this document and `root-kernel/carry.yaml` for:

- target and previous baselines;
- local and remote ref observations;
- current D ID and previous-release lineage;
- D and R status;
- tag and activation blockers;
- evidence paths;
- live-mutation state;
- rollback authority;
- next action.

## Next action

Task 5 and D1 technical result:

- first planned test run: 79 passed, 0 failed; post-D1 run: 80 passed, 0 failed;
- direct schema 16→23 and 19→23: pass with all synthetic session/message counts preserved;
- Korean and English search, FTS conversion/rebuild, malformed/index-only recovery, read-only preflight, WAL fallback, zeroed-file quarantine, and exact backup-only rollback: pass;
- RED default CJK-enabled offline recovery: both schemas reproduced 0 of 5 messages and `complete: false` while preserving the source;
- GREEN default CJK-enabled offline recovery: both schemas preserve 5 of 5 messages, report `complete: true`, pass CJK integrity and Korean search, and preserve the source without a config toggle;
- focused regression 1/1, full recovery file 4/4, `py_compile`, `ruff`, diff, static security, candidate CLI import, and independent read-only review all pass;
- actual profile databases were not opened or copied; 73 SQLite connections stayed under the disposable root or in memory; live code and gateway remain unchanged.

Task 5 is technically `verification-pass-awaiting-owner-acceptance`; technical success is not acceptance. The owner authorized the minimum D1 implementation and selected commit subject `[D1] CJK-aware offline session recovery`. Task 6, D2–D6 work, inactive-profile state canary, live mutation, tag, push, and remote-ref movement remain unauthorized.
