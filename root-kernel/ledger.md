# Root Kernel Hermes Agent v0.19.1 Release Ledger

This file is the human-readable, version-scoped release and operations ledger.

Current user-visible behavior and configuration belong in
`root-kernel/feature.md`. Structured carry state, lineage, evidence, and
retirement rules belong in `root-kernel/carry.yaml`.

## Release state

- Status: `v0.19.1-released`; tag `rk/tag/v0.19.1` on the release commit; `rk/live` moved to v0.19.1
- Candidate branch: `rk/v0.19.1`
- Candidate worktree: `/Users/draccoon/Workspace/Hermes/17th-hermes-agent-worktree`
- Tag blocker: `false`
- Live activation: v0.19.1 active at `413ee1d4bf9f83e636b937dac76a41368fe343c3`; technical pass and owner acceptance complete
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
- D6 commit and owner acceptance were both explicitly conveyed by 주군의 commit direction at `2026-08-04T20:52:21+09:00`; this is the self-recording `[D6]` commit
- D7 owner acceptance was recorded at `2026-08-05T01:20:28+09:00`; commit direction followed at `2026-08-05T01:38:42+09:00` and execution consent was reconfirmed at `2026-08-05T02:05:57+09:00`; this is the self-recording `[D7]` commit
- Task 13 integrated candidate smoke was authorized at `2026-08-05T02:19:30+09:00`; initial review blocked incomplete evidence, all corrections completed, and final independent technical verification passed at `2026-08-05T03:05:12+09:00`; 주군 accepted Task 13 at `2026-08-05T10:57:58+09:00`
- Task 14 activation backup and rollback rehearsal passed technically at `2026-08-05T12:03:10+09:00`; 주군 accepted Task 14 and authorized its two-ledger commit at `2026-08-05T12:26:25+09:00`
- Task 15 production activation passed technically at `2026-08-05T16:16:57+09:00`; 주군 accepted Task 15 and authorized its two-ledger commit at `2026-08-05T16:28:42+09:00`. Task 16, tag, push, and remote-ref movement remain separately pending
- Task 16 R1 read-only verification found canonical identity/model drift; 주군 then authorized the minimum repair. Repair and full verification passed at `2026-08-05T21:31:06+09:00`, and 주군 explicitly accepted R1 at `2026-08-05T21:57:25+09:00`
- Task 16 R2 was authorized at `2026-08-05T22:26:29+09:00`. The 49-profile target passed; the separately approved controlled root gateway refresh changed PID `9980`→`30334`, cleared KAN from the resumed session catalog, and preserved ATN. 주군 explicitly accepted R2 at `2026-08-06T00:01:21+09:00`
- Task 16 R3 was authorized after R2 acceptance. Initial verification found stale Dashboard frontend parity. 주군 then directed that Dashboard will not be used and authorized removal of its active build and runtime disablement. The service, automatic-start definitions, inactive Tailscale proxy definition, and active `web_dist` were removed with verified rollback; 주군 explicitly accepted R3 at `2026-08-06T01:29:31+09:00`
- Task 16 R4 was authorized after R3 acceptance. All 49 cron scopes contain zero jobs and current custom launchd/source parity passes. 주군 approved retaining broad `git add .` backup behavior while excluding secret data, then authorized the bounded security apply. Google Workspace retirement, credential removal, exact 63-commit history rewrite, remote/original-clone verification, and launchd resume passed technically. 주군 explicitly accepted R4 at `2026-08-06T16:07:23+09:00`
- Release-candidate commit, tag, push, and remote-ref movement: completed at
  `2026-08-07`; earlier task entries below preserve their historical gates
- Scaffolded at: `2026-08-02T17:24:26+09:00`

This document and `root-kernel/carry.yaml` must be updated together after every
approved D-item direction or verified result. Update
`root-kernel/feature.md` whenever an active user-visible behavior, default,
setting, command, or recommended recipe changes.

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

- `root-kernel/ledger.md`
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
- R2 reseeded all 49 homes to the exact live v0.19.1 set of 70 bundled skills. Package-content parity is 49/49 after excluding only runtime metadata; archives, no-bundled markers, and curator suppression files are zero.
- The applied allowlist is 70 exact bundled per profile, managed fleet 5, default-only admin 10, optional 0, local custom 0, plus the two explicitly retained default Orca skill symlinks. The 13 ATN and one Orca plugin entries remain byte-exact to their accepted manifests; Kkachi/KAN is absent from config and disk.
- Curator protection is `curator.prune_builtins: false` on 49/49. D2 remains the fail-closed write-approval carry; R2 added no candidate code.

## v0.19.1 active D items

Inherited carry lineages remain `pending-re-audit` until their own gate starts. D1–D7 and Tasks 13–15 are owner-accepted and committed. A familiar v0.18.2 patch is not authority to replay it.

| Current ID | Work item | Previous release | Current status | Next action |
|---|---|---|---|---|
| D1 | CJK-aware offline session recovery | New v0.19.1 defect discovered in Task 5 | `implemented-verified-task5-accepted` | Keep active until an exact upstream replacement satisfies the recorded retirement rule. |
| D2 | Fail-closed skill write approval import boundary | New v0.19.1 defect discovered in Task 6 | `implemented-verified-owner-accepted` | Keep active until an exact upstream fail-closed replacement is behaviorally verified. |
| D3 | OpenAI Codex credential pinning and labelled reauth | `v0.18.2/D8` | `implemented-verified-owner-accepted` | Keep active until an exact upstream replacement satisfies the retirement rule. |
| D4 | Discord thread ownership and role-mention fail-close | `v0.18.2/D4` | `implemented-verified-owner-accepted` | Closed; preserve until an exact upstream replacement is verified. |
| D5 | Kanban same-card review and workflow seams | `v0.18.2/D2` | `implemented-verified-self-recording-commit-owner-accepted` | Closed; preserved in Task 13 passing candidate. |
| D6 | CLI return-code passthrough | `v0.18.2/D6` | `implemented-verified-self-recording-commit-owner-accepted` | Closed; preserved in Task 13 passing candidate. |
| D7 | Doctor optional tool warning filter | `v0.18.2/D7` | `implementation-complete-verified-self-recording-commit-owner-accepted` | Closed; preserved in Task 13 passing candidate. |

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
- Boundary and next action: no production board, dispatcher, gateway, token, runtime, profile, registry, alias, skill, plugin, or cron was mutated. 주군의 explicit commit direction authorizes and accepts this self-recording D5-f commit, which closes D5-a through D5-f. Push remains unauthorized; the later separately authorized D6 re-audit is recorded below, and D7 plus all R gates remain blocked.

