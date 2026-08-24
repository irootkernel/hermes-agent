# Root Kernel Hermes Agent v0.20.5 Release Ledger

This ledger records the v0.20.5 candidate decisions and evidence. Current candidate behavior and configuration belong in `root-kernel/feature.md`; machine-readable state belongs in `root-kernel/carry.yaml`. The complete v0.19.1 execution history remains immutable at `rk/tag/v0.19.1` and is not copied into this release.

## Release state

- Status: `s9-activation-prep-passed-s10-held`
- Candidate branch: `rk/v0.20.5`
- Candidate HEAD before scaffold: `fcbd1076a93841fa88855acce810e342a5b78101`
- Candidate publication: not committed, not pushed, not tagged
- Live activation: not started; S9 preparation passed
- Current live release: v0.19.1 at `7e65112b5303e9aa30cda440c2ab498bf5f360bc`
- Current candidate delta: owner-accepted D1-D4/D6, S8 atomicity remediation, and the three Root Kernel documents
- Active carry decisions: D1-D4, D6, and S8 owner-accepted; S9 activation preparation authorized
- Omitted carry decisions: D5 and D7

## Exact upstream baseline

| Field | Value |
|---|---|
| Package version | `0.20.5` |
| Upstream tag | `v2026.8.19` |
| Annotated tag object | `b05e680e63d39d5a8e3ec0f5842a41d1c4209c03` |
| Peeled release commit | `fcbd1076a93841fa88855acce810e342a5b78101` |
| Candidate branch | `rk/v0.20.5` |
| Signature status | unsigned or unverifiable |
| Identity claim | tag object, peeled commit, and package version verified; no cryptographic-signature claim |
| Baseline worktree | clean |
| Baseline upstream delta | 0 files |
| Baseline Root Kernel files | 0 files before scaffold |

The candidate was created directly at the peeled upstream release commit. It was not built by merging `rk/v0.19.1`, replaying all prior carries, or merging a newer upstream `main`.

## Prior release authority

| Field | Value |
|---|---|
| Previous release | v0.19.1 |
| Previous candidate/live head | `7e65112b5303e9aa30cda440c2ab498bf5f360bc` |
| Previous release tag | `rk/tag/v0.19.1` |
| Previous tag object | `1f3e105fa1f141a736b362dc4151e0136c19a189` |
| Historical documents | `rk/tag/v0.19.1:root-kernel/{carry.yaml,feature.md,ledger.md}` |

Historical D-item IDs are preserved. D5 and D7 remain historical facts in v0.19.1 but are omitted from the current v0.20.5 feature and code contract.

## Owner decisions

1. Use the three-document Root Kernel structure: `carry.yaml`, `feature.md`, and `ledger.md`.
2. Do not recreate `for-root-kernel.md`.
3. Retain and re-audit D1, D2, D3, D4, and D6.
4. Omit all downstream D5 Kanban product/schema/tool/prompt/watcher/test behavior.
5. Omit D7 doctor warning filtering and accept upstream diagnostics.
6. Work gate-by-gate with separate owner approval for each subtask.
7. Reimplement only exact remaining behavior gaps at current v0.20.5 chokepoints; do not replay historical patches wholesale.

## Completed gates

### S0: release delta investigation

- Status: completed
- Scope: official v0.20.0–v0.20.5 releases, exact v0.19.1→v0.20.5 source delta, breaking/deprecation/removal/rename, and Root Kernel carry impact
- Report: `/Users/draccoon/Workspace/Hermes/vault/Hermes/00-inbox/hermes-agent-v0-19-1-to-v0-20-5-release-delta-report.md`
- Result: v0.20.5 expands native Kanban, Bot Mode/group-room, credential pools, cron/memory, profile/worktree/update, MCP, and provider paths, but does not prove exact replacement of D1–D4 or D6

### S1: preflight backup and exact candidate baseline

- Status: completed and owner-approved
- Source dirty state: `rk/v0.19.1` at `7e65112b…`, 23 modified files, +6,276/−3,986
- Backup: `/Users/draccoon/Workspace/Hermes/backups/20260824-030645-rk-v0205-preflight`
- Binary patch: 559,795 bytes, SHA-256 `ebde73e83bd2a55ed16a4e58d72d4d4b18060e536f83c8ba325942652341f248`
- Restore probe: `git apply --check`, actual apply, file SHA-256 parity, and numstat parity passed
- Backup manifest: 12 entries, all verified
- Source cleanup: passed after backup verification
- Upstream remote: fetch URL `https://github.com/NousResearch/hermes-agent.git`; push URL disabled
- Candidate branch: created locally at exact peeled commit
- Remote candidate branch, release tag, and live ref: unchanged
- Live clone: remained clean on v0.19.1

