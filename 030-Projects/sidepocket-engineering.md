---
title: "Sidepocket — Engineering Notes"
type: project
status: active
created: 2026-03-20
updated: 2026-04-06
tags: [project, sidepocket, engineering, nav, redis, s3, debugging, guidelines, ascend, mtm-simplification]
---

# Sidepocket — Engineering Notes

> Implementation details, formulas, recipes, and architecture notes. See [[sidepocket-infrastructure]] for project overview.

---

## Guidelines

### PR Descriptions
Keep PR descriptions short — just a 1-3 sentence summary of what was done. No headers, no root cause chains, no test plan checklists.

---

## Ascend API — MTM Simplification Research (TECH-3152)

### Max's Request (2026-04-06)
Reduce MTM complexity by moving to **1 sidepocket per account** and pulling account value directly from Ascend instead of calculating it in-house.

### What Ascend Exposes (from SDK model audit)

| Endpoint | SDK Module | Key Fields | Notes |
|---|---|---|---|
| `GET /cash-balances/v2/accounts/{account_id}:calculateCashBalance` | `cash_balances.calculate_cash_balance` | `open_liquidity_amount`, `open_balance_amount`, `available_cash_to_withdraw_amount` | **`open_liquidity_amount` = cash + all position values at market** — closest thing to total account MTM |
| `GET /ledger/v1/accounts/{account_id}/positions` | `ledger.list_positions` | `quantity`, `settled_quantity`, date | Position quantities only — no market value per position |
| `GET /ledger/v1/accounts/{account_id}/activities` | `ledger.list_activities` | Transaction-level ledger entries | Useful for transaction history / cash flows for Modified Dietz |
| `GET /ledger/v1/accounts/{account_id}/entries` | `ledger.list_entries` | Double-entry bookkeeping entries | Low-level |
| `GET /analytics/v1/snapshots` | `data_retrieval.list_snapshots` | `snapshot_type`, `process_date`, signed `download_uri` | Bulk file download (parquet/csv) — snapshot types include ACCOUNT_BALANCE, POSITIONS, CASH_ACTIVITY |

### Apex Support Ticket #1108677 — Confirmed 2026-04-23

**Humaira Zafar (Apex Solutions Engineering)** confirmed:

1. **Historical daily NLV**: Available via the **Balance file** in Ascend Standard Data (SFTP). Key field: `total_equity_amount` = total value of cash + positions. Delivered daily to Data Exchange folder. Also includes `position_market_value_amount`, buying power fields, trade/settle balances.
2. **Position-level market values**: Available via the **Positions file** — `settlement_date_market_value_amount` and `trade_date_market_value_amount` per asset per account.
3. **No pre-computed returns**: Confirmed — no TWR, cumulative %, or dollar return endpoint exists. We compute ourselves.

### Balance File — Key Fields for Return Metrics

| Field | Type | Use |
|-------|------|-----|
| `total_equity_amount` | DECIMAL(38,9) | **Daily NLV** — total cash + positions. This is our `accountValue` replacement. |
| `position_market_value_amount` | DECIMAL(38,9) | Net value of all positions |
| `cash_trade_balance_amount` | DECIMAL(38,9) | Trade date cash balance (cash accounts) |
| `total_trade_balance_amount` | DECIMAL(38,9) | Net trade date balance |
| `available_to_withdraw_amount` | DECIMAL(38,9) | Available to withdraw |
| `overnight_buying_power_issued_amount` | DECIMAL(38,9) | Buying power |
| `pending_transfers_amount` | DECIMAL(38,9) | Partially-processed transfers |
| `recent_deposits_amount` | DECIMAL(38,9) | Recent deposits (held 5 days) |

### Positions File — Key Fields

| Field | Type | Use |
|-------|------|-----|
| `trade_date_market_value_amount` | DECIMAL(38,9) | Market value on trade date |
| `settlement_date_market_value_amount` | DECIMAL(38,9) | Market value on settlement date |
| `trade_date_quantity` | DECIMAL(38,9) | Sum of settled + unsettled quantity |
| `settlement_date_quantity` | DECIMAL(38,9) | Settled-only quantity |
| `symbol` | VARCHAR(30) | Ticker |
| `cusip` | VARCHAR(12) | CUSIP identifier |

