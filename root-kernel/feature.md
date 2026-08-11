# Root Kernel Hermes Agent Feature and Operations Guide

Root Kernel Hermes Agent is a downstream distribution of
[NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent). It keeps the
upstream product intact and carries a small set of reviewed fixes and operational
extensions needed by the Root Kernel multi-profile fleet. A carry is removed when a
later upstream release provides an exact, behaviorally verified replacement.

This guide describes the **current user-visible behavior** of Root Kernel Hermes Agent
v0.19.1 and the settings required to use it. It is not the release history or the
machine-readable carry registry.

## Documentation map

| Document | Audience | Purpose |
|---|---|---|
| `root-kernel/feature.md` | Users and operators | Current differences from upstream, configuration, and usage recipes |
| `root-kernel/ledger.md` | Maintainers and release operators | Version-scoped decisions, verification, activation, and rollback history |
| `root-kernel/carry.yaml` | Automation and maintainers | Structured carry state, lineage, evidence, and retirement rules |

## Current baseline

- Root Kernel release: `rk/tag/v0.19.1`
- Upstream base: `v2026.7.30`
- Hermes package version: `0.19.1`
- Active carries: D1 through D7

Verify the installed runtime before diagnosing behavior:

```bash
hermes --version
hermes gateway status
```

The expected version line is `Hermes Agent v0.19.1 (2026.7.30)`. A checkout on
`rk/v0.19.1` does not by itself prove that the launcher or gateway service uses that
checkout; use the runtime commands above.

## Differences from upstream at a glance

| Carry | Root Kernel behavior | Operator action |
|---|---|---|
| D1 | CJK-aware offline session recovery | Automatic; no new setting |
| D2 | Skill write approval fails closed when its approval boundary is unavailable | Enable upstream `skills.write_approval` if desired |
| D3 | A profile can pin one exact OpenAI Codex credential by ID or label | Configure the pin in that profile's `.env` |
| D4 | Discord thread ownership, role-mention fail-close, and optional free-response auto-threading | Configure Discord routing explicitly |
| D5 | Same-card Kanban review/result workflows, mutex serialization, and closed workflow banners | Select Kanban flags per card |
| D6 | CLI propagates only exact nonzero integer return codes; booleans remain success | Automatic; no new setting |
| D7 | `hermes doctor` hides unavailable-tool warnings outside the configured runtime scope | Automatic; no new setting |

## D1: CJK-aware offline session recovery

Root Kernel loads the existing CJK tokenizer on the destination and verification
connections used by `hermes sessions recover`. Korean, Japanese, and Chinese messages
therefore survive offline recovery and remain searchable.

No Root Kernel-specific setting is required. Use the upstream recovery command normally,
providing a source and a separate output path:

```bash
hermes sessions recover \
  --source /path/to/damaged-state.db \
  --output /path/to/recovered-state.db
```

The carry changes the recovery boundary only. It does not change the configured tokenizer,
normal session writes, or the source database.

## D2: fail-closed skill write approval

Upstream supports staging every agent-authored skill mutation for explicit review. Root
Kernel keeps that interface but refuses the write if the approval module cannot be imported
or evaluated; it never silently falls back to allowing the mutation.

Enable the existing gate:

```bash
hermes config set skills.write_approval true
```

Review staged writes with:

```text
/skills pending
/skills diff <id>
/skills approve <id>
/skills reject <id>
```

The default remains `false`. D2 changes failure behavior, not the default or the review
commands.

## D3: OpenAI Codex credential pinning

A Root Kernel profile can select one exact entry from a shared `openai-codex` credential
pool. The pin fails closed when the selected entry is missing, duplicated by label,
unavailable, dead, exhausted, or has no runtime credential. Hermes does not substitute a
sibling pool entry when a configured pin cannot be honored.

List the pool before choosing a stable ID or unique label:

```bash
hermes auth list openai-codex
```

Set one of the following in the active profile's `.env`:

```dotenv
# Exact ID takes precedence when both are present.
HERMES_CREDENTIAL_PIN_OPENAI_CODEX_ID=<credential-id>

# Alternatively, pin a unique label.
HERMES_CREDENTIAL_PIN_OPENAI_CODEX_LABEL=<credential-label>
```

The compatibility alias `HERMES_CREDENTIAL_PIN_OPENAI_CODEX=<credential-label>` is also
accepted, but the explicit `_LABEL` form is preferred. Pins are profile-local even when the
credential pool itself is shared.

Add or reauthenticate a labelled Codex credential with the existing auth surface:

```bash
hermes auth add openai-codex --label work-codex
```

Credential values remain secrets. Do not place them in `config.yaml` or commit profile
`.env` files.

## D4: Discord routing and thread ownership

### The important upstream/downstream difference

Upstream `discord.free_response_channels` means "respond without an `@mention`" and, by
default, replies inline in the parent channel. Root Kernel adds
`discord.auto_thread_free_response`: when enabled, a mention-free request in a free-response
channel creates a thread, marks that thread as owned by the responding Hermes profile, and
routes the answer into it.

The Root Kernel extension defaults to `false` so merely adding a free-response channel does
not silently change upstream routing behavior.

### Recommended single-agent intake channel

Use exact channel IDs. With the CLI, pass a plain ID rather than JSON-list syntax:

```bash
hermes config set discord.require_mention true
hermes config set discord.free_response_channels 123456789012345678
hermes config set discord.auto_thread true
hermes config set discord.auto_thread_free_response true
hermes config set discord.thread_require_mention false
hermes gateway restart
```