### S2: three-document release scaffold

- Status: completed and owner-accepted
- Intended changed paths:
  - `root-kernel/carry.yaml`
  - `root-kernel/feature.md`
  - `root-kernel/ledger.md`
- Behavioral code or tests: none
- Verification: YAML parse, cross-document parity, stale-current-claim scan, path policy, whitespace scan, diff check, and three-path guard passed
- Owner acceptance: accepted on 2026-08-24; authorization scope includes proceeding to S3/D1

## Carry decision matrix

| ID | Decision | Current status | v0.20.5 overlap | Required next evidence |
|---|---|---|---|---|
| D1 | retain-minimal implemented | owner-accepted | CJK/FTS behavior evolved; three raw recovery/verification connections lacked tokenizer registration | Complete |
| D2 | retain-minimal implemented | owner-accepted | Skill ledger and approval transport improved; import/evaluator failure seams remained | Complete |
| D3 | retain-minimal implemented | owner-accepted | Credential pools and refresh expanded substantially but exact ownership gaps remained | Complete |
| D4 | retain-minimal implemented | owner-accepted | Bot Mode, group-room, participation, mention and thread behavior expanded | Complete |
| D5 | omit completely | omitted | Native Kanban expanded | Final zero-delta and forbidden-symbol guard only |
| D6 | retain-minimal implemented | owner-accepted | Nonzero return propagation exists but `True` became exit 1 | Complete |
| D7 | omit | omitted | Doctor diagnostics expanded | Final zero-delta guard only |

## Historical carry lineage

| Current ID | v0.19.1 evidence commit |
|---|---|
| D1 | `deb6fc641599d45e9714bebf61101128d0ca950b` |
| D2 | `49fa643064dadf3657d78be5139541079e262df0` |
| D3 | `c05d64572c01482e3619ce2850e8c6c4e0465938` |
| D4 | `c82a9b6b6bdb8f672312d0deeca302a221608bf3` |
| D6 | `11847601d5da3efe68e768e633e768482175c99a` |
| Omitted D7 | `4ca7afa4f7d2afddea0e765b47e645e0765dc012` |

These commits demonstrate historical contracts only. They are not approved cherry-picks and must not be applied wholesale.

## Candidate change boundary

The candidate changes are limited to the accepted D1-D4 paths, D6's `hermes_cli/main.py` and actual-process test, and the three Root Kernel documents recorded in `carry.yaml`.

Final-release changes may include only the source-traced, evidence-backed D1–D4 and D6 paths plus these documents. D4's allowed paths are finalized in `carry.yaml`.

The release fails if downstream changes appear in:

- native Kanban product, schema, CLI, tool, prompt, watcher, dispatcher, or tests;
- downstream doctor warning filtering;
- stale D5 symbols such as `mutex_key`, `workflow_type`, `kanban_submit_result`, or a same-card watcher;
- any source or test path not recorded for an accepted carry.

## Evidence matrix

| Gate | RED | GREEN | Adjacent | Independent review | Owner acceptance |
|---|---|---|---|---|---|
| D1 | reproduced: `no such tokenizer: cjk_unicode61` | 2 focused CJK tests passed | primary 6 passed; sibling 7 passed; Ruff passed | passed; no blocking findings | accepted 2026-08-24 |
| D2 | import fail-open and evaluator exception reproduced | 2 focused tests passed | skill manager and write approval 64 passed; Ruff passed | passed; no blocking findings | accepted 2026-08-24 |
| D3 | 38 focused failures reproduced | 38 focused tests passed | 359 D3 full-related and 414 D1-D3 cumulative tests; Ruff/static scan passed | passed; 0 blocking findings on newest snapshot | accepted 2026-08-24 |
| D4 | 17 reproduced | 24 focused passed | 84 full-related; 498 cumulative | `deleg_19ae757b` passed | accepted 2026-08-24 |
| D6 | `True` became exit 1 | 6 focused passed | 11 related; 504 historical cumulative receipt | `deleg_51f7ddda` passed | accepted 2026-08-24 |
| Integrated candidate | n/a | newest snapshot: 144 files/1,520 passed | exact guards and baseline classification passed | sixteen reviews found blockers; all findings remediated | pending re-review |
| Activation/rollback | n/a | pending | pending | pending | pending |
| Post-live | n/a | pending | pending | pending | pending |

