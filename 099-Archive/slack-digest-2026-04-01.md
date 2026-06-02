---
title: "Slack Digest — 2026-04-01"
type: note
created: 2026-04-01
updated: 2026-04-01
tags: [slack, digest, sidepocket, sprint, team, backend, qa]
---

# Slack Digest — 2026-04-01

> Latest channel updates as of 2026-04-01. Channels read: #backend, #quality-assurance.

---

## #backend — 2026-03-31 (latest thread)

### Arch Migration General Update (Max → Daniel)

Max asked for a general arch migration update for team visibility (11:59 EDT). Daniel posted a full summary at 21:30 EDT:

**Stack Upgrade: Python 3.14 / Flask 3.1 / SQLAlchemy 2.0 (TECH-3826)**
- All PRs across 6 backend services reviewed and ready to merge
- Blocker: ECS task / deploy pipeline setup (Tomasz/Yves) — waiting on infra

**SQLAlchemy DateTime Defaults (TECH-3879)**
- Complete. Fixed `server_default=func.now()` across all 6 services
- PRs open, ready to merge alongside TECH-3826
- Alembic migrations staged on each EC2

**S3 Migration (TECH-3804 / TECH-3846)**
- Redis → S3 Parquet migration script written and ready to run from cache EC2 (IAM role in place)
- Still blocked on TECH-3843 infra files and deploy pipeline
- Once unblocked: immediate next step

---

### Max's Open Question to Daniel (22:38 EDT)

> "Is there anything you can make progress on at this point besides fixing the cash merge conflict?"

**Responded via self-DM draft** — see action items below.

---

### Max → Tomasz (22:37 EDT) — ⚠️ PENDING

> "Is there any update on the deploy framework for the new service?"

No response from Tomasz yet as of digest time.

---

## #quality-assurance — 2026-03-31 (latest thread)

### Traditional IRA / Create Direct Brokerage Application Bug — RESOLVED ✅

**Reported by Oleh (12:12 EDT):**
- `Create Direct Brokerage Application` endpoint returning `invalid apex form type for Traditional IRA: direct_new_account_form` error on DEV

**Fix:** Normalized `account_sub_type` enum to string value before APEX form type lookup (`schema/mutation.py`)

**PR #162** — `hotfix/TECH-3883-traditional-ira-apex-form` → `main` on `accounts`
- Cherry-picked single commit onto clean branch from `main`
- Max to review and merge

---

## Work Done — 2026-04-01

### TECH-3883: Traditional IRA hotfix PR opened ✅
- Closed the broad develop→main PR (#161) that was opened by mistake
- Created `hotfix/TECH-3883-traditional-ira-apex-form` branch cherry-picked from develop
- Opened PR #162 → `main` on `accounts` — waiting on Max to merge

### TECH-3879: Cash merge conflict resolved ✅
- **Root cause:** All 6 TECH-3879 PRs were opened targeting `main` instead of `develop` (our mistake, Max merged 5 of them at 01:48–01:49 EDT)
- **Conflict:** `models/cash_transfer_model.py` — `main` had added `Index('ix_cash_transfer_account_number', 'account_number')` that the branch didn't know about
- **Resolution:** Kept both the `Index` from `main` and `server_default=func.now()` from TECH-3879
- Rebased on dev-ubuntu, force-pushed as `DanielBrMz`
- PR #258 on `cash` is now `MERGEABLE` — waiting on Max to review/merge

---

## My Action Items — 2026-04-01

| Priority | Action | Status |
|----------|--------|--------|
| ✅ 1 | Open PR from dev → prod (Traditional IRA fix) — PR #162 | Done |
| ✅ 2 | Fix cash TECH-3879 merge conflict — PR #258 now mergeable | Done |
| 🟡 3 | Reply to Max: "what else can you make progress on?" | Draft in self-DMs |
| 🟢 4 | Monitor for Tomasz's deploy framework update (ECS / new service) | Watching |

---

## Current Sprint Blockers

| Ticket | Blocker | Owner |
|--------|---------|-------|
| TECH-3826 | ECS deploy pipeline not set up | Tomasz / Yves |
| TECH-3843 | Infra files missing | Yves |
| TECH-3804 | Blocked on TECH-3826 + TECH-3843 | — |
