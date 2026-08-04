# Root Kernel Hermes Agent v0.19.1

## Release state

- Status: `d5-complete-owner-accepted-awaiting-d6-direction`
- Candidate branch: `rk/v0.19.1`
- Candidate worktree: `/Users/draccoon/Workspace/Hermes/17th-hermes-agent-worktree`
- Tag blocker: `true`
- Live activation: not started
- Previous Task 2 commit: `509ae0f6d1c5ea9f7dfb9a77a965614dd91b16ff`
- Task 3 ledger commit: `53e6060682a8dc98df6a30ef671b2ecb53c2384e`
- Current D1 commit: this ledger commit; exact SHA is recorded in Git and the excluded D1 evidence
- Task 4 evidence: local progress-only and Git-excluded; accumulated ledger updates are included in the authorized D1 commit scope
- Task 4 accepted by owner at `2026-08-02T19:33:32+09:00`, including the recorded 47-profile YAML formatting caveat
- Task 5 and D1 accepted by owner at `2026-08-02T23:25:52+09:00`; Task 6 read-only reconciliation authorized
- Task 6 accepted and D2 minimal fail-closed implementation/commit authorized by owner at `2026-08-03T00:41:48+09:00`; commit header must be `[D2]`
- D2 accepted by owner at `2026-08-03T01:14:44+09:00`; D3 was then authorized for a clean retain-minimal reimplementation
- D3 implementation, focused verification, independent review correction, typed rollback, and scoped commit completed at `2026-08-03T10:31:22+09:00`
- D3 accepted by owner at `2026-08-03T11:38:26+09:00`
- D4 read-only re-audit authorized and started at `2026-08-03T11:38:26+09:00`; overlap/gap evidence completed at `2026-08-03T11:56:43+09:00`; owner selected option A and authorized minimal v0.19.1-aware implementation
- D5-e commit and owner acceptance were both explicitly conveyed by the owner's commit direction at `2026-08-04T15:27:26+09:00`; this is the self-recording `[D5]` commit
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
- Task 5 technical verification passed and the owner accepted it at `2026-08-02T23:25:52+09:00`. No inactive real-profile canary was authorized or required because the synthetic paths and strict SQLite path guard provide sufficient D1 evidence.
- Owner direction: retain this minimal candidate runtime fix as current v0.19.1 D1, commit it as `[D1] CJK-aware offline session recovery`, and retire it after an exact upstream replacement is proven.

### Skills

- v0.19.1 bundled source contains exactly 70 `SKILL.md` files; the exact path, frontmatter, SKILL.md, and package hashes are recorded in `root-kernel/evidence/v0.19.1-skill-delta.json` (`4791ad338be5f017f42d13ff9ff9240d8a8137fa9e1f6f3a4a5c32e3843d1de3`) and summarized in `root-kernel/evidence/v0.19.1-skill-provenance.md` (`2a0c413ef67e129ba79a26fb1ad222b6367989651af3eac49c9e2517e6091bf3`).
- Task 6 reconciled 72→70 bundled, 102→111 official optional, and 88→95 plugin manifests. The accepted optional retention baseline remains zero.
- All 49 homes still contain 72 byte-exact v0.18.2 bundled skills with zero extra roots, archives, or no-bundled markers. No skill tree was installed, reseeded, removed, or changed in Task 6.
- The closed allowlist target is 70 exact bundled per profile, managed fleet 5, default-only admin 10, optional 0, local custom 0, and no retired plugin skills. Actual re-seeding remains post-live R2 work.
- Curator protection must set `curator.prune_builtins: false` and require zero `.curator_suppressed` files during R2. `skills.write_approval: true` alone does not intercept deterministic curator pruning and can also fail open if its approval helper cannot import; the latter is current D2.

## v0.19.1 active D items

Inherited carry lineages remain `pending-re-audit` until their own gate starts. D1–D5 are owner-accepted. D5-a through D5-e were already committed; D5-f product, tests, and both ledgers are committed together in this self-recording commit. D6–D7 remain blocked pending separate direction. A familiar v0.18.2 patch is not authority to replay it.

| Current ID | Work item | Previous release | Current status | Next action |
|---|---|---|---|---|
| D1 | CJK-aware offline session recovery | New v0.19.1 defect discovered in Task 5 | `implemented-verified-task5-accepted` | Keep active until an exact upstream replacement satisfies the recorded retirement rule. |
| D2 | Fail-closed skill write approval import boundary | New v0.19.1 defect discovered in Task 6 | `implemented-verified-owner-accepted` | Keep active until an exact upstream fail-closed replacement is behaviorally verified. |
| D3 | OpenAI Codex credential pinning and labelled reauth | `v0.18.2/D8` | `implemented-verified-owner-accepted` | Keep active until an exact upstream replacement satisfies the retirement rule. |
| D4 | Discord thread ownership and role-mention fail-close | `v0.18.2/D4` | `implemented-verified-owner-accepted` | Closed; preserve until an exact upstream replacement is verified. |
| D5 | Kanban same-card review and workflow seams | `v0.18.2/D2` | `implemented-verified-self-recording-commit-owner-accepted` | Closed; await explicit D6 re-audit direction. |
| D6 | CLI return-code passthrough | `v0.18.2/D6` | `pending-re-audit` | Trace the v0.19.1 process boundary and reproduce exact integer/bool behavior. |
| D7 | Doctor optional tool warning filter | `v0.18.2/D7` | `pending-re-audit` | Probe enabled versus disabled/default-off tool diagnostics without hiding new doctor checks. |