No pending cell may be rewritten as passed without real command output or a durable evidence receipt.

## S3 / D1 execution record

- Authorization: owner authorized S3/D1 on 2026-08-24.
- Current-target root cause: `SessionDB` registers `cjk_unicode61` per SQLite connection, but normal recovery destination, lost-and-found destination, and final verification reopened the CJK-enabled output with raw connections that did not load the extension.
- RED, normal path: message copy returned `status=failed`, `copied_rows=0`, error `no such tokenizer: cjk_unicode61`.
- RED, sibling path: lost-and-found direct-table mapping raised `sqlite3.OperationalError: no such tokenizer: cjk_unicode61`.
- Minimal product change: import the existing best-effort loader and invoke it at those three connection boundaries; no new setting, schema, CLI, or fallback behavior.
- Focused GREEN: `pytest -q tests/hermes_cli/test_session_recovery.py -k 'cjk_index_enabled' -v --tb=short` -> 2 passed, 4 deselected.
- Primary regression: `scripts/run_tests.sh tests/hermes_cli/test_session_recovery.py -v` -> 6 passed.
- Sibling regression: `scripts/run_tests.sh tests/hermes_cli/test_session_recovery_lost_and_found.py -v` -> 7 passed.
- Lint: Ruff passed for the D1 source and test files.
- Static security scan: no findings.
- Source immutability, separate output, canonical counts, complete status, `PRAGMA integrity_check`, CJK FTS integrity, and Korean search are asserted by the focused test.
- Independent review: passed with no security concerns, logic errors, or scope issues. Three test-hardening suggestions were non-blocking and are retained in `carry.yaml` for later CI/integrated-verification consideration.
- Owner acceptance: accepted by the owner response `승인` on 2026-08-24 at 10:22:52 +09:00.

## S4 / D2 authorization record

- D2 current-target re-audit and a focused RED for any confirmed gap are authorized by the same owner response.
- Historical commit `49fa6430…` remains evidence only and must not be replayed.
- No D2 production change is authorized unless exact v0.20.5 first fails the remaining fail-close contract.

## S4 / D2 execution record

- Current-target root cause: `_apply_skill_write_gate` explicitly returned `None` when `tools.write_approval` import failed, and called `evaluate_gate` outside the protected boundary so evaluator exceptions escaped.
- RED, import path: `skill_manage(create)` returned success and created `SKILL.md` while the approval dependency was unavailable.
- RED, evaluation path: `RuntimeError("boom")` escaped instead of returning a structured refusal.
- Minimal product change: evaluate the gate in the existing import `try` and return the existing `tool_error` shape on either availability failure.
- Focused GREEN: `TestWriteApprovalGate` -> 2 passed.
- Adjacent regression: `test_skill_manager_tool.py` and `test_write_approval.py` -> 64 passed.
- Ruff and static security scan: passed with no findings.
- Independent review: passed with no security concerns, logic errors, or scope issues. Three non-blocking hardening suggestions are retained in `carry.yaml` for integrated verification consideration.
- Owner acceptance: accepted by the owner response `승인` on 2026-08-24 at 14:08:06 +09:00.

## S5 / D3 authorization record

- D3 current-target source tracing and focused RED tests for confirmed gaps are authorized by the same owner response.
- Historical commit `c05d6457…` remains evidence only and must not be replayed.
- No credential value may enter source, tests, logs, evidence, or Root Kernel documents.
- No D3 production change is authorized until exact v0.20.5 behavior has been traced and a remaining contract gap is reproduced.

## S5 / D3 execution record

