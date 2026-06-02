# Sidepocket Status — 2026-04-02

## Incident: TECH-3879 cash_balance NOT NULL (NOT RESOLVED)

### What happened
- PR #258 (`cash` repo) replaced `default=func.now()` → `server_default=func.now()` on DateTime columns
- Merged **directly to main** (no UAT, no develop first) — Maxwell pushed it thinking it was good
- `server_default` requires an Alembic migration to set `DEFAULT now()` at the DB schema level — that migration was never run
- Sentry fired 3 alerts at 4:11pm Apr 1, `cash-prod-5.96`, 54 events each, escalating
- **Yves called for rollback at 7:22pm** → Max confirmed rollback ("Done") at ~7:57pm
- Cash-prod was rolled back to previous state

### Current state of TECH-3879
- Fix is on `develop` but **NOT in prod** (rolled back)
- Two options discussed in #backend:
  1. Write Alembic migrations for all affected tables → proper fix
  2. Revert to `default=func.now()` (ORM-level, not `datetime.now()`) as interim
- Max: "Alembic on prod is a project" — suggests resistance to option 1 short-term
- **TECH-3879 still "In Progress" in Jira — needs resolution plan**

### Cypress/E2E gap flagged
- Yves in #alert-sentry: `process_new_account_cash_balance()` not covered by prod Cypress tests
- Tagged Oleh Zakhariak — no resolution yet

---

## Active EPICs (assigned to Daniel)

| Key | Summary | Priority | Status |
|-----|---------|----------|--------|
| TECH-3800 | Redis → DynamoDB + proper cache | High | In Progress |
| TECH-3152 | Ascend migration (Apex → Apex Ascend) | Medium | Backlog → HOT |

---

## Ascend Migration (TECH-3152) — Becoming Urgent

Maxwell briefed Daniel via DM (Apr 1 midnight):
- Migrating Apex connections off legacy platform onto **Apex Ascend**
- **All elements must go in at once** — partial deploy shuts everything down
- Flow: QA on `dev` → copy to new branch → remove from `dev`
- Max posted TECH-3152 in #backend Apr 1 2:53pm: *"I think while we wait, it would be a good idea for you to break ground on the Apex Ascend migration"*
- **Talk to Max today about scope/timeline**

---

## Open Items for Daniel

### Immediate (today)
1. **Talk to Max** — he said "Talk tomorrow" (= today Apr 2). Align on Ascend scope/timeline. Draft reply saved to self DM.
2. ~~**Reply to #backend EOD thread**~~ — ✅ Done (Apr 2)
3. **TECH-3879 resolution plan** — decide: Alembic migrations or revert to `default=func.now()`. Need to align with Yves/Max before touching prod again.

### This sprint
4. **Ascend migration (TECH-3152)** — break ground per Max's request
5. **Auth PR #188** — Chema flagged it didn't merge ("creo que no se mergeo el ticket 3")
6. **Redis → DynamoDB (TECH-3800)** — blocked on Tomasz (deploy pipeline/ECS task setup). Follow up.
7. **Type annotations** — Yves asked all BE devs to start annotating new code going forward

### Compliance meeting
- **Tomorrow Apr 3 (Good Friday — market closed)** — Max specifically said "really need you there"

---

## Team Notes
- **Yves Perrenoud** — auditing backend code quality, pushing type hints, flagged the UAT process gap. Key technical authority.
- **Tomasz Pado** — blocking on ECS/deploy pipeline for TECH-3826 stack upgrade. Still waiting.
- **Chema (José María Soto)** — working on ticket 7 (auth/WebAuthn), addressing Yves + Travis review on PR
- **Oleh Zakhariak** — owns Cypress/E2E tests, tagged on coverage gap

---

## Process Issues Flagged
- Code merged to `main` without UAT validation → caused prod incident
- No EOD updates from Daniel or Chema → Max called it out
- E2E gap: `process_new_account_cash_balance()` not covered

---

---

## UAT DB — TECH-3879 Defaults Applied (2026-04-02 evening) ✅

All `server_default` DateTime columns now have `DEFAULT now()` at DB schema level on UAT:

| Service | DB | Alembic stamp |
|---|---|---|
| auth | sp_user | `tech3879_fix_datetime_server_defaults` |
| app-backend | sp_user | `e2f3a4b5c6d7` |
| cash | cash | `d1e2f3a4b5c6` (c3d4e5f6a7b8 pre-existing) |

DB defaults applied directly via psql. **Alembic migration files are gitignored** (`/alembic/versions/*.py`) — they live only on the EC2 servers, never committed to the repo. Ready to deploy prod (order: events → portfolio → accounts → auth → app-backend → cash).

---

## PR #190 — Auth WebAuthn Config (Chema) ✅ Tested

Adds `WEBAUTHN_CHALLENGE_KEY` fail-fast + env overrides for RP_ID/RP_NAME/ORIGIN.

- **Tested on dev-ubuntu:** auth starts cleanly with key present
- **Blocker for prod:** `WEBAUTHN_CHALLENGE_KEY` must be added to AWS Parameter Store before merging to prod
- Generated UAT key (in dev-ubuntu `.env`): `d512d05978d425dc6bc16655ed350f8ed60c6b7d527ecb12252812f30153da02`
- PR status: MERGEABLE, CLEAN

---

## Oleh's Bug — `'NoneType' object has no attribute 'isoformat'`

- Endpoint: `GET /accountApplication/consolidatedList` (accounts service)
- File: `accounts/accounts_util/util.py:12`
- Cause: `app.last_updated.isoformat()` crashes when `last_updated` is None
- Model uses `server_default` + `onupdate` — ORM doesn't eagerly set it in memory
- UAT DB has 0 NULLs but other envs or recently-inserted (pre-flush) records can have None
- **Fix:** `app.last_updated.isoformat() if app.last_updated else None`

---

## S3 Migration Status (TECH-3804)
- Script written, ready to run from cache EC2 (IAM role set, bucket `backend-cache-dev` created by Yves)
- Still blocked on infra files (TECH-3843) and deploy pipeline (Tomasz)
- Yves created `backend-cache-dev` and `backend-cache-prod` buckets Apr 1