### D5-b implementation result

- Implemented the same-card core loop: owned cooperative handoff, native submit-review, exact reviewer request-changes, and creator final-gate routing. D5-c through D5-f remain blocked and untouched.
- Added worker-only `kanban_reassign`, `kanban_submit_review`, and `kanban_request_changes` surfaces with delegated-child denial, own-task/run ownership, force-redacted metadata, spawnable distinct targets, and explicit nonterminal outcomes.
- Added terminal parity through `hermes kanban handoff`, `submit-review`, and `request-changes`; every active transition requires an explicit matching `--run-id`.
- Added nullable `tasks.review_submission_event_id` with additive migration after independent review reproduced stale nearest-event reuse and legacy/manual review lockout. Native claims validate the exact event; legacy claims complete normally without native request-changes/final-gate authority. Reclaimed native review retries preserve the exact link.
- Creator routing occurs before final completion artifacts, `completed_at`, result persistence, dependent promotion, scratch cleanup, and completion hooks. Ordinary completion now compare-and-sets its captured status/run to close the preflight/write race.
- Goal mode refuses missing, malformed, zero, or negative dispatcher run ids and rechecks ownership immediately after judging and before another model turn.
- Verification: focused `109 passed, 1 skipped`; canonical file-isolated broad gate across 34 files `206 passed, 1 skipped`, with zero failed files. The raw one-process collection retained the exact same seven baseline collection-order failures and added no new failing node. Syntax, Ruff, and diff whitespace checks passed.
- Rollback: pre-implementation archive SHA-256 `28c0785c9c589eaac13628fc2757260eb835e86a43bca9ed066c6fa313523f46`; disposable restore matched ten targets byte-for-byte and passed 61 restored tests. Restored D5-a code also opened and mutated a disposable D5-b-migrated DB successfully, proving nullable-column rollback compatibility.
- First independent implementation review found six concrete issues; all were reproduced and remediated. A final read-only Claude Code review returned `PASS` with zero blocking findings; its metadata-redaction nit was also changed to fail closed and regression-tested.
- Evidence: `root-kernel/evidence/v0.19.1-D5-b-core-same-card-loop-investigation.json`, SHA-256 `c9a53df199b46cfe1a4636fe1e4ee3cd63a694d05ed8ab8449fd1b0e1a3dbb26`.
- Boundary: no production board, dispatcher, gateway, profile, token, or live runtime was mutated. D5-b is committed in this self-recording commit; that commit did not authorize D5-c, whose later implementation authorization and result are recorded below.

### D5-c implementation result

- Restored the review outcome watcher without replaying the historical patch directly. `kanban_submit_review` first reports an existing durable task subscription, then uses only a complete trusted gateway source or a TUI session key for a best-effort fallback. `HERMES_SESSION_ID` remains telemetry-only, partial gateway identity fails closed, and the historical `review_watch` receipt shape is preserved.
- Added a same-task `submitted_review` cursor anchor to `add_notify_sub` without a schema change. Foreign-task and malformed anchors fail closed. A same destination race atomically applies `MIN(existing_cursor, anchor)` so a fast review outcome cannot be skipped, while ordinary duplicate subscriptions keep their existing cursor.
- Added `requested_changes` and `review_accepted` delivery and wake behavior to the profile-aware multi-board gateway notifier and the TUI poller. Both outcomes retain the subscription until the task reaches `done` or `archived`; push failure rewind and non-push wake-before-cursor foundations remain unchanged.
- Review-watch lookup, anchor, attach, and receipt work is isolated behind a best-effort boundary after the D5-b transition. A watcher failure cannot report a successful review transition as failed or attach a different fallback destination after an indeterminate existing-subscription lookup.
- Verification: focused `89 passed, 1 skipped`; canonical file-isolated Kanban broad gate across 49 files `298 passed, 1 skipped`, with zero failed files; i18n catalog parity `36 passed`; `py_compile`, Ruff, `git diff --check`, and added-line security scan passed.
- Rollback: pre-implementation archive SHA-256 `adf3e52e24768f270fc0a5f662a967466ff4c55b79d479db2f9fbbc31dded049`; disposable restore was clean and passed 89 baseline tests. Pre-D5-c code reopened a disposable D5-c-written DB, observed the anchored review outcome, then created and claimed another task successfully.
- Independent review: first pass found two concrete races; both were reproduced and remediated. The read-only follow-up returned `PASS` with zero blockers and reran the two remediation tests successfully.
- Evidence: `root-kernel/evidence/v0.19.1-D5-c-review-outcome-watcher.json`, SHA-256 `13e330a75729527ac14118670407a36de2902015fff1382e68f06c2afe5aa110` (local, Git-excluded evidence; publication is not authorized).
- Boundary: no production board, dispatcher, gateway runtime, profile, registry, alias, token, skill, cron, or live ref was mutated. D5-c is committed in this self-recording commit; at D5-c closeout, D5-d remained separately approval-gated and had not started.

