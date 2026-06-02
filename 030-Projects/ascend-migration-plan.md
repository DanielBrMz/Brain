# TECH-3152 — Ascend Migration Plan

**Epic:** Apex (legacy) → Apex Ascend
**Constraint:** All-or-nothing deploy. Partial rollout shuts everything down.
**Assigned:** Daniel Barreras
**Status:** Planning → In Progress (TECH-3153 auth setup already started)
**Deploy flow:** QA on `dev` → copy to new branch → remove from `dev`

---

## Codebase Reality (as of 2026-04-02)

**3 services call Apex directly:**
- `accounts` — account creation, KYC, ALE polling
- `cash` — ACH relationships, deposits/withdrawals, recurring transfers, IRA constraints
- `portfolio` — fractional trading orders, ALE polling, SOD file parsing

**2 services are unaffected:**
- `auth` — no Apex calls
- `events` — no Apex calls (downstream of cash/portfolio/accounts)
- `app-backend` — no Apex calls (aggregates data, doesn't call Apex)

**Shared utility:** `util/apex_api_util/`
- `apex_auth.py` — `APEXToken` class (JWS auth → Bearer JWT)
- `__init__.py` — `submit_to_apex`, `get_from_apex`, `put_to_apex`, `get_apex_ale_messages`, `post_doc_apex`
- `sod_files.py` — SOD file parsing (EXT981/EXT901/EXT982 from SFTP)
- `constants.py` — status enums and topic names

**Current auth (legacy):**
```python
# env vars required
APEX_API_USERNAME, APEX_API_ENTITY, APEX_API_SHARED_SECRET

# flow: JWS HS512 signature → /legit/api/v1/cc/token → Bearer JWT
# validate: GET /legit/api/v2/verify
# logout: GET /legit/api/v1/logout
```

**Current base URLs:**
- UAT: `https://uat-api.apexclearing.com`
- Prod: `https://api.apexclearing.com`

---

## Current Endpoint Map (Legacy)

### accounts service (`apex_api/apex_accounts_api.py`)
| Action | Method | Path |
|---|---|---|
| Submit account opening form | POST | `/atlas/api/v2/account_requests` |
| Get account request | GET | `/atlas/api/v2/account_requests/{id}` |
| Close account | PUT | `/atlas/api/v1/accounts/{account}/restrictions/CLOSED_BY_FIRM` |
| Get account info | GET | `/atlas/api/v1/accounts/{account}` |
| List form versions | GET | `/atlas/api/v1/forms/{title}/versions` |
| Get form content | GET | `/atlas/api/v1/forms/{title}/versions/{version}` |
| Poll ALE | GET | `/ale/api/v1/read/{topic}/{correspondent}` |
| ALE topic | — | `atlas-account_request-status` |

### cash service (`cash_process/apex_cash_api.py`)
| Action | Method | Path |
|---|---|---|
| Create deposit | POST | `/sentinel2/api/v1/transfers/achs/deposits` |
| Create withdrawal | POST | `/sentinel2/api/v1/transfers/achs/withdrawals` |
| IRA constraints | GET | `/sentinel2/api/v1/ira_constraints/{account}/{method}/{direction}` |
| Create ACH relationship | POST | `/sentinel2-counterparty/api/v1/ach_relationships` |
| Get ACH relationship | GET | `/sentinel2-counterparty/api/v1/ach_relationships/{id}` |
| List ACH relationships | GET | `/sentinel2-counterparty/api/v1/ach_relationships?account=...` |
| Cancel ACH relationship | POST | `/sentinel2-counterparty/api/v1/ach_relationships/{id}/cancel` |
| Update ACH with Plaid data | PUT | `/sentinel2-counterparty/api/v1/ach_relationships/{id}/update_plaid` |
| Get cash balance | GET | `/cash-balances/api/v2/available/{account}` |
| Create recurring deposit | POST | `/scheduled-transfers/api/v1/schedules/achs/deposits` |
| List recurring deposits | GET | `/scheduled-transfers/api/v1/schedules/achs?accountNumber=...` |
| Update recurring amount | PUT | `/scheduled-transfers/api/v1/schedules/achs/deposits/{id}/update` |
| Cancel recurring deposit | PUT | `/scheduled-transfers/api/v1/schedules/achs/deposits/{id}/cancel` |
| Poll ALE (ACH) | GET | `/ale/api/v1/read/...` |
| Poll ALE (transfers) | GET | `/ale/api/v1/read/...` |
| Poll ALE (ACATS) | GET | `/ale/api/v1/read/...` |
| ALE topics | — | `sentinel2-ach-relationship-status`, `sentinel2-transfer-state`, `alps-acat-status` |

### portfolio service (`apex_trade_api/trade_util.py`)
| Action | Method | Path |
|---|---|---|
| Place fractional order | POST | `/fractional-trading/api/v1/orders` |
| Get order status | GET | `/fractional-trading/api/v1/orders/{date}/{id}` |
| Cancel order | POST | `/fractional-trading/api/v1/orders/{date}/{id}:cancel` |
| List active symbols | GET | `/fractional-trading/api/v2/symbol` |
| Poll ALE | GET | `/ale/api/v1/read/...` |
| ALE topic | — | `fractional-trading-status` |
| SOD files | SFTP | `files.apexclearing.com` — EXT981, EXT901, EXT982 |

---

## Migration Plan

### Phase 0 — Prerequisites (before coding)
- [ ] Get Ascend API credentials (base URL, OAuth client ID/secret or new auth mechanism)
- [ ] Get Ascend endpoint mapping documentation from Maxwell/Apex team
- [ ] Confirm Ascend equivalents for:
  - ALE/event polling mechanism (same `/ale/` pattern? webhooks?)
  - SOD file delivery (same SFTP host? same file formats?)
  - ACH relationship creation (Plaid token still supported?)
- [ ] Set up `ASCEND_*` env vars in dev `.env` files

### Phase 1 — Auth infrastructure (TECH-3153) ← **START HERE**
**File:** `util/apex_api_util/ascend_auth.py` (new) + update `__init__.py`

- [ ] Implement `AscendToken` class (replacing `APEXToken` JWS flow with Ascend OAuth)
- [ ] Update `submit_to_ascend`, `get_from_ascend`, `put_to_ascend` wrappers
- [ ] Update `get_ascend_ale_messages` (or implement webhook alternative)
- [ ] Add `ASCEND_BASE_URL` env var to all service configs
- [ ] Test auth against Ascend sandbox

**Env vars to add:**
```
ASCEND_BASE_URL
ASCEND_CLIENT_ID (or ASCEND_API_USERNAME equivalent)
ASCEND_CLIENT_SECRET (or ASCEND_API_SHARED_SECRET equivalent)
```

### Phase 2 — Cash service (TECH-3158, 3159, 3160)
**Files:** `cash/cash_process/apex_cash_api.py`, `cash/cash_process/ach_relationship_api.py`

- [ ] Map all sentinel2 / sentinel2-counterparty endpoints to Ascend equivalents
- [ ] Map scheduled-transfers endpoints
- [ ] Map cash-balances endpoint
- [ ] Update ALE topic names (sentinel2-ach-relationship-status, sentinel2-transfer-state, alps-acat-status)
- [ ] Update IRA constraints endpoint
- [ ] Verify ACH relationship creation still uses Plaid processor token (or new bank linking method)

### Phase 3 — Portfolio service (TECH-3162, 3154, 3155, 3161)
**Files:** `portfolio/apex_trade_api/trade_util.py`, `portfolio/process/sod_files.py`

- [ ] Map fractional-trading endpoints
- [ ] Update ALE topic name (fractional-trading-status)
- [ ] Verify SOD file delivery:
  - SFTP host change (files.apexclearing.com → files.ascend.com?)
  - File format changes (EXT981/EXT901/EXT982 — same schema? new names?)
  - Update `sod_files.py` in apex_api_util if format changes
- [ ] Map symbol listing endpoint (`/fractional-trading/api/v2/symbol`)

### Phase 4 — Accounts service (TECH-3156, 3157)
**Files:** `accounts/apex_api/apex_accounts_api.py`

- [ ] Map atlas account_requests endpoints (submit, get, close)
- [ ] Map form versioning/hashing flow (Ascend may use different form IDs or no hash requirement)
- [ ] Update ALE topic name (atlas-account_request-status)
- [ ] Update `repCode` and `branch` constants if they change (currently `ZXB` / `8JS`)
- [ ] Verify dividend reinvestment schema still applies

### Phase 5 — Config updates (all services)
- [ ] Add `ASCEND_BASE_URL` to `config.py` and `{env}.cfg` for accounts, cash, portfolio
- [ ] Update docker-compose files and ecs-params with new env vars
- [ ] Add new ALE topic config keys
- [ ] Remove or keep old `APEX_*` vars during transition period

### Phase 6 — QA on dev
- [ ] Run existing test suites against Ascend sandbox
- [ ] Test end-to-end flows:
  - Account creation → approval
  - ACH relationship creation → deposit
  - Fractional order → fill → holdings update
  - Recurring deposit creation/cancellation
  - IRA contribution with constraints
  - Account closure
- [ ] Verify ALE message processing works
- [ ] Verify SOD file parsing works with Ascend files

### Phase 7 — Cutover (all-or-nothing deploy)
- [ ] Cut branch from dev per Max's flow
- [ ] Coordinate simultaneous deploy of accounts + cash + portfolio
- [ ] Add `ASCEND_*` credentials to AWS Parameter Store before deploy
- [ ] Have rollback plan ready (revert to legacy `apex_api_util` if Ascend fails)

---

## Key Risks

| Risk | Mitigation |
|---|---|
| Ascend auth mechanism differs significantly | Confirm in Phase 0 before writing code |
| ALE polling changes to webhook model | Confirm in Phase 0; may need new event daemon |
| SOD file format changes | Get sample Ascend files before migrating sod_files.py |
| Partial deploy causes outage | Enforce all-at-once deployment (never deploy 1 of 3 services) |
| Plaid token no longer accepted for ACH | Confirm ACH bank-linking flow with Apex/Ascend team |
| `repCode` / `branch` constants change | Confirm with Maxwell — these are hardcoded as ZXB/8JS currently |

---

## Files to Change (summary)

```
util/apex_api_util/
  ascend_auth.py          ← NEW (AscendToken class)
  __init__.py             ← UPDATE (add ascend_ wrappers)
  sod_files.py            ← UPDATE if SOD format/host changes
  constants.py            ← UPDATE topic names + status enums

accounts/
  apex_api/apex_accounts_api.py   ← UPDATE all endpoint paths
  config/config.py                ← ADD ASCEND_BASE_URL, topics
  config/uat.cfg + prod.cfg       ← ADD ASCEND_BASE_URL

cash/
  cash_process/apex_cash_api.py   ← UPDATE all endpoint paths
  cash_process/ach_relationship_api.py  ← UPDATE if needed
  config/config.py                ← ADD ASCEND_BASE_URL, topics
  config/uat.cfg + prod.cfg       ← ADD ASCEND_BASE_URL

portfolio/
  apex_trade_api/trade_util.py    ← UPDATE all endpoint paths
  config/config.py                ← ADD ASCEND_BASE_URL, topics
  config/uat.cfg + prod.cfg       ← ADD ASCEND_BASE_URL
```

---

## Starting Point

TECH-3153 (auth setup) is In Progress. Begin by:
1. Confirming what Ascend's auth mechanism is (OAuth 2.0 client credentials? Same JWS? API key?)
2. Writing `AscendToken` in `util/apex_api_util/`
3. Testing against Ascend sandbox before touching any service code