- Current-target root cause: the generic credential pool never read an active-profile exact pin; main and auxiliary Codex resolution fell through to singleton credentials; labelled Codex auth always appended a new row.
- RED: 38 focused failures reproduced ignored ID/label pins, sibling selection and lease, singleton fallback, append-only reauth, duplicate-label login, ineligible-label append, sibling refresh side effects, broad canonical-row overwrite, sibling-derived availability/recovery status, canonical reload ownership corruption, stale recovery hints mutating siblings, manual-account singleton adoption, direct singleton recovery bypass, pre-pin load seeding, stale-snapshot concurrent sibling overwrite, status sibling leakage, unavailable-pin recovery return, stale full-pool persistence overwriting concurrent sibling token rotation, canonical target-change during login, auxiliary unscoped 401 refresh, omitted active-pin structural add persistence, incomplete active-pin status reset persistence, concurrent canonical-row addition during login, stale clean snapshots skipping latest disk-only status changes, explicit main-runtime pin bypass, stale structural remove, stale add priority, pinned cooldown-clear sibling overwrite, and non-exact aged-DEAD auto-prune.
- Minimal product change: resolve active-profile exact ID before unique label in existing pool selection/current/peek/lease paths; reject unavailable pins before main or auxiliary singleton fallback; update one exact existing OAuth device-code row for labelled reauth and reject duplicates before login.
- Security hardening: unreadable profile pin source propagates failure instead of being interpreted as no pin; ambient process environment cannot configure a pin; no credential value was read or recorded.
- First independent review: failed with two blocking account-isolation findings: pinned selection refreshed siblings, and canonical labelled reauth overwrote all device-code rows.
- Remediation: pin-configured availability scopes sync/refresh/prune and status/recovery reporting to the exact candidate; labelled canonical reauth passes an opt-in exact target ID while ordinary singleton save behavior remains unchanged.
- Remediation RED/GREEN: 2 review findings failed then passed; 4 status-API cases failed then passed.
- Second independent review: failed because exact canonical-row reauth was not stable when multiple canonical rows were deduplicated on reload.
- Second remediation: duplicate canonical rows fail closed before login; a single canonical row plus independent manual sibling remains exact after reload.
- Second remediation RED/GREEN: 1 failed, then 2 passed.
- Canonical-pin corruption parity: 1 failed, then 1 passed.
- Recovery API pin-scope parity: 1 failed, then 1 passed.
- Adjudication remediation: manual device-code rows no longer sync singleton tokens; direct singleton resolution fails before auth-store access when a Codex pin exists.
- Adjudication remediation RED/GREEN: 2 failed, then 2 passed.
- Delayed-review remediation: active pins skip load-time sibling seeding/persistence; manual labelled reauth atomically reloads and updates one exact target under lock.
- Delayed-review remediation RED/GREEN: 2 failed, then 2 passed.
- Status/recovery remediation: configured pins suppress pool-wide status fallback; stale sibling failure cannot return an exhausted or dead pin.
- Status/recovery remediation RED/GREEN: 2 failed, then 2 passed.
- Atomic persistence remediation: active pins replace one exact target row under the auth-store lock and never rewrite sibling rows from the in-memory snapshot.
- Atomic persistence remediation RED/GREEN: 1 failed, then 1 passed.
- Canonical reauth/recovery remediation: exact canonical target is revalidated under lock before singleton mutation; auxiliary 401 refresh is failed-identity-aware.
- Canonical reauth/recovery remediation RED/GREEN: 2 failed, then 2 passed.
- Structural add remediation: active pins append one new credential under the auth-store lock without rewriting concurrent siblings.
- Structural add remediation RED/GREEN: 1 failed, then 1 passed.
- Reset/cardinality remediation: latest disk rows are status-reset atomically and canonical labelled reauth revalidates global eligible canonical uniqueness after login.
- Reset/cardinality remediation RED/GREEN: 2 failed, then 2 passed.
- Latest-disk reset remediation: active pins always reset latest disk rows, include reason-only fields, and return actual changed-row count.
- Latest-disk reset remediation RED/GREEN: 1 failed, then 1 passed.
- Explicit/remove/priority remediation RED/GREEN: 3 failed, then 3 passed.
- Automatic status/prune remediation RED/GREEN: 2 failed, then 2 passed.
- Focused GREEN: four D3 test files with `-k d3_credential` -> 38 passed.
- D3 full-related regression: four D3 test files through `scripts/run_tests.sh` -> 359 passed.
- Cumulative downstream regression: D1–D3 six changed test files in one canonical run -> 414 passed.
- Evidence correction: prior 382/452 figures double-counted focused tests; canonical runner summaries are authoritative.
- Ruff and added-line static security scan: passed with no findings.
- Scope adjudication and delayed reviews found eighteen further real Codex blockers; all are remediated.
- Newest-snapshot independent review passed with zero blocking findings; three follow-up suggestions are non-blocking and recorded in carry.yaml.
- D3 owner acceptance: accepted by the owner response `승인` on 2026-08-24 at 17:37:02 +09:00.
- D4 exact-target re-audit and minimal implementation are authorized; refs promotion and live activation remain locked.