### D6 read-only re-audit result

- Owner boundary: D6 read-only re-audit ran from `2026-08-04T18:20:56+09:00` to `2026-08-04T19:03:44+09:00`. Product implementation, permanent implementation tests, commit, push, D7, and all R gates remain unauthorized.
- Historical authority: final `v0.18.2/D6` commit `aad49e9fccb0bb7160778460d1473808b5c0d9c0` changed the top-level argparse process boundary from ignoring handler return values to exact-int propagation while deliberately ignoring `bool`. Its parent with final tests reproduced `3 failed, 1 passed`; the final commit passed `4`, and the historical broad three-file gate passed `312`.
- Upstream overlap: v0.19.1 commit `397e9fc1e46e594d9d021a9061095e1b109faabb` added nonzero int propagation for egress. Candidate `hermes_cli/main.py` is byte-identical to upstream tag commit `cc4cab2f592e60a197e796506de9168f74baf3ea`, SHA-256 `13a826f08c3eb64c16b06d99e0b71274152c987bf87c26d948ec6ff09556ac63`.
- Remaining gap: the native predicate is `isinstance(rc, int) and rc != 0`. Actual-`main()` subprocess injection produced `None=0`, `False=0`, `True=1`, `0=0`, `2=2`, `-1=255`, and string `"2"=0`; the expected-contract probe was `1 failed, 9 passed`, with `True` the only failure. Native v0.19.1 is therefore partial, not a replacement for the bool-safe exact-int contract.
- Real CLI smoke: missing Kanban task returned `1`, invalid board slug returned `2`, and top-level help returned `0`. Native egress and Kanban adjacent suites passed `20`.
- Docker diagnostic: a wider three-file run passed `23` and failed one pre-built s6 harness check because the image returned `137` instead of inner `42` with shutdownd permission errors. The test is byte-identical to upstream and exercises container supervision, not Python argparse; both independent review and source tracing classify it as a separate non-D6 regression, not a D6 blocker.
- Options: retiring D6 is rejected because the bool gap remains. Verbatim historical replay is rejected because it would not minimally extend the newer upstream nonzero shape. An inline `type(rc) is int` change is valid but less explicit and less directly testable. Recommended: `retain-minimal-v0.19.1-aware-exact-int-helper`.
- Proposed implementation: add one small internal helper in `hermes_cli/main.py` that exits only for nonzero values whose exact type is `int`, replace the inline `isinstance` branch with the helper, and add `tests/hermes_cli/test_main_return_codes.py`. No parser, egress, plugin registry, command handler, update, gateway, profile, or runtime contract should otherwise change.
- Required TDD contracts: permanent actual-`main()` subprocess checks for `None/False/True/0/string -> 0`, `2 -> 2`, and POSIX `-1 -> 255`; disposable-HERMES_HOME egress failure `1`; Kanban missing task `1`; invalid board or argparse misuse `2`; help `0`. Tests must assert behavior relationships, not source snapshots.
- Disposable design spike: the proposed helper passed all `10` expected-contract checks, `20` native egress/Kanban checks, Ruff, and `py_compile`; no product or permanent test file was changed.
- Independent review: architecture session `019fcc32-378b-7393-8117-806028ab4972` recommended narrow helper hardening with zero blockers. Security/test session `019fcc33-ace9-7401-a9bf-69b4aff0fb4f` found zero security blockers and required the permanent actual-main/real-CLI test matrix; that requirement is now part of the implementation proposal and must be completed before implementation can pass review.
- Evidence: `root-kernel/evidence/v0.19.1-D6-cli-return-code-reaudit.json`, SHA-256 `5a811b6c6bbb5de3f692493553685a0a6abd67508809e93bf45246ed7291361a` (local, Git-excluded).
- Rollback: non-secret pre-audit ledger archive `/Users/draccoon/Workspace/Hermes/update-backups/20260804T092056Z-rk-v0191-d6-audit/d6-ledgers-pre-audit.tar.gz`, SHA-256 `e0b6cf7944b207a9e71cf98b6731bacaf443d511ab156a3a3af5d43c4624e6b6`; both ledgers restored byte-for-byte.
- Implementation direction: 주군 explicitly authorized D6 implementation at `2026-08-04T19:16:59+09:00`. This authorizes strict TDD changes only in `hermes_cli/main.py`, `tests/hermes_cli/test_main_return_codes.py`, the two ledgers, and Git-excluded D6 implementation evidence; commit, push, D7, and live/profile/runtime mutation remain unauthorized.
- Implementation rollback: non-secret pre-implementation archive `/Users/draccoon/Workspace/Hermes/update-backups/20260804T101659Z-rk-v0191-d6-implementation/d6-pre-implementation.tar.gz`, SHA-256 `bd0baa55ee7624948bf93bc011cbc6a44357d6db1f825ac421b50bfce0e2703f`; product, ledgers, and audit evidence restored byte-for-byte, and the manifest records that the permanent test file did not exist beforehand.
- Implementation execution: strict TDD implementation and verification completed at `2026-08-04T19:33:45+09:00`; detailed results are recorded below.

### D6 implementation result

