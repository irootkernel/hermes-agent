# Root Kernel Hermes Agent v0.19.1

## Release state

- Status: `scaffolded-pending-upstream-evidence`
- Candidate branch: `rk/v0.19.1`
- Candidate worktree: `/Users/draccoon/Workspace/Hermes/17th-hermes-agent-worktree`
- Tag blocker: `true`
- Live activation: not started
- Commit: authorized for this Task 2 ledger-only first commit at `2026-08-02T17:34:44+09:00`
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
- Planned release-note evidence:
  - `root-kernel/evidence/release-note-v2026.7.20.md`
  - `root-kernel/evidence/release-note-v2026.7.30.md`
- Planned exact-delta evidence:
  - `root-kernel/evidence/upstream-delta-v2026.7.7.2-to-v2026.7.30.md`
  - `root-kernel/evidence/upstream-delta-v2026.7.7.2-to-v2026.7.30.json`
  - `root-kernel/evidence/v0.19.1-config-state-skill-signals.md`

These evidence files are pending Task 3 and must not be represented as already captured.

## Candidate and live-mutation boundary

The candidate currently equals the clean peeled upstream tag before Root Kernel scaffold changes. Task 2 adds only:

- `for-root-kernel.md`
- `root-kernel/carry.yaml`

No carry code, test port, profile, config, state database, skill installation, plugin, cron job, gateway, credential, live checkout, remote ref, or tag was changed by this scaffold task. The owner separately authorized one ledger-only first commit after Task 2 verification.

Rollback for the scaffold is to discard these two files before commit or revert the ledger-only Task 2 commit afterward. Rollback for later code work remains branch switch to `rk/v0.18.2`. Live rollback remains anchored by the separate live clone and preserved release refs.

## Config, state, and skill signals

These values are the completed planning baseline. Fleet values must be refreshed read-only in their dedicated tasks before activation.

### Configuration

- Profiles in planning baseline: 49.
- All 49 observed configs: `_config_version: 33` and `approvals.mode: manual`.
- v0.19.1 source default config version: 33. An unchanged schema number does not imply unchanged behavior.
- All 49 observed `agent.max_turns` values are explicit, between 80 and 220; v0.19.1 source default is 500 and must not replace them.
- Observed compression thresholds are explicit: 46 profiles at 0.85 and 3 at 0.7.
- All 49 observed configs omit `stt.language`; v0.19.1 globally defaults it to `en`.
- Owner-approved STT policy is pending: `ko` for Korean-only, empty string for auto-detect/multilingual, or `en` for English-only.
- `gateway.multiplex_profiles` and `profile_routes` remain inactive.
- Root default remains messaging-tokenless and gateway-disabled unless separately authorized with distinct Munang credentials.

### State

- Planning baseline: 12 databases at schema 19 and 37 at schema 16.
- v0.19.1 source target: schema 23, verified at `hermes_state_common.py::SCHEMA_VERSION`.
- Direct 16→23 and 19→23 migration, Korean search, recovery, WAL behavior, and rollback remain unproven until isolated Task 5 evidence passes.

### Skills

- v0.19.1 bundled source contains exactly 70 `SKILL.md` files; this count was rechecked on the candidate.
- Final fleet allowlist and provenance reconciliation remain pending the dedicated skill/plugin task.
- No skill tree was installed, reseeded, removed, or changed in Task 2.

## v0.19.1 active D items

All active carry lineages are reset to `pending-re-audit`. A familiar v0.18.2 patch is not authority to replay it.

| Current ID | Work item | Previous release | Current status | Next action |
|---|---|---|---|---|
| D1 | OpenAI Codex credential pinning and labelled reauth | `v0.18.2/D8` | `pending-re-audit` | Capture v0.19.1 overlap and missing pin/fail-close behavior, then request one owner direction. |
| D2 | Discord thread ownership and role-mention fail-close | `v0.18.2/D4` | `pending-re-audit` | Probe ownership/free-response/mention safety against new Discord recovery and media paths. |
| D3 | Kanban same-card review and workflow seams | `v0.18.2/D2` | `pending-re-audit` | Audit native review/repair/model/worktree behavior before testing remaining Root Kernel seams. |
| D4 | CLI return-code passthrough | `v0.18.2/D6` | `pending-re-audit` | Trace the v0.19.1 process boundary and reproduce exact integer/bool behavior. |
| D5 | Doctor optional tool warning filter | `v0.18.2/D7` | `pending-re-audit` | Probe enabled versus disabled/default-off tool diagnostics without hiding new doctor checks. |

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

The v0.19.1 numbers D1, D3, and D5 identify different active work items. Historical and current numbering must never be conflated.

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

- D1–D5 each have an explicit owner direction and current evidence.
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

Task 2 verification passed: YAML parsing, baseline parity, D-item lineage/status parity, R1–R5 pending status, evidence-path parity, and trailing-whitespace checks all succeeded.

The next allowed task is Task 3: capture exact upstream release-note, delta, and config/state/skill evidence. No D-item implementation or live mutation is authorized by this scaffold.
