# Root Kernel Hermes Agent v0.20.5 Candidate Guide

This document describes the current Root Kernel v0.20.5 candidate and the user-visible contracts planned for the release. It is not the historical release ledger. The complete v0.19.1 history remains authoritative at `rk/tag/v0.19.1`.

## Documentation map

| Document | Audience | Purpose |
|---|---|---|
| `root-kernel/feature.md` | Users and operators | Current candidate behavior, planned Root Kernel differences, configuration, and operating boundaries |
| `root-kernel/ledger.md` | Maintainers and owner | Release decisions, gate status, verification, publication, activation, and rollback |
| `root-kernel/carry.yaml` | Automation and reviewers | Machine-readable carry state, lineage, allowed paths, evidence, and retirement rules |

Do not recreate `for-root-kernel.md`.

## Current candidate baseline

- Candidate branch: `rk/v0.20.5`
- Candidate HEAD before this scaffold: `fcbd1076a93841fa88855acce810e342a5b78101`
- Upstream package: Hermes Agent `0.20.5`
- Upstream tag: `v2026.8.19`
- Annotated tag object: `b05e680e63d39d5a8e3ec0f5842a41d1c4209c03`
- Peeled release commit: `fcbd1076a93841fa88855acce810e342a5b78101`
- Signature claim: unsigned or unverifiable; only object, commit, and package identity are verified
- Live release remains `v0.19.1` on `rk/live` at `7e65112b5303e9aa30cda440c2ab498bf5f360bc`

The candidate now includes owner-accepted D1, D2, D3, D4, and D6 behavioral carries. Do not activate or advertise the release until S8 independent review and every later activation gate are complete and separately authorized.

## Candidate differences at a glance

| ID | Planned release contract | Current candidate status | Configuration impact |
|---|---|---|---|
| D1 | CJK-aware offline session recovery | Implemented, reviewed, owner-accepted | Automatic |
| D2 | Skill writes fail closed when the approval boundary is unavailable | Implemented, reviewed, owner-accepted | Uses upstream skill-write approval setting |
| D3 | Exact profile-local OpenAI Codex credential pinning and labelled reauth | Implemented, reviewed, owner-accepted | Profile-local ID/label pin settings |
| D4 | Discord thread ownership, role-mention fail-close, and optional owned free-response auto-threading | Implemented, reviewed, owner-accepted | First-owner-wins shared registry; live/recovery parity |
| D6 | Bool-safe CLI return-code propagation | Implemented, tested, reviewed, and owner-accepted | Automatic |

## Explicitly omitted downstream behavior

### D5: Root Kernel Kanban extensions

D5 is not part of v0.20.5. The candidate must use native upstream Kanban behavior and migrations. No downstream Kanban product, schema, CLI, tool, prompt, watcher, dispatcher, or test change is allowed.

Omitting D5 does not remove Kanban. Upstream v0.20.5 provides durable multi-board state, review dispatch, worktree lifecycle, notification, concurrency, and dispatcher recovery. It removes only the Root Kernel-specific same-card lifecycle, result watcher, mutex, and closed workflow-banner carries from the current feature contract.

### D7: doctor warning filtering

D7 is not part of v0.20.5. Upstream doctor output is accepted as-is. Root Kernel will not patch doctor merely to hide default-off or unavailable-tool warning rows.

## D1 candidate behavior: CJK-aware offline recovery

Exact v0.20.5 reproduced a connection-local tokenizer gap: CJK-enabled recovery returned `no such tokenizer: cjk_unicode61` while copying messages. D1 now ensures that a separate-output `hermes sessions recover` operation:

- preserves canonical session and message counts;
- reports completion correctly;
- leaves the source database unchanged;
- preserves integrity and CJK FTS behavior;
- can search Korean/CJK text after recovery;
- loads the existing CJK extension only at the normal destination, lost-and-found destination, and final verification SQLite connection boundaries.

No new user setting is introduced. `HERMES_CJK_FTS` and `HERMES_FTS5_CJK_SO` retain their existing behavior, including best-effort fallback when the feature is disabled or the extension is unavailable. D1 passed focused RED/GREEN, adjacent regressions, independent review, and owner acceptance on 2026-08-24.

## D2 candidate behavior: fail-closed skill writes

D2 changes only failure behavior at the skill-write approval availability boundary:

- approval-gate import, initialization, or evaluation failure blocks mutation;
- approved replay bypass and normal allowed/staged/blocked paths remain unchanged;
- the default approval setting is not changed by Root Kernel.