- Scope: added `_exit_if_nonzero_exact_int` in `hermes_cli/main.py`, replaced only the existing inline `isinstance` branch, and added `tests/hermes_cli/test_main_return_codes.py`. No parser, egress, Kanban, plugin registry, command handler, update, gateway, profile, or runtime implementation changed.
- Behavior: exact nonzero `int` values retain native `sys.exit` semantics. `True`, `False`, `None`, strings, and other non-exact-int returns remain process success. Handler-raised `SystemExit` remains untouched.
- TDD: before product change the permanent actual-`main()` suite produced `11 passed, 1 failed`; only `True` incorrectly returned `1`. After the minimal helper the same suite passed all `12`.
- Permanent subprocess contracts: actual `main()` injection covers `None/False/True/0/string -> 0`, `2 -> 2`, and POSIX `-1 -> 255`; disposable `HERMES_HOME` real CLI paths cover egress failure `1`, Kanban missing task `1`, invalid board `2`, argparse misuse `2`, and help `0`.
- Bounded verification: `239 passed` across `24` egress, Kanban, main-model, and update-adjacent files. Ruff check, test-file format, `py_compile`, `git diff --check`, and added-line security scan passed.
- Baseline diagnostics: `tests/hermes_cli/test_update_eol_churn.py` produced the same `5 failed, 4 passed` on clean HEAD and current. `ty` produced the same `32` errors on clean HEAD and current with zero D6 path mentions. Full `main.py` format remains baseline-red on both clean HEAD and current because upstream would be broadly reformatted. The audit's Docker s6 `137` versus `42` failure remains a separate upstream-identical container supervision regression.
- Independent review: architecture/security session `019fcc4f-76c6-7c93-a0e2-f9956e18fe8a` returned `PASS`, blocker `0`; test/regression session `019fcc52-14e3-7983-9365-fd4538d2a709` returned `PASS`, blocker `0`. Neither reviewer modified files.
- Product hashes: `hermes_cli/main.py` SHA-256 `6e7a8f0efb6d05ec642e01374814cb08b1119926d2abb87596201641ff4e4b54`; `tests/hermes_cli/test_main_return_codes.py` SHA-256 `271a700bea66e6cb516a7e3adc41573d9382e12473681de316d104b92b663026`.
- Evidence: `root-kernel/evidence/v0.19.1-D6-cli-return-code-implementation.json`, SHA-256 `11ce00b87a572afa874dad7224e9d8ae5b8eedca15c675418e1c89b7bdfe8694` (local, Git-excluded).
- Rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T101659Z-rk-v0191-d6-implementation/d6-pre-implementation.tar.gz`, SHA-256 `bd0baa55ee7624948bf93bc011cbc6a44357d6db1f825ac421b50bfce0e2703f`; restore byte parity passed and rollback removes the newly created test file. The reviewed precommit candidate archive is `/Users/draccoon/Workspace/Hermes/update-backups/20260804T115221Z-rk-v0191-d6-precommit/d6-precommit-files.tar.gz`, SHA-256 `8d6fe27e9afd79f48a36ebef720f317ca57ce526d469cade9afb8530ee65a688`; all five product/test/ledger/evidence files restored byte-for-byte at that checkpoint.
- Boundary and next action: product and permanent tests are limited to the two recorded D6 files. 주군의 explicit commit direction authorizes and accepts this self-recording D6 commit. No live/profile/runtime, gateway, token, skill, plugin, cron, D7, R gate, tag, or push mutation occurred. After commit creation, await explicit D7 re-audit direction.

### D7 read-only re-audit start

- Authorization: 주군 authorized D7 investigation, analysis, and solution proposal at `2026-08-04T21:54:30+09:00`.
- Active scope: reconstruct final `v0.18.2/D7`, trace current v0.19.1 doctor diagnostic ownership, run disposable minimal/default-off/disabled/enabled probes, compare preserved versus missing behavior, and propose one v0.19.1-aware solution.
- Excluded: no product or permanent test implementation, commit, push, Task 13 integrated smoke, live/profile/config/gateway/token/skill/plugin/cron mutation, tag, remote-ref movement, or R gate.
- Rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T125430Z-rk-v0191-d7-investigation/d7-ledgers-pre-investigation.tar.gz`, SHA-256 `08bd50dc4873c2db0d4cbdbe689399269e522e03810d17edab6b2db22078801a`; both ledgers restored byte-for-byte and no secrets are included.
- Next action: investigation is complete; option C is proposed below. Implementation requires a separate direction.

### D7 read-only re-audit result

- Exact candidate anchor: `rk/v0.19.1` HEAD `11847601d5da3efe68e768e633e768482175c99a`, exact upstream `cc4cab2f592e60a197e796506de9168f74baf3ea`; `hermes_cli/doctor.py` and the three Task 12 target test files are byte-identical to upstream.
- Historical lineage: final v0.18.2 D7 commit `5582e0db6512f67214a1b37d66a76e4df09bfe27` filtered both available and unavailable rows by exact enabled-toolset names. Re-execution passed focused `4/4` and doctor/dedicated-provider `72/72`.
- Upstream overlap: commit `6b21a935af24b7b3c4ee2370598471aa8978a243` is **partial, not replacement**. It filters only the final missing-API-key setup summary to enabled CLI toolsets; `Tool Availability` warning rows remain global.
- Current actual behavior: five disposable profiles (`default`, `web_only`, `web_disabled`, explicit `x_search`, explicit Discord platform) all returned `0` and preserved config bytes, but default-off `discord`, `discord_admin`, `homeassistant`, `spotify`, `video`, `video_gen`, and `x_search` warnings remained visible; disabled `web` also remained visible.
- Throwaway RED loop: `3 failed, 2 passed`. The three failures reproduce default-off and explicit-disable leakage; the two passes preserve fail-open visibility and runtime-gated Kanban promotion. No product or permanent test file was changed.
- Option A, retire as upstream-native: rejected because the warning-row gap remains. Option B, replay the historical available-and-unavailable name filter: rejected because v0.19.1 aliases/subtoolsets such as `browser-cdp` can differ from configured composite names and healthy-row filtering is broader than the requirement. Option D, read raw YAML only: rejected because it bypasses canonical defaults, restrictions, plugins/MCP, recent toolsets, and `agent.disabled_toolsets`.
- **Recommended option C:** after existing Kanban/Honcho overrides, resolve CLI plus explicitly configured platform scopes through `_get_platform_tools`, expand them through `resolve_toolset`, and filter only unavailable warning rows proven outside scope. Keep rows by enabled toolset name or effective tool-name intersection. Leave available rows and the native final CLI-only summary unchanged. Fail open globally on scope exceptions and per row for malformed, empty, or unmapped metadata.
- Stronger v0.19.1 diagnostics preserved: SQLite/source-ID/WAL/state/FTS repair, SSL/certifi, agent-browser/Chromium/CDP, config/deprecation, dedicated-provider/connectivity, and every section outside `Tool Availability` remain untouched.
- Disposable design spike only: new contracts `7 passed`; current doctor/dedicated-provider/SQLite target `55 passed`; Ruff and `py_compile` passed; all five real profiles returned `0` with byte-unchanged configs and expected warning filtering. With the same venv, current versus spike output outside `Tool Availability` was byte-identical in all five cases.
- Two independent read-only Codex reviews: architecture/security `PASS`, diagnostics/regression `PASS`, total blockers `0`. Permanent implementation must add real-resolver RED coverage for default, disabled, explicit tool/platform, `agent.disabled_toolsets`, `browser-cdp`, Kanban/Honcho, available-list preservation, unknown metadata, and fail-open behavior before product code.
- KSCQ query `Hermes doctor optional tool warnings default-off config scope`: no indexed learning note; no raw packet expansion and no change to the source/test/probe conclusion.
- Investigation-close evidence snapshot: `root-kernel/evidence/v0.19.1-D7-doctor-warning-filter-reaudit.json` had SHA-256 `4ce9e1f2acbd37895ba29a36f02c1d9737775786aa0b438227e0da1ae1af09f0`; the same local Git-excluded evidence file was later extended through implementation and owner acceptance, with its current hash recorded below.
- Boundary at investigation close: investigation and proposal were complete while product implementation, permanent RED/GREEN, commit, push, Task 13, live/profile/runtime mutation, tag, and remote-ref movement remained unauthorized pending separate direction.

