---
title: "dev-ubuntu — Sidepocket Microservices Server"
type: infrastructure
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [infrastructure, sidepocket, dev-ubuntu, microservices, flask, graphql]
---

# dev-ubuntu — Sidepocket Microservices Server

> Development server hosting all 9 Sidepocket microservices.

## Overview

| Field | Value |
|-------|-------|
| **Access** | SSH via agent socket (`~/.ssh/agent/`) |
| **Repos path** | `~/sidepocket/` |
| **Services** | 9 Flask microservices |
| **Pattern** | Flask + Graphene GraphQL + PostgreSQL + Redis + JWT |
| **Deployment** | Docker + AWS ECS |

## Common Architecture

All services share an identical pattern:

```
service/
├── app.py              # Flask app, JWT setup, CORS, Sentry, GraphQL endpoint
├── requirements.txt    # Python deps (Flask, graphene, SQLAlchemy, redis, etc.)
├── schema/             # GraphQL schema (query.py, mutation.py, schema.py)
├── config/             # Per-env configs (dev.cfg, qa.cfg, uat.cfg, prod.cfg)
├── config/gunicorn.py  # Gunicorn config for production
├── logger/             # Logging setup
├── view/               # GraphQL view + REST blueprints
├── db/                 # Database models + Redis connections
└── test/               # pytest (int/, sys/, uat/)
```

**Shared env vars:** `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOSTNAME`, `POSTGRES_PORT`, `SECRET_KEY`, `CACHE_REDIS_HOST`, `MKT_DATA_REDIS_HOST`, `SMTP_ENDPOINT`, `SMTP_USER`, `SMTP_PWD`

**JWT:** All services use `flask-jwt-extended` with asymmetric crypto. Token blacklist via Redis.

**Deployment:** Sentry DSN at `o486974.ingest.us.sentry.io`. Docker multi-stage builds where present.

---

## Services

### 1. accounts

| Field | Value |
|-------|-------|
| **Purpose** | User SP accounts, applications, lookups |
| **Integrations** | Apex API (clearing), SMTP |
| **Env var** | `BACKEND_APP_SETTINGS` |
| **Extra env** | `APEX_API_USERNAME`, `APEX_API_ENTITY`, `APEX_API_SHARED_SECRET` |
| **Dockerfile** | Yes (multi-stage, Python 3.14-slim) |

### 2. app-backend

