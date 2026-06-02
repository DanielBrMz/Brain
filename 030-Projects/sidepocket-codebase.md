---
title: "Sidepocket — Microservices Codebase"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, sidepocket, codebase, microservices, flask, graphql, fintech]
---

# Sidepocket — Microservices Codebase

> Detailed codebase documentation for all 9 Sidepocket services. For infrastructure and project management see [[sidepocket-infrastructure|Sidepocket Infrastructure]].
> All services at `/home/ubuntu/code/<service>/` on dev-ubuntu.

---

## Service Architecture Overview

All services follow the same pattern:
- **Framework:** Flask
- **API:** GraphQL (Graphene) at `/graphql` + REST blueprints
- **Auth:** JWT (asymmetric RSA), verified via `util/app_helpers/jwt.py`
- **DB:** PostgreSQL via SQLAlchemy
- **Cache:** Redis (ElastiCache) → migrating to S3 Parquet
- **Background:** Daemon processes (`event_daemon.py` or similar)
- **Deploy:** Docker → AWS ECS (API container + daemon container per service)

---

## 1. auth (Port 4001)

**Purpose:** Authentication, user management, JWT token lifecycle.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app with `auth_conn` — shared connection object |
| `models/user.py` | User model (email, password hash, MFA) |
| `models/profile.py` | User profile (name, phone, address) |
| `models/device.py` | Device fingerprinting |
| `models/phone_verification.py` | Phone verification flow |
| `models/preference.py` | User preferences |
| `models/change_email_request.py` | Email change workflow |
| `schema/query.py` | GraphQL queries — **imports `from app import auth_conn` at module level** |
| `schema/mutation.py` | GraphQL mutations root |
| `schema/user_mutations.py` | User CRUD mutations |
| `schema/profile_mutations.py` | Profile mutations |
| `graphene_types/` | GraphQL type definitions |
| `auth_scripts/` | Admin/maintenance scripts |
| `event_daemon.py` | Background worker |

**Gotcha:** `schema/query.py` has `from app import auth_conn` at module level. `conda run` breaks this (circular import). Always use activated shell: `auth` alias then `python app.py`.

**Third-party:** Vonage (SMS), SendGrid (email), DynamoDB (JWT revocation via TECH-3832)

---

## 2. accounts (Port 4002)

**Purpose:** Account creation, KYC, Apex account management, SSN encryption.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `account_service_layer/handlers.py` | Business logic — account creation flow, KYC |
| `apex_api/apex_accounts_api.py` | Apex Clearing API — account applications, status |
| `crypto/ssn_encryption.py` | SSN encryption/decryption (sensitive) |
| `models/account_application.py` | Account application model (KYC, status) |
| `models/paper_account.py` | Paper/demo account model |
| `schema/` | GraphQL schema |

**Third-party:** Apex Clearing (brokerage account creation)

---

## 3. app-backend (Port 4003)

**Purpose:** Main API gateway. Aggregates data from all services. Serves frontend.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app — main entry point |
| `app_domain/models.py` | Domain models (SQLAlchemy) |
| `app_service_layer/handlers.py` | **Core business logic** — `calc_live_account_balances`, `calc_live_account_nav_time_series` |
| `view/live_account.py` | `/liveUserAccountBalances`, `/liveUserAccountNav` REST endpoints |
| `view/filter_sidepocket.py` | Sidepocket filtering |
| `view/funding_method.py` | Funding method endpoints |
| `schema/query.py` | GraphQL queries |
| `schema/mutation.py` | GraphQL mutations |
| `models/user_sidepocket.py` | User-sidepocket association |
| `models/aum_tier.py` | AUM tier configuration |
| `models/cash_entry.py` | Cash entry model |

**Critical formulas** (see [[sidepocket-engineering|Engineering Notes]] for details):
```python
cash_balance = cum_complete_deposit + abs(cum_complete_sell)
             - cum_complete_buy - abs(cum_complete_withdrawal)
             + dividends - fees + credits
accountValue = cash_balance - cum_pending_buy + total_allocation_dollars
```

**Third-party:** OneSignal (push notifications)

---

## 4. portfolio (Port 4007)

**Purpose:** Holdings management, NAV calculation, mark-to-market, order execution, SOD reconciliation.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `portf_service_layer/handlers.py` | Main service layer |
| `portf_service_layer/apex_order_service.py` | Order creation → Apex |
| `portf_service_layer/account_trade_status_log_service.py` | Trade status tracking |
| `portf_service_layer/sidepocket_holding_valuation.py` | **MTM/NAV core** — mark-to-market, valuation |
| `models/sp_holding.py` | Sidepocket holding (ticker, qty, entry/exit) |
| `models/sp_order_request.py` | Order request model |
| `models/rebalance_*.py` | Rebalancing models |
| `models/security_master.py` | Security master (CUSIP → symbol) |
| `models/transaction_summary.py` | Transaction aggregation |
| `apex_trade_api/` | Apex trading API integration |
| `process/batch.py` | **Batch processing** — `daily_qc()`, `check_accounts_unstable()`, SOD reconciliation |
| `event_daemon.py` | Background worker — portfolio events |

**Order flow (6 steps):**
1. Account eligibility check
2. Security master validation
3. Buying power check
4. Generate orders → Apex
5. Track via Events service
6. Update holdings

**SOD files:** EXT982 (positions), EXT901 (accounts), EXT981 (transactions)

---

## 5. cash (Port 4006)