### Return Metrics Architecture (decided)

**Modified Dietz TWR** computed on our side:
- **Daily NLV**: `total_equity_amount` from Balance file (SFTP, daily)
- **Cash flows**: `ledger.list_activities` via SDK (deposits, withdrawals, dividends, fees)
- **Formula**: HPR = (ending_NLV - beginning_NLV - net_cash_flows) / (beginning_NLV + time-weighted cash flows)
- **Dollar return**: ending_NLV - total_net_deposits
- Chain daily HPRs for cumulative TWR

This replaces the current EXT982/EXT901/EXT981 file-based approach. `calc_daily_performance_vs_model` already does Modified Dietz — swap inputs to Balance file NLV + ledger activities.

### Data Delivery

Ascend Standard Data files delivered via **SFTP** to Data Exchange folder:
- Balance File (daily) — account-level NLV, buying power, balances
- Positions File (daily) — per-position market values, quantities
- Activities File (daily) — transaction-level ledger
- Also: Account Reference, Account Detail, Asset Reference, Tax Lot files
- Format: Parquet (via Snapshots endpoint) or flat files (via SFTP)

### What This Means for the Simplification
- `total_equity_amount` from Balance file replaces our complex `accountValue` formula (the one with `cum_pending_buy`, `total_allocation_dollars`, etc.)
- `open_liquidity_amount` from `calculateCashBalance` SDK call is the real-time equivalent
- Positions file gives us per-position market values directly — no more multiplying quantity * price ourselves
- Return metrics: we still compute, but inputs are much cleaner (single NLV field vs reconstructing from multiple EXT files)

---

## NAV / Account Value Formula (app-backend)

### `calc_live_account_balances` — `/liveUserAccountBalances`

```python
# cash_balance uses cum_complete_sell only (pending sells NOT included)
cash_balance = (cum_complete_deposit + abs(cum_complete_sell)
                - cum_complete_buy - abs(cum_complete_withdrawal)
                + dividends - fees + credits)

# TECH-3790 fix: subtract pending buys to avoid double-count
# (pending buy is in MTM immediately but cash not yet deducted)
accountValue = cash_balance - cum_pending_buy + total_allocation_dollars
```

### `calc_live_account_nav_time_series` — `/liveUserAccountNav`

```python
# TECH-3790 fix: include pending buys in net transactions
cum_complete_net_transactions = cum_complete_buy + cum_pending_buy + cum_complete_sell
account_value = cum_complete_net_amount + mtm - cum_complete_net_transactions
```

### Why pending sells don't need correction
- `cash_balance` does NOT include pending sell proceeds (only `cum_complete_sell`)
- MTM legitimately includes the SP position while sell is pending
- Self-corrects when sell completes → cash gains proceeds, MTM drops → neutral
- Brief inflation window covered by `ACCOUNT_BALANCE_UNSTABLE_{account}` Redis flag

### Verified with account 8JS09135
- `cum_pending_buy` = $1,174.87
- OLD accountValue = $274,848.08 (inflated)
- NEW accountValue = $273,673.21 (correct)

---

## Key Files

| File | Purpose |
|------|---------|
| `portfolio/portf_service_layer/sidepocket_holding_valuation.py` | MTM/NAV core logic |
| `app-backend/app_service_layer/handlers.py` | `calc_live_account_balances`, `calc_live_account_nav_time_series` |
| `app-backend/view/live_account.py` | `/liveUserAccountBalances`, `/liveUserAccountNav` endpoints |
| `util/cache/cache_utils.py` | `AccountingCacheHandler`, cash card values, transaction summary |
| `util/db/redis/RedisIO.py` | Redis wrapper (`get_df`, `mget_pattern_df`) |
| `cash/models/cash_transfer_model.py` | `ix_cash_transfer_account_number` index |
| `cash/models/fees_and_credits_model.py` | `ix_fees_and_credits_account_number` index |
| `cash/models/recurring_deposit_model.py` | recurring deposit; `check_for_start_date_in_the_future` |
| `portfolio/process/batch.py` | `daily_qc()`, `check_accounts_unstable()`, `set_account_balance_stability_status()` |
| `cash/plaid_service/plaid_service.py` | Plaid API wrapper — `get_identity()`, `get_balances()` |