| Field | Value |
|-------|-------|
| **Purpose** | Main backend — depends on stratz + util |
| **Integrations** | OneSignal (push notifications), Apex, SMTP, Twilio |
| **Env var** | `BACKEND_APP_SETTINGS` |
| **Extra env** | `ONESIGNAL_REST_TOKEN`, `ONESIGNAL_APP_ID`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` |
| **Dockerfile** | Yes (multi-stage) |
| **Notes** | CORS allows localhost:3000, admin.sidepocket.com, admindev.sidepocket.com |

### 3. auth

| Field | Value |
|-------|-------|
| **Purpose** | JWT authentication, 2FA, SMS verification |
| **Integrations** | Keycloak, Vonage (SMS), pyotp (2FA), Flask-Bcrypt |
| **Env var** | `AUTH_APP_SETTINGS` |
| **Extra env** | `VONAGE_API_KEY`, `VONAGE_API_SECRET`, `VONAGE_BRAND_NAME` |
| **Dockerfile** | Yes (multi-stage) |

### 4. billing (DEPRECATED)

| Field | Value |
|-------|-------|
| **Purpose** | Subscriptions, endorser relationships |
| **Integrations** | Stripe, Plaid |
| **Status** | **COMPLETELY DEPRECATED** — ignore in all contexts |
| **Env var** | `BILLING_APP_SETTINGS` |

### 5. cash

| Field | Value |
|-------|-------|
| **Purpose** | Cash transfers and deposits |
| **Integrations** | Plaid (identity/auth), Apex (ACH transfers) |
| **Env var** | `CASH_APP_SETTINGS` |
| **Extra env** | `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV`, `APEX_API_*` |
| **Notes** | Complex state machine for transfer lifecycle |

### 6. events

| Field | Value |
|-------|-------|
| **Purpose** | Pub-sub event handling via Redis streams |
| **Integrations** | Twilio, OneSignal, Apex, SMTP |
| **Env var** | `EVENTS_APP_SETTINGS` |
| **Extra env** | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `ONESIGNAL_*` |
| **Notes** | Token blacklist check on JWT — returns `True` if entry is `None` |

### 7. portfolio

| Field | Value |
|-------|-------|
| **Purpose** | Portfolio management, order execution, reconciliation |
| **Integrations** | Apex (fractional orders, SOD files), SMTP |
| **Env var** | `PORTFOLIO_APP_SETTINGS` |
| **Extra env** | `APEX_API_*`, `MKT_DATA_POSTGRES_*` |
| **Dependencies** | util, stratz |

**Order workflow:** Account check → Symbol validation (SecurityMaster) → Buying power check → Generate Apex fractional orders → Track via Events → Update SpOrderRequest, ApexOrder, SpHolding, Portfolio Values

**Recon workflow:** SOD EXT982 position breakout → Generate SOD TotalEquity/returns → Recon with EXT901 (Balance) + EXT981 (OvernightBuyingPower)

**Apex SOD Files:**
- **EXT981**: OvernightBuyingPower — CashTradeBalance, CashEquity, PositionMarketValue, TotalEquity, AvailableToWithdraw
- **EXT901**: Balance — TradeBalance, SettleBalance, MarketBalance
- **EXT982**: Position Breakout — CUSIP, Symbol, TradeQuantity, ClosingPrice, MarketValue, PositionType

### 8. stratz (Research Server)

| Field | Value |
|-------|-------|
| **Purpose** | Investment strategies, backtesting, market data |
| **Integrations** | IEX Cloud, Tiingo, FRED, MarketDataStack, boto3 (S3) |
| **Env var** | `STRATZ_APP_SETTINGS` |
| **Extra env** | `IEX_API_TOKEN`, `TIINGO_API_KEY`, `FRED_API_TOKEN`, `MARKETDATASTACK_API_TOKEN` |
| **Dockerfile** | Yes (Python 3.14-slim, multi-stage) |
| **Dependencies** | util |

**Algorithms:** FixedWgt, RiskOptimized, DefensiveAssetAllocation, DualMomentum, EMA, ElasticAssetAllocation, HYBondRotation, MACrossover, ProtectiveAssetAllocation, RiskParity, SMA, TacticalBond, VigilantAssetAllocation

**Capabilities:**
- Strategy backtesting (`StrategyRunner`, `SidepocketRunner`, `AccountRunner`)
- Market data jobs: `SecPricesJob`, `SecMetadataJob`, `IntradayPricesJob`, `DownloadSplitsJob`
- Data providers: `AccountDataProvider`, `SecurityDataProvider`, `DataStore`
- Report generation: `ReportDataGenerator`

**Extra deps:** `scipy`, `pandas-datareader`, `matplotlib`, `iexfinance`, `pandera`, `freezegun`, `schedule`

### 9. util (Cross-Service Library)

| Field | Value |
|-------|-------|
| **Purpose** | Shared utility library used by all services |
| **No app.py** | Library only — installed as a package |
| **No Dockerfile** | Installed as dependency |
| **Tests** | 66 passed, 3 xfailed, 17 warnings |
| **Env var** | `ASCEND_DEV_*` (Ascend integration) |

**Key deps:** `pandas_market_calendars`, `graphene`, `numpy`, `pandas`, `python-keycloak`, `redis`, `PyGithub`, `boto3`, `glom`

## Local Dev Setup

```bash
# From stratz README — applies to all services:
# 1. Create project dirs
sudo mkdir -p /opt/sidepocket/
sudo chown -R $USER:$USER /opt/sidepocket

# 2. Docker + Redis
docker network create kitt
# Redis via docker-compose at /opt/sidepocket/redis/

# 3. Each service:
cd ~/sidepocket/<service>
pip install -r requirements.txt
export <SERVICE>_APP_SETTINGS=./config/dev.cfg
python app.py  # or gunicorn -c config/gunicorn.py app:app
```

## Related

- [[sidepocket-backend|Sidepocket Backend (sp-app)]]
- [[sidepocket-webapp|Sidepocket Webapp]]
- [[cache-ec2|Cache EC2]]
- [[sp-backend-api-testing|API Testing Suite]]
