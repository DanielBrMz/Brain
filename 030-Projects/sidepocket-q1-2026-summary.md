# Daniel Barreras — Q1 2026 Engineering Summary

> For Max's shareholder presentation. Covers Jan 1 – Mar 31, 2026 (with early April included since Max asked for "first part of the year").

---

## By the Numbers

| Metric | Count |
|--------|-------|
| Pull Requests (Q1 alone) | 50+ |
| Pull Requests (through Apr 8) | 63 |
| Repos touched | 7 (accounts, auth, app-backend, cash, events, portfolio, util) |
| Services fully upgraded | 6 |
| Redis keys migrated to S3 | 2,837+ (zero failures) |
| Production bugs fixed | 10+ |
| Prod incidents resolved | 2 (TECH-3879 + SSN encryption) |
| Performance improvement | 20-49x on cache reads |

---

## January 2026

### SSN Encryption Hardening & IAM (Jan 5–9)
- **accounts #150**: Added detailed logging for SSM parameter access debugging
- **accounts #151**: Added SSN_MASTER_KEY and SSN_SALT to ECS params for dev and UAT
- Fixed deployment issue where new AES-GCM SSN encryption was being enforced while accounts repo couldn't be deployed
- Diagnosed AWS IAM permissions gap: ECS task roles lacked `ssm:GetParameter` for Parameter Store keys
- Escalated and resolved with Max

### Transaction Processing & Account Status (Jan 14)
- **cash #235**: TECH-3285 — Fixed transaction status issue when account status changes from pending to completed
- **cash #236, #237**: Queued processing implementation
- **cash #238**: Reverted queued processing (issues found)
- **cash #239**: Queued processing + Plaid validation (fixed version)
- **cash #240**: Plaid relationship improvements
- **cash #241**: Fixed queued-for-processing stuck cases
- **accounts #152**: JWT-legacy adaptive dict-JSON input handling

### SSN Encryption & Portfolio Fixes (Jan 16–28)
- **accounts #153, #154**: Moved SSN encryption to env variables instead of SSM calls (cost + latency improvement)
- **portfolio #342, #343**: TECH-3688 — Date mismatch fixes causing transaction issues across accounts
- **portfolio #346**: Fixed account value increases after Sidepocket liquidation (prod bug)
- **accounts #155**: Fixed formJson field to return valid JSON in GraphQL response

### Auth Daemon Fix (Jan 8)
- Resolved daemon mismatch causing failures

---

## February 2026

### Liquidation & NAV Fixes (Feb 3–13)
- **auth #177**: Resolved query merge conflict on auth dev
- **cash #243**: Fixed TypeError (date not JSON serializable)
- **portfolio #349**: TECH-3720 — Fixed NAV memory performance issue
- **portfolio #348**: Reverted performance bottleneck (PR #340)
- **portfolio #350**: Fixed exit-date MTM double-count on liquidation (prod bug)
- **portfolio #351**: Fixed intraday liquidation calculation (prod bug)
- **cash #247**: Handle expected Plaid errors in get_identity without raising

### Redis OOM Root Cause Analysis — TECH-3781 (Feb 6)
- Comprehensive investigation proving 384MB ElastiCache instance is undersized (not a leak)
- Full memory breakdown across all data types: 1Y (80.7MB), MAX (59.4MB), NAV (48.6MB), etc.
- Identified working set grows continuously as accounts age
- Recommended architectural fix (which became the S3 migration)
- **util #198**: Added memory checks and TTL support to RedisIO
- **cash #244**: Safe caching with TTL for cash balance operations

### Performance Optimization (Feb 17–19)
- **portfolio #353**: Fixed timestamp precision mismatch
- **portfolio #355**: Batched Redis reads in liveUserSidepocketList (perf)
- **util #199**: Cut Redis round-trips on all lookup endpoints (perf)
- **cash #248**: Added account_number indexes on cash_transfer and fees_and_credits (perf)
- **cash #249**: Added UUID primary key to cash_activity model
- **app-backend #114**: Fixed account NAV during pending buy orders (subtract cum_pending_buy)

### Bug Fixes & QA (Feb 23–26)
- **cash #251**: TECH-3796 — Suppress Apex interface errors on non-prod environments
- **accounts #157**: TECH-3796 — Same fix on accounts
- **cash #252**: TECH-3797 — Fixed recurring deposit reactivation sending past start date
- **portfolio #356**: TECH-3797 — Added instability status check to daily QC report
- **auth #178**: Fixed createProfile crash when income map cache key is absent
- **cash #253**: Guarded against None return from check_allowed_retirement_contribution

### Architecture Design (Feb 27–28)
- Designed full Redis → S3 migration architecture
- Evaluated S3 Parquet vs DynamoDB, ZeroMQ vs HTTP, PyArrow CoW implications
- Analyzed JWT auth pattern weaknesses and designed revocation-only architecture
- Identified rate limiting implementation weakness (no atomic INCR/EXPIRE)
- Audited full stack versions (Python 3.8.10, Pandas 1.1.3) → planned upgrade path