### D7 option C implementation start

- Authorization: 주군 authorized option C implementation at `2026-08-04T22:37:12+09:00`.
- Scope: add permanent behavior contracts first, prove RED on the current candidate, implement only the warning-only semantic runtime-scope filter in `hermes_cli/doctor.py`, and run the full Task 12/static/real-profile/independent-review gate.
- Commit boundary: product and permanent test implementation are authorized; commit, push, Task 13, live/profile/runtime mutation, tag, and remote-ref movement remain unauthorized.
- Rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T133712Z-rk-v0191-d7-implementation/d7-pre-implementation.tar.gz`, SHA-256 `6aca8810e894d44cf7e488c7770dd53601c2ecd9f81b9bce484ffbb4ac0eacb2`; source, permanent test, both ledgers, and investigation evidence restored byte-for-byte in a disposable directory; no secrets are included.
- TDD order: permanent RED contracts precede any product code. GREEN may change only `hermes_cli/doctor.py`; current native summary and every non-Tool-Availability diagnostic remain fixed preservation boundaries.

### D7 option C implementation result

- Result: option C is implemented in `hermes_cli/doctor.py` with permanent behavior coverage in `tests/hermes_cli/test_doctor.py`; no other product or permanent test file changed.
- Behavior: existing Kanban/Honcho overrides run first; CLI plus explicitly list-shaped platform scopes resolve through canonical `_get_platform_tools`; `resolve_toolset` preserves aliases/subtoolsets by effective-tool overlap; only unavailable warning rows proven out of scope are hidden; available rows and the native CLI-only summary remain intact.
- Fail-open boundary: scope exceptions preserve all rows. Missing, empty, non-list, non-string, or blank `tools` metadata remains visible. Non-dict rows pass through overrides/filtering, render a fixed generic warning without raw-value disclosure, and are excluded safely from the API-key summary.
- TDD: five initial behavior contracts each reproduced RED before their minimum GREEN. The first independent implementation reviews then found one shared malformed-row blocker; permanent regressions reproduced it as two failed contracts plus one failed summary contract, and all three passed after remediation.
- Verification: final doctor file `53 passed`; full Task 12 target `66 passed, 0 failed`; Ruff, `py_compile`, `git diff --check`, and added-line security scan passed.
- Real smoke: all five disposable profiles returned `0`, preserved config bytes, hid default-off/disabled warnings, retained explicit `web`, `x_search`, Discord, `browser-cdp`, and runtime Kanban diagnostics, and matched implementation-before output byte-for-byte outside `Tool Availability` in `5/5` cases. Task 13 later preserved D7 in the passing integrated candidate.
- Independent review: initial specification and security reviews returned `REVISE` on the same malformed-row fail-open blocker. After RED-driven remediation, fresh final reviews returned `PASS` with blocker `0`, security concern `0`, logic error `0`, and suggestion `0`; no reviewer modified files.
- Evidence: `root-kernel/evidence/v0.19.1-D7-doctor-warning-filter-reaudit.json`, SHA-256 `0cc19782f6672b5b83776e302a23a778ef588159afe8fbf98c27240df3b53836` (local, Git-excluded).
- Rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T133712Z-rk-v0191-d7-implementation/d7-pre-implementation.tar.gz`, SHA-256 `6aca8810e894d44cf7e488c7770dd53601c2ecd9f81b9bce484ffbb4ac0eacb2`; disposable byte restore passed and no secrets are included.
- Boundary: D7 is technically complete, owner-accepted, committed, and preserved by Task 13. Push, Task 14, live/profile/runtime mutation, tag, and remote-ref movement remain unauthorized.

### D7 owner acceptance and commit direction

- Owner acceptance: 주군 explicitly approved D7 at `2026-08-05T01:20:28+09:00`.
- Commit direction: 주군 explicitly authorized the D7 commit at `2026-08-05T01:38:42+09:00`; execution consent was reconfirmed at `2026-08-05T02:05:57+09:00`. This authorizes one self-recording `[D7]` commit only.
- Acceptance rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T162028Z-rk-v0191-d7-owner-acceptance/d7-pre-owner-acceptance.tar.gz`, SHA-256 `b553146737994d12bb3b12489a566b99d9a39fc68dfa48a0c9d5f2f5e9deb29d`; both ledgers and Git-excluded evidence restored byte-for-byte, with no secrets included.
- Precommit rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260804T163842Z-rk-v0191-d7-precommit/d7-precommit-files.tar.gz`, SHA-256 `38417cd38cdf84789e2b5aea9650bb3ccb5dd512a99a4537dfd6d4860fd1ccce`; product, permanent test, both ledgers, and Git-excluded evidence restored byte-for-byte, with no secrets included.
- Next gate: Task 13 was subsequently owner-accepted and committed; Task 14 is now owner-accepted and its two-ledger commit is authorized. Task 15, push, live/profile/runtime mutation, tag, and remote-ref movement remain unauthorized.

### Task 13 integrated candidate smoke