---

## Account Instability Flag

- Key: `ACCOUNT_BALANCE_UNSTABLE_{account_number}` in Redis DB 0
- Set to `1` during batch processing, cleared after
- FE checks before displaying account values
- Covers the sell timing inflation window (brief period where sell completes in transaction cache but portfolio batch hasn't dropped MTM yet)

---

## Auth Service Gotcha

`auth/schema/query.py` has a module-level `from app import auth_conn`. Works fine in an activated interactive shell but fails with `conda run` because Python runs `app.py` as `__main__`, not `app`. When schema import triggers `from app import auth_conn`, Python re-imports `app.py` as a fresh module → circular import crash.

**Always start auth from a terminal with the alias:** `auth` then `python app.py`

---

## TECH-3783: Slow Lookup Endpoints — Root Causes & Fixes

| Root Cause | Fix |
|-----------|-----|
| `guid_for_account_number` (util) — loaded all account data from Redis per request | Added 5-min in-process TTL cache (`_guid_cache` dict) |
| `liveUserSidepocketList` (portfolio) — 6 Redis calls per SP (N+1) | `prefetch_sp_card_data()` — single `mget` before loop |
| `cashActivity` (cash) — sequential DB queries, no index on `account_number` | Added `Index('ix_*_account_number')` via `__table_args__` |
| `RedisIO.get_df` — redundant `exists()` call before every `get()` (2 hops → 1) | Removed `exists()` pre-check |

**Pending:** `alembic upgrade head` on cash service (dev + prod) to create the two DB indexes.

---

## Redis

### Dev Redis
- Host: `sidepocket-ac-dev.tlpebq.ng.0001.use1.cache.amazonaws.com`
- Limit: 384MB
- DB 0: main cache (MTM, NAV, cash, transactions, security master)
- DB 1: JWT/auth (revocation, rate limiting, temp tokens) → moving to DynamoDB (TECH-3832)

### Key Patterns (lowercase)
```
{P}.{sp_id}.sidepocket_mtm          # NAV, 1D, 1W, 1M, 6M, 1Y, 3Y, MAX, DAILY
{P}.{sp_id}.holding_mtm
cash_balance_snapshot
cash_balance_time_series
trade_transaction_sidepocket_snapshot.{sp_id}
trade_transaction_time_series.{sp_id}
trade_transaction_account_snapshot.{acct}
trade_transaction_by_account_time_series.{acct}
ACCOUNT_BALANCE_UNSTABLE_{account}
security_master_table
```

### Memory check
`_cache_by_period_and_sp` skips caching if `used_memory / maxmemory > 0.95`. NAV phase runs last → most likely skipped when memory is tight. Cache `sidepocket_mtm` before `holding_mtm` to prioritize NAV.

---

## Redis Scan Recipes

### Find accounts with pending orders
```python
import redis, pickle, pandas as pd
r = redis.Redis(host='sidepocket-ac-dev.tlpebq.ng.0001.use1.cache.amazonaws.com', port=6379, db=0)
for key in r.keys('trade_transaction_account_snapshot.*'):
    df = pickle.loads(r.get(key))
    pending_buy = float(df['cum_pending_buy'].iloc[0])
    pending_sell = float(df['cum_pending_sell'].iloc[0])
    if pending_buy > 0 or pending_sell != 0:
        print(df['account_number'].iloc[0], pending_buy, pending_sell)
```

### Check Redis memory
```bash
redis-cli -h sidepocket-ac-dev.tlpebq.ng.0001.use1.cache.amazonaws.com INFO memory | grep used_memory_human
```

### Check keys for a sidepocket
```bash
redis-cli -h sidepocket-ac-dev.tlpebq.ng.0001.use1.cache.amazonaws.com KEYS "*<sp_id>*"
```

### Hit app-backend locally
```bash
JWT=$(cat /tmp/jwt.txt | tr -d '\n')
curl -s -H "Authorization: Bearer $JWT" "http://localhost:4003/liveUserAccountBalances?accountNumber=8JS09135"
curl -s -H "Authorization: Bearer $JWT" "http://localhost:4003/liveUserAccountNav?accountNumber=8JS09135&timezone=UTC"
```

---

## S3 Parquet Schema (TECH-3828)

### Path Convention
```
s3://sidepocket-cache-{env}/{category}/{entity_id}/{key}.parquet
```
- `env`: `dev` | `prod`
- `entity_id`: account number, sidepocket guid, or `global`
- **Bucket:** `market-data-cache-dev` (dev), `sidepocket-cache-prod` (prod)

### Redis Key → S3 Path Mapping

| Redis Key Pattern | S3 Path | Writer | Readers |
|---|---|---|---|
| `{P}.{sp_id}.sidepocket_mtm` | `sidepocket_mtm/{sp_id}/{P}.parquet` | portfolio/sidepocket_holding_valuation.py | cache_utils, portfolio/handlers.py |
| `{P}.{sp_id}.holding_mtm` | `holding_mtm/{sp_id}/{P}.parquet` | portfolio/sidepocket_holding_valuation.py | sidepocket_holding_valuation.py, handlers.py |
| `cash_balance_snapshot` | `cash_balance/global/snapshot.parquet` | cash/cash_balances.py | cache_utils |
| `cash_balance_time_series` | `cash_balance/global/time_series.parquet` | cash/cash_balances.py | cache_utils |
| `trade_transaction_sidepocket_snapshot.{sp_id}` | `transaction_sidepocket/{sp_id}/snapshot.parquet` | portfolio/transaction_summary.py | cache_utils |
| `trade_transaction_time_series.{sp_id}` | `transaction_sidepocket/{sp_id}/time_series.parquet` | portfolio/transaction_summary.py | cache_utils |
| `trade_transaction_account_snapshot.{acct}` | `transaction_account/{acct}/snapshot.parquet` | portfolio/transaction_summary.py | cache_utils |
| `trade_transaction_by_account_time_series.{acct}` | `transaction_account/{acct}/time_series.parquet` | portfolio/transaction_summary.py | — |
| `account_balance_unstable_{acct}` | `stability_flags/global/flags.parquet` | portfolio/process/batch.py | app-backend |
| `security_master_table` | `market_data/global/security_master.parquet` | portfolio/process/__init__.py | holdings processing |

**Periods (P):** `NAV`, `1D`, `1W`, `1M`, `6M`, `1Y`, `3Y`, `MAX`, `DAILY`

### Parquet Column Schemas

**sidepocket_mtm**: `id_user_sidepocket` (str), `id_model_sidepocket` (str), `account_number` (str), `guid_user` (str), `date` (date), `mtm` (f64), `weight` (f64), `dollar_return` (f64), `percent_return` (f64), `weighted_period_return` (f64), `cum_dollar_return` (f64), `cum_percent_return` (f64)

**holding_mtm**: `id` (i64), `id_user_sidepocket` (str), `id_model_sidepocket` (str), `account_number` (str), `guid_user` (str), `entry_datetime` (ts), `exit_datetime` (ts, nullable), `symbol` (str), `quantity` (f64), `date` (date), `close` (f64), `mtm` (f64), `dollar_return` (f64), `percent_return` (f64), `weight` (f64), `weighted_period_return` (f64), `entry_reason` (str, nullable), `parent_holding_id` (i64, nullable)

**cash_balance_snapshot/time_series**: `account_number` (str), `guid_user` (str), `trade_date` (date), `complete_deposit` (f64), `complete_withdrawal` (f64), `pending_deposit` (f64), `pending_withdrawal` (f64), `settled_deposit` (f64), cumulative versions of all, `dividends_and_interest` (f64), `margin_cost` (f64), `fees` (f64), `credits` (f64)

**transaction_sidepocket snapshot/time_series**: `trade_date` (date), `guid_user` (str), `account_number` (str), `id_user_sidepocket` (str), `apex_order_id` (str), `complete_buy/sell` (f64), `pending_buy/sell` (f64), cumulative versions, `settled_buy/sell` (f64), cumulative settled

**transaction_account snapshot/time_series**: Same minus `id_user_sidepocket` and `apex_order_id`

**stability_flags**: `account_number` (str), `unstable` (i8: 0 or 1), `updated_at` (ts)

**security_master**: `cusip` (str), `symbol` (str)

### S3 Bucket Configuration

`CACHE_S3_BUCKET` env var — defaults to `market-data-cache-{ENVIRONMENT}`:
- Dev default: `market-data-cache-dev`
- Prod: set `CACHE_S3_BUCKET=market-data-cache-prod` in ECS task definition
- Applies to both `S3ParquetWriter` (writer) and `InMemoryStore` (cache service reader)
- Commit: `9cdd225` on TECH-3826 branch (2026-03-20)

### Keys NOT Migrated to S3
- `{P}.{id}.security_metrics` — market data Redis instance, separate pipeline
- `{P}.{id}.model_metrics` — market data Redis instance, separate pipeline
- `account_numbers` — small list, low-frequency
- DB 1 keys (JWT, rate limiting, temp tokens) — DynamoDB via TECH-3832

---

## Plaid ACH Architecture Insight

Our ACH transfers don't depend on Plaid after initial setup — deposits/withdrawals go through Apex directly via `apex_rel_id`. Plaid token only needed for:
1. Initial bank link
2. Balance checks before transfer
3. Re-establishing a cancelled ACH relationship

**Practical optimization (TECH-3792 context):** Swap pre-transfer balance check from `plaid.get_balance()` to `get_apex_cash_balance()` (exists in `cash/cash_process/apex_cash_api.py`). Removes main ongoing Plaid dependency for existing users.

### Plaid Error Structure
```python
# ApiException.body is a JSON string:
{
    "error_type": "ITEM_ERROR",
    "error_code": "ITEM_LOGIN_REQUIRED",
    "error_message": "...",
    "display_message": "...",
    "causes": [{"error_type": "...", "error_code": "OAUTH_INVALID_TOKEN", ...}]
}
```

---

## Dev Server SSH Access (dev-ubuntu)

- **Server:** `dev-ubuntu`, private IP `172.31.1.203`, user `ubuntu`
- **Credentials:** distributed via 1Password (Max sends invite)
- **Setup:**
  ```bash
  # Save private key from 1Password
  nano ~/.ssh/sp-dev.pem
  chmod 600 ~/.ssh/sp-dev.pem
  ```
  Add to `~/.ssh/config`:
  ```
  Host dev-ubuntu
    HostName 172.31.1.203
    User ubuntu
    IdentityFile ~/.ssh/sp-dev.pem
  ```
  Then just `ssh dev-ubuntu`.
- **Deploying Alembic migrations to dev:**
  ```bash
  # Copy migration file to server
  scp alembic/versions/your_migration.py ubuntu@172.31.1.203:/home/ubuntu/code/cash/alembic/versions/
  # Verify down_revision = 'c3d4e5f6a7b8' (current HEAD on server), then:
  ssh dev-ubuntu
  cd /home/ubuntu/code/cash && cash && alembic upgrade head
  ```
- **TODO:** Write Confluence SSH guide for the team (promised to Sam 2026-03-24)

---

## Code Review Lessons

### Rigor standard: think like an attacker, not just a flow verifier

Checking that the happy path and error paths return the right things is not enough. The bar is the highest possible.

**The PR #194 miss (WebAuthn login, May 2026)**
Yves caught a user enumeration vulnerability that slipped through Daniel's approval. The login begin endpoint returned "Invalid credentials" for non-existent users, which looked safe. But a successful 200 response with credential IDs implicitly confirms the user exists. That distinction requires thinking from an attacker's perspective, not just asking "does the error handling look correct?"

Also missed: direct `sys.modules` modification in test code, which Yves had already flagged in a previous review. Known repeat patterns should be on the checklist.

**Questions to ask on every auth/security PR**
- Does a successful response leak whether a user/resource exists?
- Do unauthenticated endpoints reveal anything about internal state?
- What does each possible response (200, 400, 401, 404) tell an attacker?
- Are constants that appear in multiple places (e.g. `MAX_LOGIN_ATTEMPTS`) centralized or hardcoded at every callsite?
- Have patterns flagged in previous reviews on this codebase been repeated here?

---

## Debugging Recipes

### Connect to dev DB
```bash
psql -h database-1.cluster-cebswxepgbru.us-east-1.rds.amazonaws.com -U sidepocket -d <dbname>
```

### Verify NAV endpoint
```
GET https://portfoliodev.sidepocket.com/api/v1/sidepocket/<sp_id>/nav
```

### Run MTM manually (Python)
```python
id_user_sidepocket = 'a4aee071-b8c0-42b9-9577-0c30d784d711'
MarkToMarketHandler().intraday_mark_to_market(id_user_sidepocket)
MarkToMarketHandler().eod_mark_to_market(id_user_sidepocket)
```

---

## Known Open Issues

- **guid_user DatatypeMismatch (CRITICAL, active since Apr 17)**: `cash-prod-5.97`, 2,462+ Sentry events and rising daily. Root cause: `.fillna(0.0)` after outer merges fills UUID `guid_user` with `0.0` in `process_cash_balance_for_account_and_date`. PR #262 ready but Max flagged ffill/bfill concern on Apr 22 — must address review before deploy.
- **`datetime.now()` schema bug (TECH-3879, deprioritized)**: UAT DB patched Apr 2. Prod still rolled back. No discussion since early April.
- **Sell NAV timing inflation**: Sell completing in transaction cache before portfolio batch drops MTM → brief NAV inflation by sell amount. Self-correcting, covered by instability flag. Needs its own ticket.
- **Tax feature (pending ticket)**: Max wants full bank transaction pull for tax purposes. Hard constraints: no re-auth, no credential storage. Technically impossible with any OAuth aggregator. Three options presented; awaiting Max's decision.
- **TECH-3783 deploy**: `alembic upgrade head` on cash service still needed (dev + prod) to create DB indexes.
- **TECH-3792 deploy**: Register Plaid webhook URL in Dashboard (sandbox + prod), frontend re-auth prompt, prod alembic migration (`c3d4e5f6a7b8`).
- **Plaid RATE_LIMIT_EXCEEDED (IDENTITY_LIMIT)**: 435 Sentry events escalating since ~Apr 7. Related to pre-transfer balance checks.
- **InvalidHeader: Authorization**: 1,087 events since Dec 2025, still firing on cash-prod.

---

## Ascend Migration Progress (TECH-3152) — Updated 2026-04-23

Completed this sprint (Apr 15-18):

| Ticket | PR | Description |
|--------|-----|-------------|
| TECH-3153 | util #210 | `get_ascend_sdk()` factory + `AscendToken` JWT signing |
| TECH-3155 | util #211 | `get_ascend_cash_balance_details()` + `get_ascend_snapshot_data()`, 9 tests |
| TECH-3154 | portfolio #364 | SOD download → `list_snapshots()` behind `USE_ASCEND`, 6 tests |
| TECH-3160 | portfolio #365 | Buying power + pre-trade validation → Ascend, 9 tests |

Return metrics: no pre-computed TWR in SDK. Recommended Modified Dietz from `list_snapshots(ACCOUNT_BALANCE)` + `ledger.list_activities`. Apex support ticket open.

Next: TECH-3162 (order placement + cancellation), merge PRs once reviewed, deploy guid_user fix.
