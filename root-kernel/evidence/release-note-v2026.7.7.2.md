# Hermes Agent v0.18.2 (2026.7.7.2)

- Source: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2
- Tag: `v2026.7.7.2`
- Published: `2026-07-08T03:11:22Z`
- Target commitish: `main`
- Captured for: Root Kernel Hermes Agent `rk/v0.18.2` scaffold
- Captured at: `2026-07-09T16:05:24+09:00`

---

# Hermes Agent v0.18.2 (v2026.7.7.2)

**Release Date:** July 7, 2026

> Same-day patch on top of v0.18.1, picking up the WhatsApp Baileys dependency fix needed for tagged-release Docker builds.

---

## What's in this patch

- **fix(whatsapp): unpin Baileys from git commit, use published 7.0.0-rc13** ([#60643](https://github.com/NousResearch/hermes-agent/pull/60643)) — the WhatsApp bridge dependency now installs from the published npm release instead of a pinned git commit, making installs and Docker image builds reliable.

Full curated release notes for the entire post-v0.18.0 window ship with v0.19.0.

## Updating

```bash
hermes update        # existing installs
pip install -U hermes-agent
```

**Full Changelog**: [v2026.7.7...v2026.7.7.2](https://github.com/NousResearch/hermes-agent/compare/v2026.7.7...v2026.7.7.2)

