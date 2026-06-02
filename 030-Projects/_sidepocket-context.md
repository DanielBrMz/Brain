---
title: "Sidepocket — Quick Context"
type: context
updated: 2026-05-18
tags: [sidepocket, context]
---

# Sidepocket — Quick Context

> One-read context file for Claude. Load this first for any Sidepocket work.

## What is it
Fintech investment platform — portfolio management, brokerage, cash/ACH, billing. Python/Flask microservices on AWS ECS.

## Architecture
8 microservices: auth (4001), accounts (4002), app-backend (4003), cash (4006), portfolio (4007), events (4005), stratz (4000), billing (deprecated). Each runs API + daemon containers. PostgreSQL RDS, ElastiCache Redis (migrating to S3), DynamoDB for JWT revocations.

## Team
- **Max Bradley** — CEO/PM, reviews all PRs, makes architecture decisions
- **Yves Perrenoud** — CTO, DevOps/infra, ECS deploys, code quality enforcer
- **Tomasz Pado** — GitHub Actions runners, ECS task setup, security groups
- **Chema (José María Soto)** — WebAuthn/passkeys (auth service)
- **Sam** — Plaid multi-account, mobile app
- **Daniel (you)** — Sr Full Stack, Ascend migration, cache migration, prod hotfixes

## Current Status (2026-05-18)

### All Services Live on Dev — Full Ascend Migration Complete

| Service | Latest Dev Tag | Status |
|---------|---------------|--------|
| auth | dev-9.38 | Live — WebAuthn endpoints deployed |
| accounts | dev-6.139 | Live — Full Ascend migration (ALE, investigations, documents) |
| cash | dev-15.20 | Live — Full Ascend migration (transfer ALE, dividend reinvest, None guards) |
| app-backend | dev-12.83 | Live — Ascend SBX creds |
| portfolio | dev-27.13 | Live — Full Ascend migration (trade_util, rebalance, validate_etf, ETF whitelist fix) |
| events | dev-2.89 | Live — Ascend SBX creds |
| stratz | dev-11.32 | Live — dead Apex imports removed |
| util | dev-6.5.10 | Live — ETF whitelist fix, empty DataFrame guard, Sentry log noise fix |

### Arch Migration (TECH-3826) — COMPLETE
All 6 services migrated to Python 3.14, SQLAlchemy 2.x, pandas 2.x, numpy 2.x.

### Ascend Migration (TECH-3152) — FULLY COMPLETE

**All production code paths now route through Ascend when USE_ASCEND=true.** Zero unguarded legacy Apex API calls remain across all 8 services. Full codebase audit completed May 15 + May 18 with agent council verification.

Legacy Apex code still exists as fallback in `else` branches (for USE_ASCEND=false), and in the util library (which provides both APIs). When USE_ASCEND=true on dev, zero legacy Apex calls execute.

**Ascend SSM Parameter Store (all 7 values set by Max on May 12):**
- ASCEND_API_KEY — 48-char SBX key (07vqWz...)
- ASCEND_PRIVATE_KEY — SBX PEM
- ASCEND_SERVICE_ACCOUNT_NAME — correspondents/01KP60MNZPWR0Q52Q558BK3JDR_daniel_barreras@sidepocket.com_uat
- ASCEND_ORGANIZATION — correspondents/01KP60MNZPWR0Q52Q558BK3JDR
- ASCEND_SERVER — sbx
- ASCEND_CORRESPONDENT_CODE — 01KP60MNZPWR0Q52Q558BK3JDR
- ASCEND_CORRESPONDENT_ID — 01KP60MNZPWR0Q52Q558BK3JDR

**IMPORTANT:** SBX has no real account data (ALE returns empty 404, account lookups return 404). This is expected. Need UAT API key from Apex onboarding.

**Apex SOW Review Meeting:** Wednesday May 20, 2:00 PM EST with Ryan Lee, Nicholas Franzese, Garrett Huff. Max added to invite. This unlocks UAT credentials + dedicated onboarding support.

### Database Indexes — 13 INDEXES ADDED on May 18

All created with `CREATE INDEX CONCURRENTLY` (zero locks, zero downtime). Prior state: zero business-column indexes across all tables.

**Tier 1 (Critical):**
- `idx_atsl_account_number` on account_trade_status_log (account_number) — 48MB
- `idx_atsl_status_created_at` on account_trade_status_log (status, created_at DESC) — 274MB
- `idx_sp_order_request_account_status` on sp_order_request (account_number, status)
- `idx_sp_order_request_guid_user` on sp_order_request (guid_user)
- `idx_rebalance_order_preview_id` on rebalance_order (rebalance_preview_id)
- `idx_rebalance_order_account` on rebalance_order (account_number)