### D5-d implementation result

- Added native worker-only `kanban_submit_result` and `hermes kanban submit-result` surfaces. Submission requires the worker's exact active run, defaults the distinct spawnable acceptor to the creator, uses the existing exact `review_submission_event_id`, and adds no schema.
- Result provenance now binds the `submitted_result` event to the exact released implementation run and submitter. Request-changes can return only to that submitter; creator/acceptor approval emits ordinary `completed`, never `review_accepted`, and goal-mode acceptance still runs the completion judge.
- Declared scratch artifacts remain in-flight through submission and are copied only during successful final acceptance. Missing files, oversized files, symlink escapes, copy failures, transaction rollback, ambiguous COMMIT outcomes, post-COMMIT validation failures, and `BaseException` interrupts preserve a fail-closed DB/filesystem relationship without deleting durable references or leaving partial copies.
- Reused D5-c's durable watcher and exact `submitted_result` cursor foundation without gateway or TUI product changes. Terminal and run-release tools suppress the worker stop nudge only after an actual `ok: true` result; failed calls continue the bounded retry nudge.
- Verification: focused 8-file suite `213 passed, 1 skipped`; canonical file-isolated Kanban broad gate across 42 files `269 passed`, with zero failed files. `py_compile`, Ruff, `git diff --check`, added-line security scan, and Bandit delta comparison passed; Bandit matched HEAD at 54 findings with zero high severity and no added distribution.
- Rollback: pre-implementation archive SHA-256 `2974e8fde1d3813861df15ba040935e5eebddabb94f733d430b6542b0674814e`; prompt-test supplement SHA-256 `a6477156e696e3f447ba94c0222efb9ebd44e489b73bfbfcc7d7f67d32b4d1ee`; disposable restore matched all 16 targets byte-for-byte against HEAD.
- Independent review reproduced eight blockers across provenance, rework routing, acceptance reclaim, artifact durability, interrupt cleanup, and stop-guard success detection. Every finding was RED-tested and remediated; the final focused read-only follow-up returned `PASS` with zero blockers.
- Evidence: `root-kernel/evidence/v0.19.1-D5-d-result-submission.json`, SHA-256 `aef2b114fd01215e023db82900f7bbed88fc4c99a214d48bc00382df674e239e` (local, Git-excluded evidence; publication is not authorized).
- Boundary: no production board, dispatcher, gateway runtime, profile, registry, alias, token, skill, cron, or live ref was mutated. D5-d is committed in this self-recording commit; D5-e remains separately approval-gated and has not started.
- Owner acceptance: 주군 accepted committed D5-d by explicitly directing the next D5-e gate to start at `2026-08-04T13:08:11+09:00`.

### D5-e investigation and implementation result

