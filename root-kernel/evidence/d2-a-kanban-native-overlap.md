# D2-a — Kanban native-overlap audit for Root Kernel v0.18.2

- Branch: `rk/v0.18.2`
- Upstream base: Hermes Agent `v0.18.2` / tag `v2026.7.7.2` / commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Audit timestamp: `2026-07-09T20:18:11+09:00`
- Scope: audit/ledger only; no product-code mutation.
- Decision: `partial-native local-minimized carry`.

## Outcome

D2 is **not fully upstream-absorbed** in v0.18.2. Upstream now has stronger Kanban foundations than the v0.17 carry point, so the old D2 chain must not be replayed wholesale. The user-facing Root Kernel D2 workflow should remain compatible, but implementation should reuse native v0.18.2 review/goal/notify/swarm surfaces and add only missing same-card seams.

## Native v0.18.2 foundations to preserve

- Native review foundation: `review` status, `claim_review_task`, review dispatch, and `has_spawnable_review`.
- Notification foundation: `kanban_notify_subs`, `add_notify_sub`, CLI notify subscribe/list/unsubscribe, dashboard home-subscribe, and gateway Kanban notifier.
- Goal foundation: `/goal` completion contracts plus Kanban `goal_mode` / `goal_max_turns` and worker completion judge gating.
- Delegation foundation: background `delegate_task` fan-out for helper work.
- Swarm foundation: `hermes_cli/kanban_swarm.py` Swarm v1 graph (`parallel workers -> verifier -> synthesizer`) with blackboard root.
- Generic workflow metadata: `workflow_template_id` and `current_step_key`.

## Missing Root Kernel D2 contract

The following v0.17 D2 contract pieces are still absent or not equivalent in v0.18.2:

| Subitem | v0.18.2 status | D2-a classification |
|---|---|---|
| D2-b same-card handoff | CLI `reassign/reclaim` exists, but worker cooperative same-card handoff does not. | Carry minimal seam. |
| D2-c submit-for-review | Native review queue/claim/dispatch exists, but worker-facing submit-review transition does not. | Reuse native review; carry submission seam. |
| D2-d request-changes | Reviewer return-to-rework loop is absent. | Carry minimal seam. |
| D2-e creator final gate | Reviewer approval is not split from creator/final approval. | Carry minimal seam. |
| D2-f review watcher | Generic notifier exists, but review-specific `requested_changes` / `review_accepted` loop is absent. | Extend notifier minimally. |
| D2-g result acceptance loop | Creator/acceptor result submission loop is absent. | Carry minimal seam. |
| D2-h mutex key | `tasks.mutex_key` and mutex dispatch/direct-claim guards are absent. | Carry independent seam. |
| D2-i workflow context banner | `workflow_template_id/current_step_key` exist, but closed Root Kernel workflow banners are absent. | Carry banner seam without replacing upstream metadata. |

## Symbol probe evidence

Command shape:

```bash
cd /Users/draccoon/Workspace/Hermes/17th-hermes-agent-worktree
env -u HERMES_KANBAN_DB -u HERMES_KANBAN_BOARD \
  HERMES_HOME="$(mktemp -d)" \
  /Users/draccoon/.hermes/hermes-agent/venv/bin/python - <<'PY'
from hermes_cli import kanban_db as kb
import tools.kanban_tools as kt
missing=[]
for name in ['handoff_task','submit_task_for_review','request_changes_task','submit_task_result']:
    if not hasattr(kb, name): missing.append('kanban_db.'+name)
for name in ['kanban_reassign','kanban_submit_review','kanban_request_changes','kanban_submit_result']:
    if name not in getattr(kt, '__dict__', {}):
        missing.append('tools surface '+name)
print('missing_d2_symbols=' + ','.join(missing))
print('has_native_review=', hasattr(kb,'claim_review_task'), hasattr(kb,'has_spawnable_review'))
print('task_has_workflow_template=', 'workflow_template_id' in kb.Task.__dataclass_fields__, 'current_step_key' in kb.Task.__dataclass_fields__)
print('task_has_d2_fields=', 'mutex_key' in kb.Task.__dataclass_fields__, 'workflow_type' in kb.Task.__dataclass_fields__)
PY
```