**Purpose:** Cash transfers, ACH relationships, Plaid banking, recurring deposits, fees.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `cash_service_layer/handlers.py` | Cash transfer business logic |
| `cash_process/cash_balances.py` | Cash balance calculation + caching |
| `cash_process/process_cash_transfers.py` | Transfer state machine |
| `cash_process/apex_cash_api.py` | Apex cash/ACH API |
| `cash_process/ach_relationship_api.py` | ACH relationship management |
| `plaid_service/plaid_service.py` | Plaid API wrapper — `get_identity()`, `get_balances()` |
| `models/cash_transfer.py` | Cash transfer model (with `ix_cash_transfer_account_number` index) |
| `models/recurring_deposit.py` | Recurring deposit — `check_for_start_date_in_the_future` |
| `models/fees_and_credits.py` | Fees and credits (with `ix_fees_and_credits_account_number` index) |
| `models/acats.py` | ACATS transfer model |
| `cash_scripts/` | Maintenance scripts |

**Transfer states:** `PENDING` → `SUCCESS` / `ERROR` (Apex + Plaid + ACH flow)

**Third-party:** Plaid (bank linking), Apex (ACH transfers)

---

## 6. events (Port 4005)

**Purpose:** Notification dispatch (email, SMS, push) across all services.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `message_services/one_signal_api.py` | OneSignal push notifications |
| `message_services/smtp_email.py` | SMTP email sending |
| `message_services/twilio_client.py` | Twilio SMS |
| `daemon_tasks/notification_handler.py` | Background notification processing |
| `models/notification_model.py` | Notification model (type, status, recipient) |
| `schema/` | GraphQL schema |

---

## 7. billing (Port 4004)

**Purpose:** Subscription management, Stripe integration, AUM-based billing.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `operations/batch.py` | Batch billing operations |
| `operations/subscription.py` | Subscription lifecycle |
| `operations/stripe_bank_tokens.py` | Stripe bank token management |
| `stripe_util/stripe_api.py` | Stripe API wrapper |
| `models/plan.py` | Billing plan model |
| `models/stripe_account.py` | Stripe customer account |
| `models/subscription.py` | Subscription model |
| `models/aum_tier.py` | AUM tier pricing |

---

## 8. stratz (Port 4000)

**Purpose:** Market data, investment strategies, portfolio algorithms, backtesting.

**Key Files:**
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `algo/` | **12 strategy algorithms:** |
| | RiskOptimized, DualMomentum, ElasticAssetAllocation, |
| | GoldenButterfly, PermanentPortfolio, AllWeatherBridge, |
| | MomentumFactor, ValueFactor, GrowthFactor, |
| | DividendGrowth, SectorRotation, TacticalBond |
| `market_data/` | Market data fetching (IEX, Tiingo, MarketDataStack) |
| `domain/` | Domain models |
| `backtest/` | Strategy backtesting engine |
| `daemon.py` | Market data daemon — periodic data refresh |
| `adapters/dynamodb_orm.py` | DynamoDB adapter for market data storage |

**Third-party:** IEX Cloud, Tiingo, MarketDataStack (market data providers), AWS DynamoDB

---

## 9. util (Shared Library)

**Purpose:** Shared utilities used by all services. Installed as package via `pip install /usr/src/util` in Docker.

**Key Files:**
| File | Purpose |
|------|---------|
| `cache/cache_utils.py` | `AccountingCacheHandler` — cash cards, transaction summaries |
| `cache_service/app.py` | Cache service Flask app (TECH-3830) |
| `cache_service/server.py` | ZeroRPC server for long-running cache |
| `cache_service/store.py` | `InMemoryStore` — cache from S3 Parquet |
| `cache_service/poller.py` | S3 polling for cache updates |
| `db/cache_store.py` | `CacheStore` ABC (TECH-3827) |
| `db/db_session.py` | SQLAlchemy session management |
| `db/redis/RedisIO.py` | Redis wrapper — `get_df`, `mget_pattern_df` |
| `app_helpers/jwt.py` | JWT verification/generation |
| `app_helpers/blueprint.py` | Flask blueprint helpers |
| `app_helpers/caching.py` | Caching decorators |
| `app_helpers/cors.py` | CORS configuration |
| `app_helpers/config.py` | Config loader |
| `apex_api_util/` | Shared Apex API utilities |
| `finance/date_utils.py` | Trading day calculations |
| `finance/holiday_calendar.py` | Market holiday calendar |
| `crypto/hkdf.py` | HKDF key derivation |
| `config_utils/redis_config.py` | Redis connection configuration |

---

## Service Communication

```
Frontend (webapp) → app-backend (4003) → {all services via internal REST/GraphQL}
                         ↕
                    Redis (cache)  →  S3 Parquet (migration target)
                         ↕
              portfolio ←→ cash ←→ accounts
                  ↕           ↕
              Apex API    Plaid API
                  ↕
               stratz (market data)
                  ↕
            events (notifications)
```

---

## Database Schema (Key Tables)

Each service has its own PostgreSQL database. Key models:

| Service | Key Models |
|---------|-----------|
| auth | user, profile, device, phone_verification, preference |
| accounts | account_application, paper_account |
| app-backend | user_sidepocket, aum_tier, cash_entry |
| portfolio | sp_holding, sp_order_request, security_master, transaction_summary, rebalance_* |
| cash | cash_transfer, recurring_deposit, fees_and_credits, acats |
| events | notification |
| billing | plan, stripe_account, subscription, aum_tier |
| stratz | (DynamoDB — market data, strategy configs) |

---

## Related Notes

- [[sidepocket-infrastructure|Sidepocket Infrastructure]] — AWS, deployment, Docker, tickets
- [[sidepocket-engineering|Sidepocket Engineering Notes]] — NAV formulas, Redis, S3 schema, debugging
- [[sidepocket-team|Sidepocket Team]] — people and roles
- [[sidepocket-webapp|Sidepocket Webapp]] — Next.js frontend