- Historical contract: commit `0361594452e9329bfe7d32be1e0a853cd4c810a2` adds an explicit board-local `mutex_key`, trim/blank normalization, ready/review direct-claim guards, same-tick dispatch deferral, health suppression, CLI/tool create surfaces, and a non-unique lookup index. All `12` focused tests passed in `1.27s`; an added 20-trial multi-connection race probe produced exactly one claim, one running row, and one structured rejection every time.
- Direct replay is rejected: `git apply --check` failed on every historical product, test, and ledger hunk because current v0.19.1 chokepoints changed.
- Current gap: a disposable expected-contract probe failed all `9` contracts. After a test-only column was added, two same-key tasks both reached `running` through separate direct claim connections; ready and review claims both bypassed serialization; a same-tick dry run selected both; health still called the deferred queue spawnable; model/schema/CLI/tool surfaces are absent.
- Native foundations preserved: board-scoped dispatch lock, hardened `BEGIN IMMEDIATE` transaction boundary, per-profile cap, tools, project links, and worktree isolation passed `55` current tests. The dispatch lock is only a partial foundation because terminal/external direct claims bypass it; `write_txn` is the correct authoritative race boundary.
- Option comparison: a disposable application-guard prototype passed `20/20` simultaneous claim trials while preserving `Optional[Task]` and structured rejection semantics. A partial unique index failed closed but raised `IntegrityError`, produced no `claim_rejected` receipt, and changes rollback caller behavior. A separate lock table duplicates run/reclaim state; dispatcher-only filtering leaves direct claims open.
- Recommended solution: retain a minimal v0.19.1-aware application guard. Add nullable `tasks.mutex_key`, a non-unique `(mutex_key, status)` lookup index, trim-only normalization, and ready/review owner checks inside the existing `write_txn`. Use indexed exact lookup normally, then defensively normalize remaining running-row keys so whitespace-bearing carried/manual values cannot bypass direct claims; do not rewrite existing DB values. Keep dispatcher owner-map filtering for same-tick scheduling and `skipped_mutex_locked` diagnostics, but keep the direct claim guard authoritative. The key is board-local and explicit, preserves case/schemes, and promises mutual exclusion only while work is `running`, not fairness or a reservation during review wait.
- Surface scope: `hermes_cli/kanban_db.py`, `hermes_cli/kanban.py`, and `tools/kanban_tools.py`, plus their three existing test files and both ledgers. Exclude D5-f prompt/context banners. Dashboard task reads naturally gain the dataclass field through `asdict`; dashboard create UI/API expansion remains outside the inherited D2-h contract.
- Required implementation evidence: fresh/legacy and existing-carried-column migration, normalization/event provenance, dirty whitespace-bearing stored-key consistency, documented no-length-cap behavior, CLI/tool parity, simultaneous ready/review claims, existing-owner and same-tick dry/live dispatch, health suppression, unlock through complete/block/review/result/failure/stale exits, unrelated/different-board behavior, pre-existing duplicate-owner characterization without silent repair, all current concurrency/worktree/D5-b/c/d regressions, and pre-D5-e code reopening and mutating a migrated disposable DB.
- Rollback: non-secret ledger backup `/Users/draccoon/Workspace/Hermes/update-backups/20260804T040811Z-rk-v0191-d5e-investigation/d5e-ledgers-pre-investigation.tar.gz`, SHA-256 `b6dce8a8a8c25b67a9bc78c0d5c3aa926edd107cd0d1b51813ddc43a8cc5f4d1`; byte restore passed. A disposable additive-column/non-unique-index DB remained readable and writable by pre-D5-e code.
- KSCQ: query `mutex key serialization kanban concurrency` returned no indexed learning note; repository source and executable probes determined the recommendation.
- Implementation: added nullable board-local `mutex_key`, trim-only/blank normalization, additive migration, non-unique partial lookup index, atomic ready/review direct-claim guards, same-tick ready/review dry/live dispatcher serialization, mutex-aware health suppression, and CLI/tool create and diagnostic parity. Ownership exists only while a task is `running`; case and schemes remain distinct.
- Carried/manual safety: the authoritative exact query now uses `idx_tasks_mutex_status`. Canonically stored exact owners deterministically precede whitespace-bearing dirty variants; dirty fallback still fails closed when no exact owner exists, and stored values are never rewritten. Existing duplicate running owners are not silently repaired and block new claims.
- Verification: final focused suite `30 passed, 101 deselected`; product-adjacent three-file suite `131 passed`; canonical file-isolated Kanban broad gate across 49 files `349 passed, 1 skipped`, with zero failed files. A real two-connection ready race passed `50/50`; review race, ready/review cross-lane dry/live, 120,009-character CLI JSON round-trip, migration preservation, and complete/result/block/failure/manual/stale/timeout/crash release paths passed. `py_compile`, Ruff, `git diff --check`, added-line security, and Bandit delta passed; Bandit matched HEAD at 52 findings with zero high severity and no new findings.
- Rollback: non-secret pre-implementation archive `/Users/draccoon/Workspace/Hermes/update-backups/20260804T045524Z-rk-v0191-d5e-implementation/d5e-pre-implementation.tar.gz`, SHA-256 `0390df209bdb445da4c484990d225e0e50c0bf07746c303e6ec76f566eb52b2d`; hash verification and restored `102 passed` suite succeeded. Current D5-e code created the disposable DB, restored pre-D5-e code reopened it and created/claimed a task, and current code reopened it again with key preservation. The owner-authorized pre-commit eight-file backup is `/Users/draccoon/Workspace/Hermes/update-backups/20260804T062738Z-rk-v0191-d5e-precommit/d5e-precommit-files.tar.gz`, SHA-256 `7b44121e80aba8aa10b9427b4f14863493e9ce5a777237964f7000275a41ee0a`; disposable byte restore passed. The acceptance-semantics amend backup is `/Users/draccoon/Workspace/Hermes/update-backups/20260804T063404Z-rk-v0191-d5e-acceptance-correction/d5e-ledgers-pre-acceptance-amend.tar.gz`, SHA-256 `5f83cc1a08dd4d64532ec4134a972fad5a8d3ca7044dddac582b68590d4ec51c`; byte restore passed and pre-amend commit `5f5f1e23097ec0d89e81889fdd583405197e7617` remains recoverable from reflog.
- Independent review: two background read-only reviewers found the unused partial-index path, mixed dirty/exact owner-ID disagreement, and missing edge regressions. The two logic blockers were RED-reproduced, remediated, and permanently regression-tested. The final read-only Codex blocker follow-up returned `PASS` with zero security concerns, logic errors, or missing tests and modified no files.
- Evidence: `root-kernel/evidence/v0.19.1-D5-e-mutex-key-investigation.json`, SHA-256 `06a066ae2a2edd299563823b5162000a9ef01b58bff992c3a4b4d5dd83b3efa3` (local, Git-excluded; publication is not authorized).
- Boundary: D5-e is committed and owner-accepted by the same explicit commit direction. At D5-e closeout, push remained unauthorized and D5-f had not started; the later D5-f investigation authorization is recorded below. No production board, dispatcher, gateway runtime, profile, registry, alias, token, skill, cron, runtime, or live ref was read or mutated.