## Publication state

| Ref/action | State |
|---|---|
| Local `rk/v0.20.5` | created at upstream baseline |
| Commit scaffold | not authorized yet |
| Push `rk/v0.20.5` | not authorized |
| Create/push `rk/tag/v0.20.5` | not authorized |
| Move `rk/live` | not authorized |
| Activate live clone | not authorized |

The literal `rk/tags/v02.20.5` is prohibited unless the owner explicitly chooses that exceptional spelling.

## Activation and rollback boundary

No profile, config, state DB, skill, plugin, cron job, credential, gateway, service, launcher, remote ref, or live checkout was changed by S2.

Current rollback authorities:

1. Candidate rollback: discard all paths in the exact 22-path candidate manifest against HEAD `fcbd1076…`; removing only the three `root-kernel/` files does not return to upstream v0.20.5. Preserve unrelated work.
2. Preflight dirty-state rollback: apply the verified `worktree.patch` to v0.19.1 commit `7e65112b…`.
3. Live rollback: not yet applicable because live remains unchanged at v0.19.1.
4. State rollback: not yet applicable because no state DB was opened or migrated.

Before activation, a separate mode-restricted activation backup and migration rehearsal are mandatory. Code-only downgrade against a state DB migrated from schema 23 to 26 is not an accepted rollback procedure.

## Documentation parity checklist