`auto_thread_free_response` is a downstream Discord-extra key. The v0.19.1 config CLI accepts
Discord extras, and the adapter reads and bridges the key normally even though it is not an
upstream Discord option.

Equivalent configuration shape:

```yaml
discord:
  require_mention: true
  free_response_channels: "<channel-id>"
  auto_thread: true
  auto_thread_free_response: true
  thread_require_mention: false
```

Do not pass a JSON-looking value such as `["1234567890"]` to `hermes config set`; that CLI
stores it as one literal string in v0.19.1, brackets and quotes included, so it will not
match the actual channel ID. For multiple channels, use a comma-separated string or a real
YAML list.

### Routing matrix

| Context | Mention required | New thread | Response location |
|---|---:|---:|---|
| Ordinary server channel | Yes | On explicit mention when `auto_thread` is true | New thread |
| Free-response channel, downstream option off | No | No | Parent channel |
| Free-response channel, `auto_thread_free_response: true` | No | Yes | New owned thread |
| Channel listed in `no_thread_channels` | Depends on mention policy | No | Parent channel |
| Existing thread owned by this Hermes profile | No when `thread_require_mention: false` | No | Existing thread |
| Existing thread owned by another profile | Explicit routing required | No | No ambient response |
| Discord DM | No | No | DM |

### Ownership and fail-close behavior

- Auto-created, `/thread`-created, and forum text/media threads record a persistent owner.
- Participation alone does not grant mention-free default-responder authority.
- Ownership survives gateway restarts and is used by recovered-message admission.
- A role mention that does not explicitly mention this bot fails closed, even in a
  free-response channel.
- If configured auto-thread creation fails, Hermes reports the failure and does not silently
  dump the agent response into the shared parent channel.

After changing Discord routing, always restart the gateway and verify reconnection:

```bash
hermes gateway restart
hermes gateway status
```

Messages received before the corrected restart are not replayed unless
`discord.missed_message_backfill.enabled` was already enabled.

## D5: same-card Kanban workflows

Root Kernel extends upstream Kanban with an enforced same-card implementation, review,
rework, and final-acceptance lifecycle. It also adds board-local mutex serialization and a
closed set of code-owned workflow banners rendered into worker context.

### Per-card creation controls

```bash
hermes kanban create "Implement feature" \
  --assignee worker \
  --mutex-key repo:feature \
  --workflow-type creator_accepted_work
```

`--mutex-key` serializes running tasks with the same exact board-local key. Values are
trimmed, but case and schemes remain distinct.

Supported `--workflow-type` values:

- `creator_accepted_work`
- `creator_adjudicated_review`
- `parallel_color_review`
- `round_based_color_consensus`
- `fanout_fanin`
- `serial_dependency_chain`
- `single_card_baton`

These values select static, code-owned operating instructions. They are separate from
upstream future-v2 `workflow_template_id` and `current_step_key` routing metadata.

### Same-card lifecycle

- `kanban_reassign` performs a cooperative baton pass without creating a duplicate card.
- `kanban_submit_review` routes implementation to a distinct reviewer.
- `kanban_request_changes` returns rejected work to the exact implementation worker/run.
- `kanban_submit_result` routes finished work to the creator or designated acceptor.
- Only the creator or acceptor performs final completion when the selected workflow requires
  that authority.
- Declared scratch artifacts remain in flight until successful final acceptance.

Use `hermes kanban <subcommand> --help` for the exact terminal surface. Agent workers receive
the matching Kanban tools automatically.

## D6: bool-safe CLI return codes

Root Kernel preserves upstream nonzero integer exit-code propagation but excludes Python
booleans, which are integer subclasses. Exact nonzero `int` values remain process exit
codes; `True`, `False`, `None`, and strings do not accidentally report command failure.

No setting is required. This matters to shell scripts, CI, and launchd/systemd wrappers.

## D7: runtime-scoped doctor warnings

`hermes doctor` resolves the effective CLI and explicitly configured platform toolsets, then
hides only unavailable-tool warnings proven outside that scope. Unknown or malformed tool
metadata fails open and remains visible. Healthy rows and all non-tool diagnostics remain
unchanged.

No setting is required:

```bash
hermes doctor
```

A warning for an enabled Discord, web, browser-CDP, Kanban, Honcho, or other configured
surface remains visible. Optional platforms that were never enabled no longer create noise.

## Distribution behavior versus fleet policy

D1 through D7 are code carries in the Root Kernel distribution. The post-live R1 through R5
records in the release ledger also include deployment policy for the specific Root Kernel
fleet, such as profile identity repair, exact skill seeding, Dashboard retirement, cron and
launchd audits, and local asset cleanup. Those fleet mutations are **not automatic defaults**
for every clone of the distribution.

For example, the Root Kernel fleet intentionally disabled Dashboard services and removed its
active frontend build, but the source-level `hermes dashboard` command still exists in the
distribution.

## Upgrade and retirement policy

Before moving Root Kernel to a newer upstream release:

1. Read the active entries in `root-kernel/carry.yaml`.
2. Reproduce each carry's behavior against the exact new upstream target.
3. Retire a carry only when an exact upstream replacement satisfies its recorded retirement
   rule and equivalent regression coverage passes.
4. Record investigation, verification, activation, and rollback facts in
   `root-kernel/ledger.md`.
5. Update this guide when an active user-visible behavior, default, setting, command, or
   recommended recipe changes.

Do not infer that a matching symbol, nearby upstream change, or closed issue replaces a
carry. Behavioral verification is the retirement authority.
