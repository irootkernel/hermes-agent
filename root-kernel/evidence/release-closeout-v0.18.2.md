# Root Kernel Hermes Agent v0.18.2 release closeout

- Status: ready for publication
- Operator authorization: 2026-08-01T19:09:09+09:00
- Release branch: `rk/v0.18.2`
- Live branch: `rk/live`
- Annotated tag: `rk/tag/v0.18.2`
- Candidate pre-closeout head: `217d28ddd5aed9e7f82764d8b8e049e9f9dcc9a3`
- Ops repository commit: `d35460fd1fdec5105d7d7068843602b7c77163eb`
- Previous live/rollback commit: `79780a587ecb260788a23767d9996d5f7042a311`
- Rollback ref in the live checkout repository: `rk/rollback/pre-v0.18.2-20260801T014431`
- Force-with-lease authorization: `2026-08-01T20:25:29+09:00`
- Expected old remote `rk/live`: `79780a587ecb260788a23767d9996d5f7042a311`

## Exact base

- Upstream version: Hermes Agent `v0.18.2`
- Upstream release tag: `v2026.7.7.2`
- Peeled upstream tag commit: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- Candidate merge-base with the peeled tag: `9de9c25f620ff7f1ce0fd5457d596052d5159596`
- `git merge-base --is-ancestor v2026.7.7.2^{} HEAD`: exit 0

The CLI banner's `upstream c3c60ccb` decoration is a fork merge-base display. `c3c60ccb` is an earlier local D4 commit and is not the selected upstream release base.

## Runtime evidence

- Live Hermes reports `v0.18.2`.
- The local live branch was activated at `217d28ddd5aed9e7f82764d8b8e049e9f9dcc9a3`.
- Twelve running gateways use `/Users/draccoon/.hermes/hermes-agent/venv/bin/python`.
- Forty-nine profile config checks and fresh skill resolvers pass.
- Every profile retains 72 exact bundled skills.
- Managed skill state is fleet 5 plus Munang admin 10; official optional retention is zero.
- Managed governance and integrated script governance return zero violations.
- Default and Biui doctor commands return exit 0.

## Accepted host cleanup

- R4 automation cleanup and governance are accepted.
- R5 profile-owned asset optimization is accepted.
- The later managed-root consolidation and official optional retirement were explicitly approved.
- Ops focused tests report 24 passed; plist lint, Python compile, shell syntax, and diff check pass.
- Candidate D2/D4/D6/D7/D8 targeted suite reports 1394 passed and zero failed.
- Independent read-only ops review passed with no security, logic, or scope blockers.
- Independent candidate SOT review passed after the exact force-with-lease publication contract was recorded.
- High-confidence added-line and untracked-file credential scan reports zero findings.

## Publication contract

The closeout commit containing this evidence is the intended common target of:

1. remote `rk/v0.18.2`;
2. remote `rk/live` via an exact force-with-lease repoint from `79780a587ecb260788a23767d9996d5f7042a311`;
3. annotated tag `rk/tag/v0.18.2`.

No force push or history rewrite is authorized except the operator-approved exact force-with-lease repoint of remote `rk/live`. The release must abort if the remote value differs from the recorded v0.17 commit. The tag must not be created until the ops repository commit is published, the candidate diff is reviewed, and final tests pass.

## Separate non-blocking work

ATN live daemon activation and retired persona/channel prompt cleanup are separate operations. They are not absorbed into this release.
