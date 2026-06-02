---
title: "Vault Improvement Plan"
type: project
status: active
created: 2026-04-25
tags: [vault, infrastructure, meta]
---

# Vault Improvement Plan

> Goal: zero orphans, maximum context density, minimal prompting needed for Claude to understand any project.

---

## Problem

1. **23 orphaned notes** in 030-Projects not linked from 000-Index
2. **10 truly orphaned notes** with zero backlinks from anywhere
3. **Sidepocket notes are fragmented** — status snapshots (Apr 2), slack digests, Q1 summary, monday queue are all one-off documents with no parent linking them
4. **FetEnhNet notes are fragmented** — 15+ notes scattered without a clear hub that links them all
5. **BCH meeting minutes** are individual files instead of a threaded log
6. **No project-level CLAUDE.md** context files — every session re-discovers the same project structure
7. **000-Index.md is stale** — doesn't reflect notes created since March 30
8. **Duplicate content** — `github-repos.md` exists in both 030-Projects and 070-Accounts
9. **Missing indexes** — 050-Knowledge has no `knowledge-index.md`, 010-System has no `packages-aur.md` link from index

---

## Plan

### Phase 1: Hub Notes (link orphans)

Create or update hub notes that gather related orphans under one roof.

**Sidepocket Hub** — update `sidepocket-engineering.md` to link:
- `sidepocket-status-2026-04-02.md` (archive or fold in)
- `sidepocket-q1-2026-summary.md`
- `sidepocket-monday-queue.md`
- `ascend-migration-plan.md`
- `ascend-migration-mapping.md`
- `sidepocket-team.md`
- `slack-digest-2026-03-30.md` / `slack-digest-2026-04-01.md` (archive)

**FetEnhNet Hub** — update `fetenh-net.md` to link ALL sub-notes:
- `BCH-FetEnhNet.md` (merge into fetenh-net.md or archive)
- `FetEnhNet-Run20-Plan.md`, `FetEnhNet-Run21-Plan.md`
- `fetenh-data-inventory.md`, `fetenh-data-methodology.md`, `fetenh-data-knowledge-graph.md`
- `fetenh-option-c-dataset.md`
- `fetenh-manual-registration-guide.md`
- `fetenh-overfitting-analysis.md`

**BCH Meetings** — make `BCH-Meeting-Minutes.md` the hub with links to individual meetings:
- `BCH-Meeting-2026-03-24.md`
- `BCH-Meeting-2026-03-31.md`
- `BCH-Meeting-2026-04-07.md`
- `BCH-Meeting-2026-04-14.md`

### Phase 2: Update 000-Index.md

- Add all new Sidepocket notes (monday queue, Ascend mapping, Q1 summary)
- Add all FetEnhNet sub-notes under the BCH section
- Add missing links: `sidepocket-team`, `github-repos`, `local-project-file-structures`
- Remove or fix broken wikilinks
- Add "Ephemeral / Time-stamped" section for status snapshots and digests

### Phase 3: Deduplicate

- `github-repos.md` exists in both 030-Projects and 070-Accounts — merge into 070-Accounts, redirect from 030
- `BCH-FetEnhNet.md` overlaps with `fetenh-net.md` — merge, archive the older one

### Phase 4: Archive stale notes

Move to `099-Archive/`:
- `slack-digest-2026-03-30.md` / `slack-digest-2026-04-01.md` — point-in-time, info now in memory
- `sidepocket-status-2026-04-02.md` — superseded by current engineering notes
- `BCH-Email-2026-03-24.md` — sent, done
- `puentes-application-2026.md` — if application submitted

### Phase 5: Context density for Claude

Create lightweight `_context.md` files in each project root that Claude can load in one read:

**`030-Projects/_sidepocket-context.md`** — single file with:
- Current status (what's merged, what's in review, what's blocked)
- Architecture one-liner (8 microservices, Flask, ECS, Redis→S3)
- Key people (Max, Yves, Tomasz, Chema + what they own)
- Active tickets and their status
- Link to detailed notes

**`030-Projects/_fetenh-context.md`** — single file with:
- Current training status (which run, what metrics)
- Pipeline status (inverse alignment solved, data pipeline in progress)
- Server paths
- Kiho's requirements
- Link to detailed notes

These replace having to read 5-10 notes to understand a project. One read, full context.

### Phase 6: Memory ↔ Vault alignment

Audit Claude memory files against vault notes. Memory should point to vault for details, not duplicate them:
- `sidepocket_current_priorities.md` → should reference `sidepocket-monday-queue.md`
- `bch_fetenh_net.md` → should reference `fetenh-net.md`
- Remove memory entries that are just stale vault snapshots

---

## Execution Order

1. Phase 1 (hub notes) — fixes orphans, ~15 min
2. Phase 2 (index update) — fixes navigation, ~10 min
3. Phase 5 (context files) — biggest impact for daily use, ~20 min
4. Phase 3+4 (dedup + archive) — cleanup, ~10 min
5. Phase 6 (memory alignment) — maintenance, ~10 min

---

## Success Criteria

- `find 030-Projects -name "*.md" | while read f; do grep -rl "$(basename ${f%.md})" --include="*.md" | grep -v "$f" | wc -l; done` → zero orphans
- Every note reachable from 000-Index.md in ≤2 clicks
- Claude can load full project context with one `Read` call per project
- No duplicate content across vault + memory