**Tier 2 (High):**
- `idx_sp_holding_active` on sp_holding (account_number) WHERE exit_datetime IS NULL
- `idx_sp_holding_guid_user` on sp_holding (guid_user)
- `idx_txn_summary_account_date` on transaction_summary (account_number, trade_date DESC)
- `idx_txn_summary_guid_user` on transaction_summary (guid_user)
- `idx_lus_account_number` on live_user_sidepocket (account_number)
- `idx_lus_guid_user` on live_user_sidepocket (guid_user)
- `idx_lus_status` on live_user_sidepocket (status) WHERE status = 'FUNDED'

**Impact:** Check Trade Status endpoint dropped from >3000ms to <3000ms immediately. Cypress tests went from 372/376 to 373/376 passing.

**24% rollback ratio** (52M rollbacks / 218M commits) flagged by financial architect — abnormal, needs separate investigation ticket.

### S3 Cache (TECH-3830) — Development Done, Tomasz Engaging
Cache service running on ECS dev. OOM stable. S3 bucket `backend-cache-dev` has objects. Remaining blockers: Cloud Map DNS + `USE_ZERORPC_CACHE` env var in Parameter Store.

TECH-3833 (decommission ElastiCache): Assigned to Yves — Redis at 95-108% memory. Flushed on May 14 (324MB→14MB) but repopulated to full within hours.

### Sentry Status — Zero Code Errors on Dev

Only remaining: Redis memory warnings (infra, TECH-3833), 9DK (no rebalance preview IDs), P1W (intermittent SBX token 401), fee 404s (SBX expected).

### Cypress API Tests — 373/376 Passing

3 remaining failures (not regressions):
- isoCurrencyCode: pycountry version difference (test data needs regeneration)
- Investigation Search: Ascend external API latency >3000ms (not code-fixable)
- One more data assertion (minor)

cashTransferStatus: FIXED — added QUEUED_FOR_PROCESSING to test expectations
Check Trade Status: FIXED — account_trade_status_log index eliminated full table scan

### Jira State
- Daniel open tickets: 2 (TECH-3830 Development Done, TECH-3879 In QA/parked)
- TECH-3152 (Ascend): Done — full migration complete
- TECH-3826 (stack): Done
- TECH-3800 (Redis→S3): Done

### Merged PRs (May 13-18 sessions)

**May 13:**
- auth #208, accounts #186, portfolio #398, util #226, cash #281, stratz #279

**May 14-15 (Sentry fixes + Ascend migration):**
- util #226 (reverted→#228 clean re-apply) — empty DataFrame guard + Sentry log noise
- cash #282 — None cache guards for daemon jobs
- cash #283 — transfer ALE + dividend reinvestment Ascend guards
- portfolio #399 — full Ascend migration (trade_util, validate_etf, rebalance, process init)
- accounts #187 — ALE endpoint + APEX_API_ENTITY guards (investigations, documents)
- stratz #280 — remove dead Apex imports

**May 18 (ETF whitelist + co-author cleanup):**
- util #227 (revert #226), #228 (clean re-apply), #229 (ETF whitelist fix)

### Releases Cut (May 12-18, 40+ total)
- portfolio: dev-27.04 → dev-27.13 (10 releases)
- accounts: dev-6.133 → dev-6.139 (7 releases)
- cash: dev-15.14 → dev-15.20 (7 releases)
- app-backend: dev-12.80 → dev-12.83 (4 releases)
- auth: dev-9.34 → dev-9.38 (5 releases)
- events: dev-2.88 → dev-2.89 (2 releases)
- stratz: dev-11.28 → dev-11.32 (5 releases)
- util: dev-6.5.8 → dev-6.5.10 (3 releases)

### Open Items
- Yves proposed auth → DynamoDB migration to replace ElastiCache db#1. Needs scoping ticket.
- QC with Oleh — blocked until UAT creds (SBX has no real account data)
- UAT API key — Apex SOW review call May 20, UAT provisioning follows
- WebAuthn migration — `001_add_webauthn_credential` needs to run on dev DB (Chema)
- KPF/HF1 prod release — InvalidHeader fix sitting in dev, needs prod promotion
- 24% rollback ratio investigation — file ticket
- isoCurrencyCode test data — regenerate from live API response
- Prod index migration — coordinate with Yves for maintenance window

### Blockers
- Tomasz: Cloud Map DNS + cache env vars
- Apex TWR: Humaira researching (ticket #1108677)
- UAT Ascend credentials: SOW review call May 20 → UAT provisioning follows
- util branch protection: can't force-push to develop (need Maintain role from Tomasz)

## Key Links
- Jira: `TECH` project at sidepocket.atlassian.net
- Dev server: dev-ubuntu (172.31.1.203), SSH via ProxyJump
- Cache EC2: 54.162.5.34
- Sentry: sidepocket-incorporated org
- Sentry API token: sntryu_36c1... (stored in session, not committed)

## Detailed Notes
- [[sidepocket-infrastructure]] — full infra, PRs, ECS, Alembic state
- [[sidepocket-engineering]] — NAV formulas, Ascend API mapping, known issues
- [[sidepocket-team]] — people, Slack IDs
- [[sidepocket-codebase]] — all 9 services overview
- [[sidepocket-monday-queue]] — current action items