### D5-f investigation and solution result

- Owner direction: D5-f investigation, analysis, and solution proposal were explicitly authorized at `2026-08-04T15:41:39+09:00`; investigation completed at `2026-08-04T16:11:25+09:00`; implementation was explicitly authorized at `2026-08-04T16:30:18+09:00`. Commit, push, D6, D7, and all R gates remain unauthorized.
- Historical authority: final `v0.18.2/D2-i` commit `bc757256037e6ab0d5004e26c21b0b376597a3a3` added a separate nullable closed-enum `workflow_type`, seven static banners, fail-closed creation, persisted-value sanitization, worker-context rendering before Body, and CLI/tool surfaces. Its isolated rerun passed `10` focused tests and `597 passed, 1 skipped` broad tests.
- Native overlap: v0.19.1 `KANBAN_GUIDANCE` correctly documents generic current D5 lifecycle tools, but it does not persist a per-card protocol, color/review lane, fan-out/fan-in role, serial-chain role, or baton rule. `workflow_template_id` and `current_step_key` are future-v2 routing/stage identifiers with current filter/run-snapshot consumers; they are arbitrary metadata, not a closed prompt authority. Native overlap is partial, not a replacement.
- Current RED: disposable `/tmp/test_d5f_v0191_gap_probe.py` produced `7 failed in 1.91s`, proving the absence of `Task.workflow_type`, create/CLI/tool surfaces, closed registry, per-card worker-context banner, and any native/global replacement. Current native guidance/spawn checks passed `2`, confirming that the generic layer itself remains healthy.
- Compatibility: a real `historical D2-i → current candidate → historical D2-i` database sequence preserved the existing `workflow_type` column and `creator_accepted_work` bytes. Current code safely ignored the field and hid the banner; historical code reopened the same DB and restored the banner. This favors preserving the existing storage/user name rather than inventing a new incompatible one.
- Rejected options: retire loses per-card constraints; verbatim replay carries stale validation/index/copy; reusing native workflow metadata creates prompt-authority and future-v2 collisions; lifecycle inference is lossy and ambiguous.
- Recommended option: `retain-minimal-v0.19.1-aware-closed-workflow-context`.
  - Preserve `workflow_type` and CLI `--workflow-type` for v0.18.2 DB/user-surface compatibility, while documenting that it is a closed contextual key separate from native routing metadata.
  - Keep the seven historical values. Create-time `None` is allowed; any non-string, blank, or unknown value fails before idempotency lookup and before row/event writes. Persisted reads accept only actual known strings; hostile text, numeric, BLOB/bytes, and other values sanitize to null without `str()` coercion or raw-value leakage.
  - Render only static code-owned text in `build_worker_context` after task metadata and before Body. Do not change global `KANBAN_GUIDANCE`, system-prompt assembly, `_default_spawn`, D5-b–e transitions, or native workflow metadata.
  - Add nullable `workflow_type TEXT` only when absent; preserve an existing D2-i column and bytes; do not recreate the historical dead `workflow_type` index because no query consumes it.
  - Expose only canonical value or null through `Task`, created events, CLI create/list/show JSON, `kanban_create` schema/result, tool list/show, dashboard dataclass reads, and worker context.
- Required copy correction: the historical `creator_adjudicated_review` banner is wrong under current D5 semantics because it tells an active reviewer to call `kanban_submit_review`. The revised banner must direct rejection through `kanban_request_changes` and acceptance through `kanban_complete`. The disposable design spike passed all seven values, eight strict invalid types, five typed SQLite rows, before-Body ordering, and removal of the stale reviewer tool.
- Proposed implementation files: `hermes_cli/kanban_db.py`, `hermes_cli/kanban.py`, and `tools/kanban_tools.py`; focused tests in their three existing test files, with a dashboard read regression only if direct parity is not already covered.
- Required TDD: all seven banners; strict invalid types and idempotency ordering with zero writes; persisted hostile text/numeric/BLOB sanitization across every output; exact CLI/tool enum parity; no-key context byte parity; fresh/additive/repeated migration and no dead index; historical bytes; D5 transition preservation; native `workflow_template_id` / `current_step_key` and run `step_key` preservation; focused, product-adjacent, broad, static, security, and rollback gates.
- Independent review: read-only architecture review `019fcb91-78d5-70f0-8aed-e097d3efc081` recommended a minimal v0.19.1-aware redesign. Read-only security/regression review `019fcb97-b5f1-7441-a508-0f32c65542a1` found zero security blockers and one logic blocker, the stale reviewer tool instruction; the proposed copy and design spike correct it. No reviewer modified files.
- Evidence: `root-kernel/evidence/v0.19.1-D5-f-closed-workflow-context-investigation.json`, SHA-256 `05175e9e52710af037f68e9b15d3cb76aee0b60b8a7f3c4592c22446f6b0627c` (local, Git-excluded; publication is not authorized).
- Rollback: investigation backup `/Users/draccoon/Workspace/Hermes/update-backups/20260804T064139Z-rk-v0191-d5f-investigation/d5f-ledgers-pre-investigation.tar.gz`, SHA-256 `641269997f8349aa24e815fd038de53f2cfd9d170bbf6b42102b298489367e5a`; implementation preimage `/Users/draccoon/Workspace/Hermes/update-backups/20260804T073018Z-rk-v0191-d5f-implementation/d5f-pre-implementation.tar.gz`, SHA-256 `3204ce604459d95df101afee887ee74fe12290fb2c596e00b3b8995a44a3b669`. Both are non-secret and byte restore passed.
- KSCQ: query `closed workflow context banner kanban prompt workflow_type` returned no indexed learning note.
- Boundary and next action at investigation close: implementation was separately authorized and followed vertical TDD; the completed result is recorded below.

