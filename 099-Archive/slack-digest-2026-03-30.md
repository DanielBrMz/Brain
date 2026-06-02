---
title: "Slack Digest — 2026-03-30"
type: note
created: 2026-03-30
updated: 2026-03-30
tags: [slack, digest, sidepocket, sprint, team]
---

# Slack Digest — 2026-03-30

> Latest channel updates as of 2026-03-30. Channels read: #team-sprintreview, #team-frontend, #team-sidepocket, #team-devops, #backend.

---

## Sprint Close — 2026-03-28 (#team-sprintreview)

Maxwell closed the sprint on 2026-03-27. Updates posted:

### Daniel (me)
**Completed:**
- Reviewed and merged Chema's auth PRs — WebAuthn credential model + migration, WebAuthn deps, AESGCM challenge encryption (PRs #182, #183, #184)
- S3 data layer + InMemoryStore fully tested and stable
- Redis → S3 migration script complete — all 2,837 keys migrated, zero failures
- Alembic upgrade head automation in Dockerfile entrypoint done

**Blocked:**
- [[sidepocket-engineering#TECH-3826|TECH-3826]] stack upgrade PRs ready to merge but waiting on deploy pipeline / ECS task setup from Yves

**Next sprint:**
- Merge TECH-3826 once deploy pipeline is ready
- Continue TECH-3804 (remaining migration tickets)

---

### Sam
- Working on TECH-3819 (account flows) + TECH-3818 (categories/budget tracking)
- ~60% done; needed to re-architect when initial plan proved insufficient
- Expected completion: mid-week (≈2026-04-01)
- Next: TECH-3820 (account sync daemon update)

---

### Joab (Security)
- **Completed SEC-811** — Sidepocket Level 1 DFD + system documentation, STRIDE mitigation mapping, OSCAL integration
  - Subtasks SEC-812, SEC-813, SEC-814 all done
  - Published to GitHub org — now the security baseline for SDLC
- Other sprint tickets pushed due to SEC-811 complexity

---

## #team-devops — 2026-03-24
- Travis shared: [Manifest Repository Pattern for Security Compliance](https://docs.google.com/document/d/1JoopzVRPSFX4yRWynHVk8ZNFMv4Byk5gDDIkITKr34A/edit) — worth reading for DevOps context

## #team-frontend — 2026-03-29
- Travis shared: [Decompiling the White House App](https://blog.thereallo.dev/blog/decompiling-the-white-house-app) — just for fun

## #team-sidepocket — 2026-03-24
- Christina OOO Thursday (traveling back to California)

---

## #backend — 2026-03-28 → 2026-03-30 (active thread)

### Yves: DateTime schema audit 🚨
Yves ran a quick audit of all DB models and found a widespread bad practice:

> **`default=datetime.now()` used in many models instead of `server_default=func.now()`**

- `default=datetime.now()` captures the **server/daemon startup time** — not the actual insertion time. A service that hasn't restarted in months is inserting wrong dates on every row.
- Correct approach: `server_default=func.now()` — lets the DB generate the timestamp at insert.
- A majority correctly use `func.now()` but as `default=` not `server_default=`.

**Yves also flagged:** Chema's **WebAuthn `created_at`** column has this same bug — wrong date will be set.

**Max:** "Good catch Yves" → pinged Daniel to ticket it for next sprint.
**Daniel (2026-03-30 12:22):** "Yep, on it" — ticketed as TECH-3879 (done).

---

## Current Sprint — "April 3 2026" (Sprint 524)

- **Started:** 2026-03-30
- **Ends:** 2026-04-10

---

## My Work Queue — Sprint "April 3 2026"

| Priority | Ticket | Description | Status |
|----------|--------|-------------|--------|
| 1 | [TECH-3879](https://sidepocket.atlassian.net/browse/TECH-3879) | Fix SQLAlchemy DateTime defaults across all models | In Progress |
| 2 | TECH-3826 | Stack upgrade PRs — merge once ECS deploy pipeline ready | Blocked on Yves |
| 3 | TECH-3804 | Remaining migration tickets | Up next after 3826 |

**Blocker on 3826:** Ping Yves mid-week if no update on ECS deploy pipeline.