- Authorization and boundary: 주군 authorized Task 13 at `2026-08-05T02:19:30+09:00`. Only candidate smoke was authorized; Task 14, `rk/live`, profiles, live runtime, gateways, refs, tags, push, and remote-ref movement remained outside scope.
- Technical verdict: `accepted-ledger-commit-created`; corrected verification and independent re-audit completed at `2026-08-05T03:05:12+09:00`, 주군 accepted Task 13 at `2026-08-05T10:57:58+09:00`, and authorized the two-ledger commit at `2026-08-05T11:12:30+09:00`. Final commit identity is the Git HEAD after the ledger-only closeout amend.
- Exact candidate: `rk/v0.19.1` at `4ca7afa4f7d2afddea0e765b47e645e0765dc012`, 16 carry commits above local and upstream annotated tag `v2026.7.30`, object `d25e2dbdbc40b49808c0a0e9cfed21cc90cffab3`, which peels exactly to release commit `cc4cab2f592e60a197e796506de9168f74baf3ea`. The SSH signature verified with ED25519 fingerprint `SHA256:x9xNOpeJhoEAY2gWhmWHZROC3QF3VjOEbmNo9vQ8y2A`.
- Carry origins: D1 is a current-release Task 5 discovery; D2 is a current-release Task 6 discovery; D3 through D7 retain lineages `v0.18.2/D8`, `v0.18.2/D4`, `v0.18.2/D2`, `v0.18.2/D6`, and `v0.18.2/D7` respectively.
- Disposable CLI: core imports, `--version`, `--help`, `config check`, and `doctor` all returned `0` under clean no-credential `HERMES_HOME`; the disposable home was removed.
- Python verification: a single canonical run over 54 de-duplicated test files passed `1,339`, failed `0`. The 13 carry/surface group runs passed `1,428` executions with `0` failures; that second number intentionally includes repeated files and is not a unique-test count.
- Dashboard: R3 remains in the activation roster, so the conditional source/build smoke ran. Source tests passed `12/12`; the final auditable exact-lock tmpfs build produced 51 files with SHA-256 `15e8ff94af4dbec3e10f7d85333db569735622916d3fbdafd0b79e99aaba5e5c`.
- Docker and dashboard isolation: exact executable scripts and full host commands are preserved. Each final run used one candidate-only read-only bind mount, read-only container root, nonroot user, tmpfs, `--network none`, no host credential/database mount, and explicit inner-command exit codes. Docker imported `/candidate/hermes_cli/main.py`, returned `0` for imports/version/config/doctor/SQLite FTS, and linked SQLite `3.53.4`.
- Nonblocking warnings: the host shared candidate venv links SQLite `3.50.4` and uses verified DELETE-mode fallback; activation rebuild must re-verify fixed SQLite. The source banner local-main annotation is not release-base evidence. Blank-home missing config/auth/launcher, partial sessions schema, Skills Hub, and optional-tool warnings are expected and isolated. One auxiliary timeout first attempt exceeded its threshold by 3.8 ms and passed retry; exact tag and candidate each passed `3/3` clean-env comparisons, and candidate passed `5/5` normal-env repeats.
- Scope boundary: Task 14's typed runtime/launcher/gateway rollback rehearsal was not part of Task 13. It subsequently passed and is now owner-accepted with its two-ledger commit authorized.
- Independent review: the first review returned `BLOCKED` and found the tag-ref, lineage, command-auditability, warning-classification, and duplicate-count defects. After correction, a fresh read-only Codex audit returned `VERDICT: PASS`, `TASK13_BLOCKERS: NONE`, and `FILES_MODIFIED: NONE`.
- Evidence: `root-kernel/evidence/v0.19.1-task13-integrated-candidate-smoke.json`, SHA-256 `7578a4f5a0a9f2759f8f296cdd1edf4f39a699e17b24916259f4f7fc26cc8de5` (local, Git-excluded). Logs and executable evidence scripts are under `/Users/draccoon/Workspace/Hermes/update-backups/20260804T172349Z-rk-v0191-task13/`.
- Rollback: the Task 13 start-ledger archive SHA-256 is `9bd94bdb39f5f15149f3072f9231b183450806f9368c3d36de11fe80387e8e44`. The pre-review-correction archive SHA-256 is `f183c6f6eb5f07366e0ccf46a10190cf6db5a94a4ad0f87aa20101e8e337ae90`. The pre-owner-acceptance archive SHA-256 is `c3f0992f4d1dc201b9ae8bb6ec977d674a3fc9d5d61e9546a0b7612f9f49b132`. The precommit archive is `/Users/draccoon/Workspace/Hermes/update-backups/20260805T021230Z-rk-v0191-task13-precommit/task13-precommit-files.tar.gz`, SHA-256 `fd1bfb741a8cb6b60827affe2ea218ab2ad4547a642bac9af4f19b07021f8a1d`; byte restore passed and no secrets are included.
- Historical next gate at Task 13 closeout: the authorized two-ledger `[INT]` self-recording commit was created, Task 14 awaited acceptance, and Task 15 was unauthorized. Tasks 14–15 have since been owner-accepted.

### Task 14 activation backup and rollback rehearsal

