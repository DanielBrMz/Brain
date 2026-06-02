---
title: "Claude Code — Project Home"
type: reference
created: 2026-03-19
updated: 2026-03-20
tags: [claude, ai, project, meta]
---

# Claude Code — Project Home

> This folder is the bridge between Claude Code (the AI assistant) and this Brain vault.
> Claude reads `~/CLAUDE.md` on every session and references these notes for context.

## What Claude Knows

Claude Code maintains two types of persistent context:

| Source | Path | Purpose |
|--------|------|---------|
| Project instructions | `~/CLAUDE.md` | Role, system state, project commands — loaded every session |
| Memory (user) | [[user-profile\|_Claude/user-profile]] | Who you are, your stack, preferences |
| Memory (system) | [[system-state\|_Claude/system-state]] | Machine state, maintenance history, deferred items |

## How This Vault Fits In

```
Session startup flow:
  CLAUDE.md → "open ~/Brain/000-Index.md first"
       ↓
  Brain/000-Index.md → navigate to relevant notes
       ↓
  Work on projects / system / life notes
```

Claude updates memory files here after significant changes. The vault is the source of
truth — these notes should be kept more current than any other documentation.

## Claude Memory Files

Raw memory files (auto-managed by Claude) also live at:
```
/root/.claude/projects/-home-brmz/memory/
├── MEMORY.md           ← index (references vault paths)
├── user_profile.md     ← synced from _Claude/user-profile.md
└── project_system_state.md ← synced from _Claude/system-state.md
```

## Obsidian CLI

The `obsidian` CLI (run as `brmz`) lets Claude interact with this vault directly:

```bash
sudo -u brmz obsidian read file="000-Index"
sudo -u brmz obsidian search query="TODO"
sudo -u brmz obsidian append file="maintenance-log" content="- Fixed X"
sudo -u brmz obsidian property:set name="updated" value="2026-03-20" file="arch-overview"
```

## Related

- [[../000-Index|Master Index]]
- [[user-profile|User Profile]]
- [[system-state|System State]]