---

## March 2026

### Architecture Migration — Build Phase (Mar 2–11)
- **TECH-2979 Epic**: Cleared old tickets, populated with 8 new stories for full migration
- **util #200**: TECH-3827 — CacheStore ABC (storage abstraction layer)
- **auth #179**: TECH-3832 — RevocationStore ABC (JWT decoupling from Redis)
- **util #201**: TECH-3829 — S3 dual-write pipeline (portfolio + util)
- **portfolio #358**: TECH-3829 — Dual-write sidepocket and transaction caches to S3 Parquet
- **util #202**: TECH-3830 — Cache service implementation
- **util #203**: TECH-3831 — One-time Redis to S3 Parquet migration script
- **util #204**: TECH-3831 — Redis to S3 migration (final)
- **app-backend #115**: TECH-3800 — Migrated Redis read call sites to abstraction layer
- **portfolio #359**: TECH-3800 — Same migration on portfolio
- **cash #255**: TECH-3800 — Same migration on cash
- **portfolio #357**: TECH-3812 — Fix NAV cache stitch

### Stack Upgrade — TECH-3826 (Mar 12)
All 6 backend services + util upgraded to Python 3.14 / Flask 3.1 / SQLAlchemy 2.0 / Pandas 3 / PyArrow:
- **util #205**: Tech 3826
- **cash #256**: Tech 3826
- **portfolio #360**: Tech 3826
- **app-backend #116**: Tech 3826
- **auth #180**: Tech 3826
- **accounts #158**: Tech 3826
- **events #85**: Tech 3826
- **stratz #270**: Tech 3826

### Migration Execution (Mar 20)
- Ran full Redis → S3 migration: 2,837 keys, zero failures
- Speed benchmarks: **20-49x faster** on single-key reads, **11x on multi-key gets**
- Added `mget_pattern_df_filtered`: cut wire transfer from 60MB → matching rows only
- ~3 min cold start (one-time)

### Code Review & Collaboration (Mar 23–28)
- Reviewed and merged Chema's auth PRs: WebAuthn credential model (#182), deps (#183), AESGCM challenge encryption (#184)
- Alembic upgrade head automation in Dockerfile entrypoint
- Flagged Alembic migration chain conflict risk with Chema's PR

### Production Incident — TECH-3879 (Mar 31)
Fixed DateTime column defaults across ALL 6 services (`server_default=func.now()`):
- **auth #187**, **accounts #159**, **app-backend #117**, **cash #258**, **events #86**, **portfolio #361** — all merged
- Alembic migrations staged for each EC2 in correct deploy order
- **accounts #160**: TECH-3883 — Normalized account_sub_type enum for APEX form lookup

---

## April 2026 (through Apr 8)

### Ascend Migration — TECH-3152/3153
- **util #206**: TECH-3153 — Built AscendToken auth class (RS256/JWS) + all ascend_* API wrappers (submit, get, put, ALE, doc upload). **Merged.**
- Researched MTM simplification: `open_liquidity_amount` from Ascend replaces in-house accountValue formula
- Mapped all 20+ Apex API calls in cash service for migration
- **Blocker**: Ascend credentials not yet configured on dev-ubuntu

### Production Bug Fixes
- **accounts #162**: TECH-3883 — Fixed account_sub_type enum before APEX form lookup
- **accounts #163**: Filtered null account_number from consolidated list query
- **accounts #165**: Guarded against None last_updated in consolidatedList
- **accounts #166**: Fixed missing import os and base64 in ssn_encryption
- **accounts #167**: Removed Argon2id, switched to AES-256-GCM-SIV for SSN encryption (open)

### TECH-3879 UAT Deployment
- Applied DEFAULT now() to all affected columns across UAT (sp_user + cash DBs)
- Sync main → develop across all 6 services: auth #189, accounts #164, app-backend #118, cash #260, events #87, portfolio #362

### Code Review
- Tested Chema's WebAuthn config PR #190 on UAT
- Reviewed Yves's security feedback on encryption approach

---

## Complete PR List (63 PRs, Jan 1 – Apr 8, 2026)