- Purpose: make v0.19.1 activation reversible before any live change.
- Technical verdict: `accepted-ledger-commit-created`; technical verification passed at `2026-08-05T12:03:10+09:00`, and 주군 accepted Task 14 and authorized its two-ledger commit at `2026-08-05T12:26:25+09:00`. Final commit identity is the Git HEAD after the ledger-only closeout amend.
- Package: `/Users/draccoon/Workspace/Hermes/update-backups/20260805T025041Z-rk-v0191-activation/activation-rollback-package.tar.gz`, SHA-256 `b5f76771b6165282aaf4a51f7e47f0eb732d0d5ba70791bb49f85ba85f53d5cb`, mode `0600`. It records both repositories' local and remote-tracking heads, live checkout/venv/launcher paths, 49 typed config targets, 12 gateways plus dashboard, 17 launchd definitions, 13 activation definitions, and skill/cron/script manifests.
- Exclusions: no `.env`, `auth.json`, token, key, credential pool, complete profile config, venv contents, secret-bearing log, or production state DB byte is archived. Structured secret and archive restore byte/mode checks passed.
- Rehearsal: restored 27 package files; live v0.18.2 import, version, config check, and session-state commands returned `0`; disposable state schema 19 passed integrity; 13 definitions reconstructed without launch; live PIDs and both Git heads were unchanged.
- Sensitive state boundary: metadata for 12 production DBs was recorded without reading or copying bytes. Restricted backup remains separately approval-gated before Task 15.
- Activation boundary: preserve the current v0.18.2 venv before rebuilding; normalize and roll back the PATH launcher; control the current root gateway only from an external shell; do not reuse or fall back to another profile's credentials.
- Review: deterministic closeout audit passed every Task 14 requirement. Optional Codex and Claude independent CLI reviews were unavailable due authentication and produced no verdict; the plan does not require an independent LLM review.
- Evidence: `root-kernel/evidence/v0.19.1-task14-activation-rollback.json`, SHA-256 `d501562673429a104b246bce7c9dddf0d946e1a2bc4b6b4f9ea19bf32bf4e048` (local, Git-excluded).
- Acceptance commit rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260805T032625Z-rk-v0191-task14-acceptance-precommit/task14-acceptance-precommit.tar.gz`, SHA-256 `e17056feaac1dda5ebb1825159e4f9485cf82eb4ca73d73883569f416529b2b0`; restore parity passed and no secrets are included.
- Historical next gate at Task 14 closeout: the authorized two-ledger `[INT]` commit was created and Task 15 remained separately gated. Task 15 has since activated v0.19.1 and been owner-accepted; tag, push, and remote refs remain unauthorized.

### Task 15 production activation

- Technical verdict: `accepted-ledger-commit-created`; v0.19.1 is active on local `rk/live` at candidate head `413ee1d4bf9f83e636b937dac76a41368fe343c3`. 주군 accepted Task 15 and authorized its two-ledger commit at `2026-08-05T16:28:42+09:00`. No push, tag, or remote-ref movement occurred.
- First attempt: the system-Python SQLite 3.51.0 read-only integrity check failed before the first DB copy. Automatic rollback restored v0.18.2, all 13 approved processes, schema 19, and a clean live worktree. The corrected controller retained read-only source access and switched only to the prepared managed SQLite 3.53.1 runtime.
- Restricted backup and migration: 12/12 schema-19 DB backups passed integrity, count parity, FTS readability, directory mode `0700`, and file mode `0600`; all 12 live DBs then migrated to schema 23. Default counts are 1,071 sessions and 84,410 messages/FTS rows; the other 11 DBs were empty before and remain empty after migration.
- Runtime: Python 3.11.15, SQLite 3.53.1, Hermes v0.19.1, 13 fresh approved PIDs, 12 gateway profiles, dashboard health pass, 12/12 cron-status commands pass, and PATH launcher target `/Users/draccoon/.hermes/hermes-agent/venv/bin/python`.
- Activation smoke: 49/49 profile config checks passed with zero writes; Discord and Telegram visible smoke passed; no credential fallback or reuse was detected.
- Post-live rollback-trigger regression: D1, D4, D5, D6, D7, and CJK FTS focused scope passed 397/397 across 14 files under disposable test isolation.
- Rollback authority: `rk/rollback/pre-v0.19.1-20260805T130458`, preserved `venv.rollback-v0.18.2`, and the restricted 12-DB snapshot remain available. The automatic rollback path was exercised successfully by the first attempt.
- Evidence: `root-kernel/evidence/v0.19.1-task15-production-activation.json`, SHA-256 `8780c14b6db179171dbd5fc4afb709cec7f29bf89144a05d4639e6a6ff8dc74d` (local, Git-excluded). Controller receipt SHA-256 `6712e97619c248b63c4f6f431b7791f899c8a774d379f4946ed11d24db5c83f3`; restricted backup receipt SHA-256 `718f461cba8ffa8259a8ce98b8fd77be53abf81710148a944b2c9d9a1ebed2e8`.
- One-shot cleanup: the completed activation LaunchAgent is unloaded and removed from `~/Library/LaunchAgents`; its mode-0600 plist is archived in the Task 15 controller package, preventing stale login-time reruns.
- Closeout rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260805T071516Z-rk-v0191-task15-closeout/task15-closeout-preledger.tar.gz`, SHA-256 `c09356d15281b1cd8c2a60e514a20605b4988f6093cede6354ab47c90a037eec`; no secrets included.
- Acceptance precommit rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260805T072842Z-rk-v0191-task15-acceptance-precommit/task15-acceptance-precommit.tar.gz`, SHA-256 `8fbafcfc585260b3afab6d24b0031a4f073db4bcad8ca745e5a896dee871d56c`; three-file byte restore parity passed and no secrets are included.
- Next gate: Task 15 is owner-accepted and its two-ledger commit is created. Await a separate Task 16 R1 start direction; do not push, tag, or move remote refs.

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

R gates are not candidate-construction tasks. `rk/live` activation and Task 15 owner acceptance are complete. R1–R5 are owner-accepted. The tag blocker is cleared.

| Gate | Scope | Status | Acceptance |
|---|---|---|---|
| R1 | Config/profile activation policy | `owner-accepted` | Accepted by owner at `2026-08-05T21:57:25+09:00` |
| R2 | Skill provenance, overrides, and compatibility | `owner-accepted` | Accepted by owner at `2026-08-06T00:01:21+09:00` |
| R3 | Dashboard and Desktop | `owner-accepted` | Dashboard intentionally disabled; accepted by owner at `2026-08-06T01:29:31+09:00` |
| R4 | Cron, local scripts, watchers, and automation | `owner-accepted` | Security apply passed; accepted by owner at `2026-08-06T16:07:23+09:00` |
| R5 | Profile-owned local asset optimization | `owner-accepted` | Asset optimization passed; accepted by owner at `2026-08-06T17:30:00+09:00` |

Only one R gate may be active at a time. Technical success is not acceptance.

### Task 16 R1 config/profile activation policy

- Technical verdict: `pass`; owner acceptance: `accepted` at `2026-08-05T21:57:25+09:00`. The initial findings were pre-existing source-of-truth drift, not a v0.19.1 runtime regression.
- Owner-authorized identity repair: the canonical default member, alias, and executable now resolve as `Munang` / `munang` / `문앙`; `/Users/draccoon/.local/bin/munang` launches the default config, and the legacy `heuktaeja` executable and active source-of-truth terms are absent.
- Owner-authorized model repair: 25 inactive profile configs moved from `openai-codex/gpt-5.5` to `openai-codex/gpt-5.6-sol`. Non-target semantics and file modes are unchanged. Fleet distribution is now 46 `gpt-5.6-sol` and 3 intentionally retained `glm-5.2`, with zero registry model/provider mismatch.
- Canary: the public config CLI applied the target but rewrote YAML formatting. The already-approved Task 4 canonical serializer restored exact formatting; exact target-only forward, exact rollback, and `config check` passed before fleet use.
- Final verification: 49/49 `config check`, 0 verification writes, 49/49 approved typed policy, zero canonical identity/model/provider mismatch, 12 unchanged gateway PIDs with no restart, 12 schema-23 state databases, and clean live `413ee1d4`.
- Nonblocking inherited observation: `ijeok` and `yuyeop` have no Korean alias entry and duplicate their English name in `SOUL.md`; canonical registry identity is exact and R1 did not alter them.
- Evidence: `root-kernel/evidence/v0.19.1-task16-r1-config-profile-policy.json`, SHA-256 `18e6d621a7c9a0e4a1408d068d049512b87a12a2688d70cfe2cf7903ec2627cf` (local, Git-excluded).
- Repair rollback: `/Users/draccoon/Workspace/Hermes/update-backups/20260805T211508+0900-rk-v0191-task16-r1-repair/`; typed rollback dry-run and archive extraction canary passed, no secret files are included.
- At R1 closeout, no gateway restart, state database write, token/auth write, commit, tag, push, or remote ref movement had occurred, and R2 still required separate direction. That R2 direction was subsequently granted.

### Task 16 R2 skill provenance, overrides, and compatibility

- Technical verdict: `pass`; owner acceptance: `accepted` at `2026-08-06T00:01:21+09:00`. The controlled external refresh changed root gateway PID `9980`→`30334` on the live v0.19.1 venv; the resumed session catalog now contains zero KAN tools.
- Applied target: 49/49 profiles contain the exact 70 v0.19.1 bundled packages, `curator.prune_builtins: false`, zero no-bundled/suppression/archive state, managed governance 15 skills across 49 profiles with zero violations, and 49/49 passing `config check` and fresh resolver checks.
- Plugin result: 13 ATN plus one Orca entry remain byte-exact; `orca-cli` and `orchestration` remain as the explicitly retained default Orca skill symlinks. Kkachi/KAN is absent from default config, disk, fresh skill disclosure, and fresh tool disclosure.
- Canary and rollback: inactive `biui` passed exact 72→70 forward, config check, exact config rollback, and exact skill-tree rollback. The secret-excluded rollback package is `/Users/draccoon/Workspace/Hermes/update-backups/20260805T223716+0900-rk-v0191-task16-r2/`.
- Verification: skill/curator/cron suite `189 passed`; plugin discovery and compatibility suite `137 passed`; 12 gateways are running, and root uses the live v0.19.1 venv. Telegram and Discord reconnected as expected, with Discord identity `문앙#5587`.
- Resolved finding `R2-RUNTIME-KAN-001`: KAN is absent from disk, config, fresh disclosure, and the resumed session catalog; ATN remains in 13 profile plugin entries and all four required skill disclosures. The controller's initial `failed` receipt was a false negative from comparing Discord's correct 74 autocomplete registrations with the resolver's 76 enabled skills; independent post-refresh verification passed, and the corrected controller is preserved in the rollback package.
- Evidence: `root-kernel/evidence/v0.19.1-task16-r2-skill-provenance.json`, SHA-256 `da8f53037b650d37173f413bed57481c1e9ed954bc706a810dfc43686ef73988` (local, Git-excluded).
- No state database, credential, token, auth file, candidate code, commit, tag, push, or remote ref was changed.