### D5-f implementation result

- Implemented the selected minimal v0.19.1-aware design in `hermes_cli/kanban_db.py`, `hermes_cli/kanban.py`, and `tools/kanban_tools.py`, with permanent regression coverage in their three existing test files. The closed contextual field remains separate from native future-v2 routing metadata.
- Added seven code-owned static workflow banners. Creation allows null and canonical known strings only; non-string, blank, unknown, and instruction-bearing values fail before idempotency lookup and before row/event writes. Persisted unknown text, numeric, BLOB/bytes, and arbitrary objects sanitize to null without string coercion or raw-value prompt/output exposure.
- `creator_adjudicated_review` now directs rejection through `kanban_request_changes` and acceptance through `kanban_complete`; it never directs an active reviewer to `kanban_submit_review`. Static workflow context renders before Body, and `agent/prompt_builder.py` / global `KANBAN_GUIDANCE` remain unchanged.
- Schema behavior is additive: fresh/legacy boards gain nullable `workflow_type TEXT` only when absent. Current code creates no workflow index; an existing historical `idx_tasks_workflow_type` is preserved rather than destructively dropped. Existing D2-i bytes remain unchanged.
- CLI `--workflow-type`, CLI create/show/list JSON, `kanban_create` schema/result, model-tool show/list, created-event provenance, sanitized `Task` reads, dashboard dataclass reads, and worker context now expose only a canonical value or null.
- Same-card implementation/reviewer request-changes and creator-result final acceptance tests preserve `workflow_type`, `workflow_template_id`, `current_step_key`, and every implementation/reviewer/acceptor run `step_key` snapshot.
- TDD and verification: feature-bearing DB, migration, CLI/tool, and lifecycle groups failed against the HEAD preimage before turning green; reversible no-workflow context and historical-index preservation were added as review-hardening relationship regressions. Final CI-parity focused gate passed `153`; the complete Kanban consumer gate passed `337` across `41` files with zero failures. Ruff, `compileall`, and `git diff --check` passed. `ty` remains baseline-red but improved from `121` changed-file diagnostics on HEAD to `83`; product-only remained `21 → 21` with no new diagnostic.
- A wider non-gating `tests/hermes_cli tests/tools` diagnostic run timed out at `600s` after unrelated existing environment failures for Daytona/Modal availability, macOS `/private/tmp`, systemd/D-Bus, and MCP timing. The bounded complete Kanban consumer gate above is green.
- Compatibility: a real `historical D2-i → current D5-f → historical D2-i` disposable DB sequence passed with workflow bytes, historical index, banner, and native metadata preserved. A HEAD/current no-workflow worker-context comparison was byte-identical at SHA-256 `54c7b3ca193010724a2ca23dd44bf3fb37d83d3167522ba66d74ec7ec9f64541`; a reversible add/remove relationship regression protects the repository path without freezing unrelated output text.
- Independent review: architecture/security final review `019fcbd7-2e76-7e70-9a22-9b227899f156` returned `PASS`. Test/migration first pass `019fcbdb-0933-74a0-b530-9fdcea900ce1` requested repository-anchored byte-stability and historical-index preservation coverage; these were resolved with the reversible relationship contract required by `AGENTS.md`, plus full creator-result acceptance coverage. Blocker follow-up `019fcbe7-454a-7992-be91-662934865f32` returned `PASS`. Precommit AGENTS review `019fcbfb-0bcd-7a40-84e8-da01b3068ee2` found only stale golden wording; after correction, follow-up `019fcc00-e1ba-7f82-8ddd-2f4befb75bdd` returned `PASS` with zero blockers. No reviewer modified files.
- Evidence: `root-kernel/evidence/v0.19.1-D5-f-closed-workflow-context-implementation.json`, SHA-256 `62415d80420aca6e587a86c7662518060ce3e75557d8b871a84ff80c61d01d65` (local, Git-excluded; publication is not authorized).
- Rollback: non-secret pre-implementation archive `/Users/draccoon/Workspace/Hermes/update-backups/20260804T073018Z-rk-v0191-d5f-implementation/d5f-pre-implementation.tar.gz`, SHA-256 `3204ce604459d95df101afee887ee74fe12290fb2c596e00b3b8995a44a3b669`; byte restore passed. The reviewed pre-authorization commit candidate archive is `/Users/draccoon/Workspace/Hermes/update-backups/20260804T090230Z-rk-v0191-d5f-precommit/d5f-precommit-files.tar.gz`, SHA-256 `77f1191d18a2c9e2916098c409a121ee5fefd6bec51d7654dee84be468ec0b51`; all nine product/test/ledger/evidence files restored byte-for-byte at that checkpoint. No live restore was performed.
- Boundary and next action: no production board, dispatcher, gateway, token, runtime, profile, registry, alias, skill, plugin, or cron was mutated. 주군의 explicit commit direction authorizes and accepts this self-recording D5-f commit, which closes D5-a through D5-f. Push remains unauthorized; await separate D6 re-audit direction, and do not start D7 or any R gate.

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