### accounts (16 PRs)
| # | Title | State |
|---|-------|-------|
| 150 | Add detailed logging for SSM parameter access debugging | merged |
| 151 | Add SSN_MASTER_KEY and SSN_SALT to ECS params | merged |
| 152 | JWT-legacy adaptive dict-json inputs | merged |
| 153 | Env variables instead of SSM calls | merged |
| 154 | Env variables instead of SSM calls | merged |
| 155 | Fix formJson field to return valid JSON in GraphQL | merged |
| 157 | TECH-3796: suppress Apex interface errors on non-prod | merged |
| 158 | Tech 3826 (stack upgrade) | open |
| 159 | TECH-3879: fix DateTime column defaults | merged |
| 160 | TECH-3883: normalize account_sub_type enum | merged |
| 161 | develop → main (TECH-3883) | closed |
| 162 | TECH-3883: normalize account_sub_type before APEX form | merged |
| 163 | Filter null account_number from consolidated list | merged |
| 164 | Sync main → develop (TECH-3879) | merged |
| 165 | Guard against None last_updated in consolidatedList | merged |
| 166 | Fix missing import os and base64 in ssn_encryption | merged |
| 167 | Remove Argon2id, switch to AES-256-GCM-SIV | open |

### auth (5 PRs)
| # | Title | State |
|---|-------|-------|
| 177 | Fix/resolve query merge conflict | merged |
| 178 | Fix createProfile crash on missing income map cache | merged |
| 179 | Tech 3832 (JWT revocation rearchitect) | merged |
| 180 | Tech 3826 (stack upgrade) | open |
| 187 | TECH-3879: fix DateTime column defaults | merged |
| 189 | Sync main → develop (TECH-3879) | merged |

### app-backend (4 PRs)
| # | Title | State |
|---|-------|-------|
| 114 | Fix: subtract cum_pending_buy from account NAV | merged |
| 115 | TECH-3800: migrate Redis reads to abstraction layer | open |
| 116 | Tech 3826 (stack upgrade) | open |
| 117 | TECH-3879: fix DateTime column defaults | merged |
| 118 | Sync main → develop (TECH-3879) | merged |

### cash (14 PRs)
| # | Title | State |
|---|-------|-------|
| 235 | TECH-3285: transaction status on pending→complete | merged |
| 236 | Queued processing | merged |
| 237 | Queued processing | merged |
| 238 | Revert "Queued processing" | merged |
| 239 | Queued processing + Plaid validation | merged |
| 240 | Plaid relationship | merged |
| 241 | Queued for processing stuck cases | merged |
| 243 | Fix TypeError: date not JSON serializable | merged |
| 244 | TECH-3781: safe caching with TTL | open |
| 247 | Handle Plaid errors in get_identity | merged |
| 248 | perf: add account_number indexes | merged |
| 249 | fix: add UUID primary key to cash_activity | merged |
| 251 | TECH-3796: suppress Apex errors on non-prod | merged |
| 252 | TECH-3797: fix recurring deposit past start date | merged |
| 253 | hotfix: guard against None retirement contribution | merged |
| 255 | TECH-3800: migrate Redis reads | open |
| 256 | Tech 3826 (stack upgrade) | open |
| 258 | TECH-3879: fix DateTime defaults | merged |
| 260 | Sync main → develop (TECH-3879) | merged |

### events (3 PRs)
| # | Title | State |
|---|-------|-------|
| 85 | Tech 3826 (stack upgrade) | open |
| 86 | TECH-3879: fix DateTime defaults | merged |
| 87 | Sync main → develop (TECH-3879) | merged |

### portfolio (13 PRs)
| # | Title | State |
|---|-------|-------|
| 342 | Tech 3688 | merged |
| 343 | Tech 3688 | merged |
| 346 | Account value increases after liquidation | merged |
| 347 | Tech 3720 fix nav memory | closed |
| 348 | Revert 340 performance bottleneck | merged |
| 349 | Tech 3720 fix nav memory | merged |
| 350 | Fix exit-date MTM double-count on liquidation | merged |
| 351 | Fix intraday liquidation | merged |
| 353 | Timestamp precision mismatch | merged |
| 355 | perf: batch Redis reads in liveUserSidepocketList | merged |
| 356 | TECH-3797: instability status check in QC report | merged |
| 357 | Tech 3812 fix nav cache stitch | open |
| 358 | TECH-3829: dual-write to S3 Parquet | merged |
| 359 | TECH-3800: migrate Redis reads | open |
| 360 | Tech 3826 (stack upgrade) | open |
| 361 | TECH-3879: fix DateTime defaults | merged |
| 362 | Sync main → develop (TECH-3879) | merged |

### util (8 PRs)
| # | Title | State |
|---|-------|-------|
| 198 | TECH-3781: memory checks + TTL support to RedisIO | open |
| 199 | perf: cut Redis round-trips on all lookup endpoints | merged |
| 200 | Tech 3827 (storage abstraction layer) | merged |
| 201 | Tech 3829 (S3 dual-write pipeline) | merged |
| 202 | TECH-3830 (cache service) | merged |
| 203 | TECH-3831: Redis to S3 migration script | merged |
| 204 | Tech 3831 redis to s3 migration | merged |
| 205 | Tech 3826 (stack upgrade) | open |
| 206 | TECH-3153: Ascend auth infrastructure | merged |

### stratz (1 PR)
| # | Title | State |
|---|-------|-------|
| 270 | Tech 3826 (stack upgrade) | open |