### Task 16 R3 Dashboard and Desktop

- Technical verdict: `passed`; owner acceptance: `accepted` at `2026-08-06T01:29:31+09:00`. 주군 superseded the unused-frontend repair with an explicit Dashboard retirement policy and accepted the resulting state.
- Applied scope: unloaded `ai.hermes.dashboard` PID `9887`; removed canonical and installed Dashboard launchd definitions; removed the inactive canonical `ai.hermes.dashboard.tailscale-proxy` definition; removed live `hermes_cli/web_dist` 30-file build. Hermes source and the `dashboard` CLI command remain installed but no service, automatic-start definition, listener, process, or active frontend build remains.
- Verification: Dashboard labels are unloaded, port `9119` is closed, health returns connection refusal, active and candidate `web_dist` are absent, and config check passes. Root gateway PID `30334` remained running with Discord and Telegram connected; Desktop remains intentionally inactive.
- Resolved finding `R3-DASHBOARD-001`: stale frontend parity is no longer applicable because the owner-directed supported state is Dashboard disabled, not Dashboard refreshed. `R3-DASHBOARD-002` is superseded by the same retirement while the root gateway remains independently healthy.
- Rollback: exact definitions, prior 30-file frontend build, and pre-change R3 ledgers are preserved without secrets under `/Users/draccoon/Workspace/Hermes/update-backups/20260806T011838+0900-rk-v0191-task16-r3-dashboard-disable/`; extraction canary, script syntax, and all package checksums pass.
- Evidence: `root-kernel/evidence/v0.19.1-task16-r3-dashboard-desktop.json`, SHA-256 `849ac9570bc93f5ff7880232231b9a9393ed421ca17487b07c799cbadf50c054` (local, Git-excluded).
- Next action: R3 is owner-accepted; R4 is now also owner-accepted. R5 remains pending.

### Task 16 R4 Cron, local scripts, watchers, and automation