Current v0.19.1 IDs identify execution order and may differ from identically numbered v0.18.2 history. Historical and current numbering must never be conflated.

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

- D1–D7 each have an explicit owner direction and current evidence.
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

Task 6 technical result:

- exact upstream inventory: 72→70 bundled, 102→111 official optional, and 88→95 plugin manifests with complete path and content hashes;
- current fleet: 49/49 exact 72-skill v0.18.2 roots, extras 0, archives 0, markers 0, managed 5+10 with 15/15 source-map/sidecar parity;
- fresh resolver: 49 distinct processes, default 87, other profiles 77, duplicate names 0, and all audited hashes unchanged;
- disposable official-sync canary: exact 72→70 re-seed and exact 72 rollback passed;
- tests: skill/provenance/curator/cron slice 187 passed; separate overlapping plugin slice 95 passed;
- plugin decision: retain ATN and Orca, retire Kkachi network and its three KAN skills during post-live R2, and do not auto-enable new upstream plugins;
- corrected R2 protection: `curator.prune_builtins: false`, zero `.curator_suppressed`, secret-excluded typed KAN backup, exact installed-plugin hashes, and first-profile stop/restore;
- independent review exposed a v0.19.1 fail-open `skills.write_approval` import boundary. It was registered as new current D2, owner-authorized for a minimum fail-closed fix, and remains a tag blocker until separate D2 acceptance.

D2 technical result:

- import-failure RED reproduced a real unauthorized create (`success: true`); evaluation-failure RED reproduced an escaped `RuntimeError`;
- GREEN: both paths now return a structured `success: false` error before mutation; focused result 2 passed;
- related manager/approval/provenance/usage/guard/curator/ghost/cron slice: 199 passed, 0 failed;
- broad `tests/tools/` failures were reproduced on detached pre-D2 head with no new D2 failure; `py_compile`, `ruff`, diff check, and static added-line scan pass;
- fresh resolver: 49 processes, counts 87/77, duplicates 0, and all profile config/skill/managed hashes unchanged;
- independent read-only review passed with no security concern, logic error, suggestion, or scope creep;
- evidence: `root-kernel/evidence/v0.19.1-D2-skill-write-approval.json`, SHA-256 `0d6b1de44322fc7f37e66149008c0d30bf6359767e2c029a98d7f92c6f6a29d6`;
- pre-change rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260803T004148-rk-v0191-d2-write-approval/`, archive SHA-256 `e82b6c8d46f8855dc6e2c97d5f731c946cdb25686eb22f505964172f6d58f852`; typed restore passed and restored source reproduced both RED tests.

D3 technical result:

- abandoned pre-reset D3 changes were backed up non-secret, removed completely, and the worktree was restored to clean `516f0b74d` before a new closed-scope plan was written;
- production scope is four central files only: credential-pool selection, main runtime singleton fail-close, two auxiliary Codex helpers, and the existing labelled auth write boundary;
- profile-local exact ID/label pinning, ID precedence, duplicate/missing/empty/dead/exhausted fail-close, explicit API-key preservation, and no-pin behavior are covered;
- labelled reauth updates one exact OAuth row by captured index; manual rows preserve the singleton, while canonical `device_code` rows synchronize it so the update survives the next `load_pool()`;
- D3 focused result: 19 passed; related four-module result: 299 passed with the unchanged timing-sensitive test deselected, and that test passed separately 1/1;
- `py_compile`, `ruff`, `git diff --check`, added-line secret scan, and live-state boundary checks pass;
- independent read-only review initially found three logic errors; all three reproduced RED, passed after correction, and the bounded verdict-only follow-up reports zero remaining findings;
- evidence: `root-kernel/evidence/v0.19.1-D3-codex-credential-pinning.json`, SHA-256 `f3413b141b12c42b4b94958e20fa2cb55d595e492ce26144fa562da530570e1e`;
- rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260803T013102Z-rk-v0191-d3-clean.tar.gz`, SHA-256 `2abe783db89ab7bf0a0c694a26e0d43a481147980e58fcfb1cfd8ea48d6deeaf`; disposable restore canary changed 19 GREEN to 16 RED plus 3 preservation passes.

D4 read-only re-audit result:

- exact upstream anchor: tag `v2026.7.30`, commit `cc4cab2f592e60a197e796506de9168f74baf3ea`; current branch has no D4-related source or test delta from that anchor;
- upstream overlap: persistent participation tracking, require/free-response/thread-require-mention gates, fail-closed auto-thread failure, reply/voice skip behavior, bot inline-mention gates, safe output mention defaults, and missed-message recovery admission;
- remaining core gap: persistent thread owner state is absent, so participation still grants mention-free live routing and the new recovered-message path repeats the same ownership substitution;
- remaining routing gap: Discord role mentions are not detected as explicit routing, so a role-addressed message can fall through to a free-response/default responder;
- remaining creation/config gap: free-response owned auto-thread, parent-owner fallback, YAML/config bridge, and ownership marking for auto-created, slash-created, and new forum text/media threads are absent;
- isolated upstream-related Discord suite: `65 passed, 3 warnings` with Discord routing environment variables explicitly unset;
- disposable D4 probe: `6 failed as expected`, reproducing role fail-close absence, live/recovery participation-as-ownership, missing free-response owned auto-thread, missing owner tracker, and missing role-mention detector;
- evidence: `root-kernel/evidence/v0.19.1-D4-discord-thread-ownership.json`, SHA-256 `a93a6e7c726fbb945726de186251cbb53fd9808ee925bc116500da354e2836f1`;
- owner selected option A: retain a minimal v0.19.1-aware owner and role fail-close extension across shared live/recovery admission and all relevant thread-creation siblings, without replaying obsolete v0.18.2 code wholesale;
- implementation RED: core `7 failed`; config/slash/forum sibling `4 failed`;
- implementation GREEN: focused `42 passed`; related Discord suite `112 passed, 3 warnings`; thread persistence sibling `3 passed`;
- broad gateway Discord glob: `233 passed, 3 failed`; detached clean base reproduced the exact same three `discord.File` import-order failures, so D4 adds no broad failure;
- `py_compile`, `ruff`, `git diff --check`, and added-line security scan pass;
- rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260803T033508Z-rk-v0191-d4-pre-implementation/d4-targets.tar.gz`, SHA-256 `0cdccc37fd3c06cfab0d2317c5f6a058fdfdbe61c980ab571e97bed8745ad51c`; restore produced byte-equivalent pre-D4 production and changed current tests to `13 failed, 1 passed`;
- independent review: passed; security concerns `0`, logic errors `0`;
- evidence: `root-kernel/evidence/v0.19.1-D4-discord-thread-ownership.json`, SHA-256 `a93a6e7c726fbb945726de186251cbb53fd9808ee925bc116500da354e2836f1`.

D5 read-only re-audit result:

- exact upstream anchor: tag `v2026.7.30`, commit `cc4cab2f592e60a197e796506de9168f74baf3ea`; candidate D5 source and tests are byte-identical to that anchor;
- historical lineage: `D2-a` was audit-only; the v0.18.2 minimal implementation bundled legacy `D2-b` through `D2-e` into commit `4f7e449fb [D2-b] restore Kanban same-card review loop`, followed by legacy `D2-f`, `D2-g`, `D2-h`, and `D2-i` commits;
- current subitems for this carry: `D5-a` analysis; `D5-b` core same-card loop; `D5-c` review watcher; `D5-d` result acceptance; `D5-e` mutex; `D5-f` workflow banner;
- renumbering: legacy b-e → canonical b, legacy f → c, legacy g → d, legacy h → e, legacy i → f; no requirement is retired;
- preserve upstream: native review claim/dispatch, generic workflow metadata, goal judge, repair/corruption recovery/WAL checkpoint, per-task model/provider override, delegated-child mutation denial, child/project worktree isolation, and profile-aware cursor-safe notifier routing;
- remaining gaps: cooperative same-card handoff; submit-review/request-changes/creator final gate; creator result acceptance; review-specific watcher outcomes; `mutex_key`; closed `workflow_type` banners; immediate worker tool disclosure;
- semantic confirmation: a native reviewer claims `review -> running` and `kanban_complete` closes directly to `done`; current worker guidance still uses `review-required` block as a workaround;
- disposable D5 gap probe: `7 failed, 1 passed`, where the pass confirms native review and generic workflow metadata remain;
- native related suite: `89 passed, 1 skipped`;
- repair/WAL/model/child/worktree preservation suite: `23 passed`;
- independent review: passed; security concerns `0`, logic errors `0`;
- KSCQ retrieval: no related indexed learning note; no raw-packet expansion;
- evidence: `root-kernel/evidence/v0.19.1-D5-kanban-same-card-review.json`, SHA-256 `f7d341a6ba42306bfb51fa180b26dbbe4be0eda12ac2bb31ddbf5e93a51d97da`;
- scenario A, recommended: retain current D5-b through D5-f at current chokepoints; current b is the bundled core same-card loop, while current c/d/e/f are watcher/result/mutex/banner; preserve every verified new upstream behavior.

D1–D5 are owner-accepted. D5-a through D5-f are implemented, verified, and committed, with D5-f product, tests, and ledgers recorded by this self-recording commit. D6–D7, fleet re-seed, live mutation, tag, push, and remote-ref movement remain unauthorized pending separate direction.