- [x] Three canonical document paths used
- [x] `for-root-kernel.md` absent
- [x] Exact upstream tag object, peeled commit, and package version recorded
- [x] Prior-release authority points to `rk/tag/v0.19.1`
- [x] Active IDs are D1, D2, D3, D4, D6
- [x] D5 and D7 are omitted from the current behavior contract
- [x] No-downstream-Kanban invariant recorded
- [x] No-downstream-doctor-filter invariant recorded
- [x] Publication, activation, and rollback state recorded
- [x] YAML parse and cross-document automated verification
- [x] S2 owner acceptance
- [x] D1 RED reproduced on exact v0.20.5
- [x] D1 focused GREEN and adjacent regressions
- [x] D1 independent review
- [x] D1 owner acceptance
- [x] D2 RED reproduced on exact v0.20.5
- [x] D2 focused GREEN and adjacent regressions
- [x] D2 independent review
- [x] D2 owner acceptance
- [x] D3 RED reproduced on exact v0.20.5
- [x] D3 focused GREEN and expanded adjacent regressions
- [x] D3 Ruff and static security scan
- [x] D3 first independent review completed with two blocking findings
- [x] D3 review findings reproduced and remediated RED/GREEN
- [x] D3 second independent review completed with one blocking finding
- [x] D3 reload-stability finding reproduced and remediated RED/GREEN
- [x] D3 final independent review
- [x] D3 owner acceptance
- [x] D4 exact-target re-audit and eight RED reproductions
- [x] D4 focused GREEN and related/cumulative regressions
- [x] D4 Ruff and diff guard
- [x] D4 first independent review completed with four blocking findings
- [x] D4 review findings reproduced in five RED tests and remediated GREEN
- [x] D4 second independent review completed with one blocking finding
- [x] D4 recovery pre-admission mutation reproduced and remediated RED/GREEN
- [x] D4 third independent review completed with one blocking finding
- [x] D4 recovery/live dedup race reproduced and remediated RED/GREEN
- [x] D4 fourth independent review completed with one blocking finding
- [x] D4 mention-only owner poisoning reproduced on live/recovery and remediated RED/GREEN
- [x] D4 final independent review passed with zero blocking findings
- [x] D4 owner acceptance recorded at `2026-08-24T19:22:55+09:00`
- [x] D6 actual-process RED reproduced: `True` returned exit 1
- [x] D6 one-line exact-integer GREEN: 6 focused tests
- [x] D6 related regression: 11 passed across 3 files
- [x] D1-D6 cumulative regression: 504 passed across 11 files
- [x] D6 Ruff, static scan, compilation, and diff guard
- [x] D6 final independent review `deleg_51f7ddda` passed with zero blockers
- [x] D6 owner acceptance recorded at `2026-08-24T19:51:46+09:00`
- [x] S8 clean selected gate: 144 files, 1,487 passed, 2 Windows-only skips
- [x] S8 full-run classification: 26 files/89 failures match clean upstream; three candidate-only transients pass 11/11 isolated; zero persistent candidate-only failures
- [x] S8 exact 22-path, D5/D7 forbidden-scope, retired-symbol, secret/security, compilation, Ruff, YAML, and diff guards
- [x] S8 disposable v0.20.5/schema-26 config/doctor/state smoke; directory removed
- [x] S8 independent review `deleg_691f25ed` completed with two blockers
- [x] D3 failed exact removal, failed status reset, and failed aged-prune preserve live memory; 3 focused and 84 full credential-pool tests passed
- [x] Root Kernel stale D4/S8/omitted-guard/activation claims reconciled
- [x] Remediated S8 selected gate: 144 files, 1,489 passed, 2 Windows-only skips
- [x] S8 re-review `deleg_6542efca` completed with two blockers
- [x] D3 successful reset, remove, and aged-prune now reconcile live memory to the authoritative locked disk snapshot; 6 focused and 86 full credential-pool tests passed
- [x] D4 path finality, shared cross-profile ownership wording, and next-action state reconciled
- [x] Newest remediated S8 selected gate: 144 files, 1,491 passed, 2 Windows-only skips
- [x] S8 third review `deleg_8568c1a8` completed with two blockers
- [x] Pinned status-only persistence now merges into the locked latest target row and reconciles live memory; 7 focused and 87 full credential-pool tests passed
- [x] Feature guide D6 and S8 current-state wording reconciled with carry and ledger
- [x] Latest remediated S8 selected gate: 144 files, 1,492 passed, 2 Windows-only skips
- [x] S8 fourth review `deleg_def093db` completed with two blockers
- [x] Pinned cooldown clearing uses persist-first latest-row status merge; success/failure reconciliation tests and 88 full credential-pool tests passed
- [x] Auto-thread ownership preclaim removed; mention-only and failed-hydration rejection probes passed, with 46 free-response and 156 combined related tests passing
- [x] Latest fourth-review-remediated S8 selected gate: 144 files, 1,495 passed, 2 Windows-only skips
- [x] S8 fifth review `deleg_f5726f00` completed with one D3 blocker
- [x] Pinned canonical token sync and refresh use full-row persist-first authoritative reconciliation; injected exact-save failure remains live/disk atomic, concurrent siblings reconcile, and 90 full credential-pool tests pass
- [x] Latest fifth-review-remediated S8 selected gate: 144 files, 1,497 passed, 2 Windows-only skips
- [x] S8 sixth review `deleg_a900f368` completed with D3 lock-continuity and stale-ledger blockers
- [x] Canonical provider-token read and exact target merge/save now execute under one auth-store lock; split-lock regression and 91 credential-pool tests pass
- [x] Latest sixth-review-remediated S8 selected gate: 144 files, 1,498 passed, 2 Windows-only skips
- [x] S8 seventh review `deleg_7410723f` completed with terminal-refresh atomicity and stale `failure_reason` blockers
- [x] Ambiguous identity now aborts before refresh; terminal quarantine atomically clears provider state and exact canonical rows before live reconciliation; provider adoption clears `failure_reason`; 93 credential-pool tests pass
- [x] Latest seventh-review-remediated S8 selected gate: 144 files, 1,500 passed, 2 Windows-only skips
- [x] S8 eighth review `deleg_5a09976d` completed with canonical eligibility, access-only race, and rollback-boundary blockers
- [x] Sync/quarantine require one eligible canonical identity, quarantine removes only the exact target, both token generations guard terminal races, rollback covers all 22 candidate paths, and 96 credential-pool tests pass
- [x] Latest eighth-review-remediated S8 selected gate: 144 files, 1,503 passed, 2 Windows-only skips
- [x] S8 ninth review `deleg_bb1c20b6` completed with provider-source provenance and live/recovered dedup parity blockers
- [x] Provider sync/quarantine lock the fallback source, terminal writes return to that source with exact active-store rollback on failure, live dispatch releases dedup on exception/cancellation, and 98 pool plus 48 free-response tests pass
- [x] Latest ninth-review-remediated S8 selected gate: 144 files, 1,507 passed, 2 Windows-only skips
- [x] S8 tenth review `deleg_83140d88` completed with global-source disappearance and stale machine-ledger blockers
- [x] Locked fallback disappearance now fails closed before sync/quarantine mutation, exact profile/root bytes remain unchanged, machine-ledger status is current, and 100 pool plus 48 free-response tests pass
- [x] Latest tenth-review-remediated S8 selected gate: 144 files, 1,509 passed, 2 Windows-only skips
- [x] S8 eleventh review `deleg_81a923c4` completed with one cross-store post-commit rollback blocker
- [x] Fallback quarantine now restores exact authoritative-source and active-profile bytes after a source save commits then raises; 101 pool plus 48 free-response tests pass
- [x] Latest eleventh-review-remediated S8 selected gate: 144 files, 1,510 passed, 2 Windows-only skips
- [x] S8 twelfth review `deleg_197efb17` completed with active-save compensation and rollback-diagnostic blockers
- [x] Both fallback saves share one compensation boundary; source and active rollback are independent, preserve the operation error, and emit explicit partial-state diagnostics; 104 pool plus 48 free-response tests pass
- [x] Latest twelfth-review-remediated S8 selected gate: 144 files, 1,513 passed, 2 Windows-only skips
- [x] S8 thirteenth review `deleg_f48c749d` completed with one restore parent-directory-fsync durability blocker
- [x] Exact rollback now fsyncs its replacement file and parent directory; actual directory-fsync failure on source and active restoration paths preserves the original operation error and explicit partial-state diagnostics; 107 pool plus 48 free-response tests pass
- [x] Latest thirteenth-review-remediated S8 selected gate: 144 files, 1,516 passed, 2 Windows-only skips
- [x] S8 fourteenth review `deleg_4c81ff70` completed with one successful-refresh cross-store atomicity blocker
- [x] Pinned canonical Codex refresh now transactionally persists the exact profile row and authoritative source before live reconciliation; source commit-then-raise restores both exact stores and propagates; 108 pool plus 48 free-response tests pass
- [x] Latest fourteenth-review-remediated S8 selected gate: 144 files, 1,517 passed, 2 Windows-only skips
- [x] S8 fifteenth review `deleg_d761edf9` completed with active-local commit compensation and provider-metadata parity blockers
- [x] Active-local and fallback refresh share one compensation boundary; active-local stores the full provider state with token-pair/last_refresh parity and exact rollback on commit-then-raise; 110 pool plus 48 free-response tests pass
- [x] Latest fifteenth-review-remediated S8 selected gate: 144 files, 1,519 passed, 2 Windows-only skips
- [x] S8 sixteenth review `deleg_c69470f4` completed with one global-fallback active-provider mutation blocker
- [x] Canonical refresh source persistence now uses set_active false, preserving distinct profile/global selections and unrelated metadata while persisting Codex token-pair/last_refresh parity; 111 pool plus 48 free-response tests pass
- [x] Latest sixteenth-review-remediated S8 selected gate: 144 files, 1,520 passed, 2 Windows-only skips
- [x] S8 seventeenth independent exact-snapshot review `deleg_43450386`: passed, zero blockers/security/correctness/scope findings
- [x] S8 owner acceptance: `승인` received 2026-08-25
- [x] S9 external activation backup: four mode-0600 v23 SQLite snapshots under mode-0700 backup root
- [x] S9 real-data disposable migration: four profiles v23→v26, integrity OK, zero foreign-key violations, session/message counts preserved
- [x] S9 atomic rollback rehearsal: four profiles restored byte-for-byte to v23 snapshots with file and parent-directory fsync
- [x] S9 live invariance: Hermes v0.19.1, four gateways running, four live databases remain integrity-OK v23
- [ ] S10 held by owner at 2026-08-25T00:47:33+09:00; v0.19.1 live state retained

## Next action

Remain on v0.19.1 until the owner explicitly resumes and approves S10. No commit, push, tag, ref promotion, live state migration, or live activation is authorized.