Observed result:

```text
missing_d2_symbols=kanban_db.handoff_task,kanban_db.submit_task_for_review,kanban_db.request_changes_task,kanban_db.submit_task_result,tools surface kanban_reassign,tools surface kanban_submit_review,tools surface kanban_request_changes,tools surface kanban_submit_result
has_native_review= True True
task_has_workflow_template= True True
task_has_d2_fields= False False
```

## Focused smoke evidence

Native review slice:

```bash
HERMES_HOME="$(mktemp -d)" /Users/draccoon/.hermes/hermes-agent/venv/bin/python -m pytest -q -o addopts= \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_transitions_to_running \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_fails_on_non_review \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_fails_when_already_claimed \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_dry_run \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_spawns_with_correct_skills \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_skips_unassigned \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_skips_nonspawnable \
  tests/hermes_cli/test_kanban_db.py::test_has_spawnable_review_true \
  tests/hermes_cli/test_kanban_db.py::test_has_spawnable_review_false_on_empty \
  tests/hermes_cli/test_kanban_db.py::test_review_status_in_valid_statuses
```

Result:

```text
10 passed in 0.76s
```

Overlap mapping slice:

```bash
HERMES_HOME="$(mktemp -d)" /Users/draccoon/.hermes/hermes-agent/venv/bin/python -m pytest -q -o addopts= \
  tests/hermes_cli/test_kanban_db.py::test_list_tasks_filters_workflow_template_and_step \
  tests/hermes_cli/test_kanban_db.py::test_claim_review_task_transitions_to_running \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_dry_run \
  tests/hermes_cli/test_kanban_db.py::test_dispatch_review_spawns_with_correct_skills \
  tests/hermes_cli/test_kanban_db.py::test_has_spawnable_review_true \
  tests/tools/test_kanban_tools.py::test_complete_goal_mode_rejected_by_judge \
  tests/tools/test_kanban_tools.py::test_create_subscribes_gateway_session \
  tests/tools/test_kanban_tools.py::test_create_does_not_subscribe_in_cli_session \
  tests/gateway/test_kanban_notifier.py
```

Result:

```text
15 passed in 1.37s
```

## v0.17 lineage

The previous Root Kernel D2 chain was carried as separate commits:

```text
3961b513b [D2-b] Add Kanban same-card handoff tool
b6d3d7aa3 [D2-c] Add Kanban same-card review submission
19e3a3251 [D2-d] Add Kanban request-changes rework flow
05de5df63 [D2-e] Add Kanban creator final gate
7ed82be9d fix: [D2-f] notify async Kanban review outcomes
3ec3d21c5 fix(rk): [D2-g] add Kanban result acceptance loop
74edd5bee fix(rk): [D2-h] serialize Kanban tasks by mutex key
8c091f1b9 fix(rk): [D2-i] add Kanban workflow context banners
```

## Decision and next sequence

D2-a closes as an audit-only checkpoint. The next D2 work should proceed subitem-by-subitem:

1. `D2-b/c/d/e`: core same-card handoff, submit-review, request-changes, and creator/final gate loop, preserving upstream native review claim/dispatch.
2. `D2-f`: review-outcome watcher/notification extension on top of existing notify subscriptions.
3. `D2-g`: creator/acceptor result submission loop.
4. `D2-h`: mutex-key serialization.
5. `D2-i`: workflow-type banners beside upstream workflow metadata.

## Boundary

No live profile state, gateway, token, production Kanban DB, `rk/live`, push, or tag was mutated by this audit. Product-code patches remain pending for D2-b through D2-i.