- Technical verdict: `passed`; owner acceptance: `accepted` at `2026-08-06T16:07:23+09:00`.
- Cron and scheduler inventory: all 49 profile scopes were parsed; 14 store files exist, every scope has zero jobs, parse errors are zero, and no dormant enabled job exists. Twelve gateway schedulers are running, but there is no cron work to schedule.
- Script governance: current audit exits `0` with zero reported governance violations; 18 runtime files and one reachable transitive dependency were checked. Python and shell syntax checks pass. Focused candidate and expanded external automation-contract suites pass `89`, fail `0`.
- Custom launchd: four automation labels retain exact canonical/install byte parity and existing targets. The Workspace backup label resumed enabled and loaded with `RunAtLoad=false`; one bounded launchd run completed with exit `0`.
- Resolved finding `R4-AUTOMATION-001`: broad `git add .` behavior is retained for non-secret data. The Workspace repository has 28 synchronized secret-only patterns and the backup fails closed if any matching path is tracked or if its pattern file is absent.
- Resolved finding `R4-REMOTE-TIP-001`: the repaired broad backup had already advanced local and remote `main` together while excluding the credential from the remote tip.
- Resolved finding `R4-HISTORY-001`: `google-workspace` is disabled in `default` and `wolong`; both prior tokens fail live refresh as revoked or invalid; all profile client/token files and the Workspace OAuth credential file were removed without a secret backup. The old `th-earth` OAuth client deletion is owner-confirmed.
- Git security apply: `git-filter-repo 2.47.0` rewrote exactly 63 commits from first exposure through `main` and moved only remote `main` with force-with-lease, from `d1ada06aed69aacc8ba12c80bb81fa3b8a247b20` to `2026a231fbc10e913fae32acf05d35c6f8e88c55`. A rejected full rewrite was never pushed because it would have stripped an earlier GitHub merge signature and changed 102 commits; the accepted partial rewrite preserves that signed commit byte-for-byte. Fresh remote fetch across the sole branch, zero tags, and one unaffected pull ref is clean; the old head is unreachable; the original clone reflogs and objects were pruned.
- Nonblocking R5 inputs: 15 unconsumed profile wrappers, two generated watcher copies for terminal task `t_4b987a3b`, two unloaded Wolong Dashboard source plists, and the now-unconsumed Dashboard proxy source were classified but not removed. Root `kanban_task_watcher.py` remains a canonical compatibility entrypoint used by the Wolyeong generator.
- Verification: previous fail-closed secret canaries remain passed. After the rewrite, Workspace local, origin, and remote `main` match; the repository is clean; a direct backup smoke made no commit; the canonical launchd label is enabled and loaded, and one bounded run completed with exit `0`. Both Hermes gateways retained their PIDs and were not restarted.
- Rollback: the non-secret security package is `/Users/draccoon/Workspace/Hermes/update-backups/20260806T044956+0900-rk-v0191-task16-r4-security-apply/`; checksums pass. Config and launchd rollback remain available. Historical rollback is intentionally unavailable after verified cleanup because it would reintroduce the exposed credential history.
- Evidence: `root-kernel/evidence/v0.19.1-task16-r4-automation.json`, SHA-256 `4df1e6f59b8c7c64a0a3beff130e72217293b2398f8f29601f41e8f73f312d85`; impact assessment `root-kernel/evidence/v0.19.1-task16-r4-security-impact.json`, SHA-256 `48eeddf79004823fb4d34c62b96bd40b03490973077775d4819de9eb3de52bd4`; apply receipt `root-kernel/evidence/v0.19.1-task16-r4-security-apply.json`, SHA-256 `8920884e489d8727bae4274f49d328d50bb1b5d4ac0fd7d5185653f62e1ef1ae` (local, Git-excluded).
- Next action: R4 is owner-accepted. R5 remains pending and must not start without separate direction.

### Task 16 R5 Profile-owned local asset optimization

- Technical verdict: `passed`; owner acceptance: `accepted` at `2026-08-06T17:30:00+09:00`.
- Security cleanup: `auth/google_oauth.json` and lock files removed from `default` and `wolong` (expired tokens for deleted `th-earth` client, R4 scope gap). `profiles/wolong/.env.pre-telegram-restore-20260404-001451` removed (stale secret-bearing backup).
- R4-AUTOMATION-002 resolved: two `t_4b987a3b` watcher scripts removed (completed task, no consumer); 125 stale kanban-watcher and `watch_*` state files removed.
- R4-AUTOMATION-003 resolved: two wolong Dashboard source plists removed (neither installed nor loaded after R3 Dashboard retirement); empty `launchd/` dir removed.
- Additional optimization: 284 old kanban workspace directories removed (default 144 + wolong 140); 3 `.omx` metadata dirs removed.
- Preserved: `scripts/kanban_task_watcher.py` (canonical compatibility entrypoint); 15 active profile-owned scripts; 49 cron stores.
- Verification: both profile `config check` pass; gateway PIDs `30334` and `9976` unchanged; launchd automation loaded and enabled; all removed files confirmed gone; preserved files confirmed present.
- Rollback: non-secret backup under `/Users/draccoon/Workspace/Hermes/update-backups/20260806T1700-rk-v0191-task16-r5-asset-optimization/`; checksums pass. Secret rollback intentionally unavailable.
- Evidence: `root-kernel/evidence/v0.19.1-task16-r5-asset-optimization.json`, SHA-256 `96cf50b9b6ca6fb84f9e0bb8ef272b1ae82887a22b14cd029d948c48745bf29a` (local, Git-excluded).
- Next action: none. Release-candidate commit, tag `rk/tag/v0.19.1`, push, and `rk/live` movement completed at `2026-08-07`; v0.19.1 is released.

## Activation and rollback boundaries

Task 15 activation is technically passed and owner-accepted. The activation prerequisites below are satisfied:

- D1–D7 each have an explicit owner direction and current evidence.
- Candidate-focused, state, skill, automation, gateway, and rollback smokes pass.
- The 49-profile semantic config outcome is approved, including STT language.
- A typed, non-secret rollback package is created and restored in a disposable path.
- Any real state database backup/canary has separate sensitive-data approval.
- External control is ready for the root no-self-restart boundary.

The local live backend runtime is v0.19.1. The tag blocker is cleared; all post-live R gates are owner-accepted.

No `.env`, `auth.json`, token, credential pool, private key, or real state database may be copied into this repository or ordinary evidence.

## Documentation parity checklist

Before every commit-ready report, compare this document and
`root-kernel/carry.yaml` for:

- target and previous baselines;
- local and remote ref observations;
- current D ID and previous-release lineage;
- D and R status;
- tag and activation blockers;
- evidence paths;
- live-mutation state;
- rollback authority;
- next action.

Also compare the active carries with `root-kernel/feature.md`. The feature
guide must describe every active user-visible carry and its current operator
action without copying release chronology or machine-only evidence.

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

D1–D7 and Tasks 13–15 are owner-accepted and committed. R1–R5 are owner-accepted. v0.19.1 is released: tag `rk/tag/v0.19.1` created, candidate pushed, and `rk/live` moved to v0.19.1.