The exact v0.20.5 candidate reproduced an import fail-open and an evaluator exception escape. D2 now returns a structured blocking tool error before mutation for both failures. Normal allow, staged review, explicit block, and approved replay behavior remain governed by the upstream approval implementation. D2 passed independent review without blocking findings and received owner acceptance on 2026-08-24.

## D3 candidate behavior: exact Codex credential ownership

The v0.20.5 credential pool supports richer rotation, cooldown, refresh, and profile attribution, but exact target testing reproduced sibling and singleton substitution plus append-only labelled reauth. D3 now enforces this profile-local ownership contract:

- an exact configured credential ID wins;
- a label must resolve uniquely;
- an unavailable, dead, exhausted, missing, or ambiguous pin fails closed;
- no sibling credential or singleton fallback substitutes for a configured pin;
- labelled reauth updates the exact pinned row;
- unpinned profiles retain native v0.20.5 pool rotation and failover.

The active profile `.env` may set `HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID` or `HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL`; exact ID takes precedence. The process ambient environment does not configure these pins. Secret values remain in the owning profile’s approved credential storage and must never enter these documents, evidence, logs, or backups.

## D4: Discord ownership and role fail-close

Upstream v0.20.5 adds Bot Mode, group-room behavior, profile-scoped sessions, richer thread handling, and mention routing. Root Kernel must not fork or replace those systems.

The completed D4 implementation closes only the owner-required gaps:

- thread participation does not grant default-responder ownership;
- ownership is keyed to the numeric responder identity, shared across profiles, and survives recovery/restart;
- recovered messages respect the same ownership admission rule;
- unsafe role-only mentions fail closed;
- admitted live and recovered ingress claim one persistent first owner only after every routing gate passes;
- free-response auto-threading is retained only for an owned message and fails closed if thread creation fails.

Generic outbound forum text/media and handoff thread creation remain native transport operations; absent admitted ingress they do not claim default-responder ownership and are outside D4's ownership-creation scope. Participation alone never grants ownership.

## D6: bool-safe process exits

The actual-process contract was RED because Python treats `bool` as an `int`; the top-level handler-return boundary is now narrowed so that:

- `None`, `False`, `True`, zero, and non-integer values remain process success unless another native path raises an exit;
- only an exact nonzero integer propagates as the process exit code;
- argparse exits, handler-raised `SystemExit`, and ordinary native nonzero command returns remain unchanged.

No setting is required.

## Release and operating invariants

- Historical patches are evidence, not implementation authority.
- Each carry must be reproduced against exact v0.20.5 before code changes.
- Each retained carry uses a focused RED test, the smallest GREEN change, adjacent regressions, documentation parity, and a separate owner gate.
- Only the allowed D1–D4/D6 source and test paths plus these three documents may differ from upstream.
- No downstream D5 Kanban or D7 doctor code may appear.
- The candidate is not published, tagged, live, or installed merely because this branch exists.
- `rk/v0.20.5`, planned `rk/tag/v0.20.5`, and `rk/live` may converge only after integrated acceptance.
- The literal exceptional ref `rk/tags/v02.20.5` must not be created without explicit owner direction.

## Runtime and rollback boundary

The live clone remains `/Users/draccoon/.hermes/hermes-agent` on v0.19.1. This scaffold does not change profiles, configuration, state databases, credentials, plugins, skills, cron jobs, gateways, services, launchers, remote refs, or the live checkout.

The preflight dirty state is preserved at:

`/Users/draccoon/Workspace/Hermes/backups/20260824-030645-rk-v0205-preflight`

The v0.20.5 carries are committed as seven logical checkpoints above upstream target `fcbd1076…`. Production rollback restores remote `rk/live` and the live clone to v0.19.1 commit `7e65112b…`, then restores the matching v23 profile snapshots from `/Users/draccoon/Workspace/Hermes/backups/20260825-031813-v0205-live-activation/` only while all writers are stopped.

## Next gate

D1, D2, D3, D4, D6, and S8 are owner-accepted. S9 activation preparation passed. The owner authorized S10 on 2026-08-25; `rk/v0.20.5`, annotated tag `rk/tag/v0.20.5`, and `rk/live` were promoted, and the live clone was updated from v0.19.1 to v0.20.5. S11 passed with all four profiles on config schema 38 and state schema 26, integrity OK, zero foreign-key violations, four gateways running from the live venv, and successful identity/model probes for 문앙(Munang), 공명(Gongmyeong), 월영(Wolyeong), and 사마의(Samaui).
