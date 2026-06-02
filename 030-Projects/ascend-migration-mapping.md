# Ascend Migration Mapping — Cash Service (TECH-3152)

> Every `apex_*` call in the cash service and its `ascend_*` replacement.

---

## Core API Functions (in `apex_api_util/__init__.py`)

| Legacy (Apex) | Replacement (Ascend) | Status |
|---|---|---|
| `submit_to_apex(base_url, path, json)` | `submit_to_ascend(base_url, path, json)` | ✅ Implemented |
| `get_from_apex(base_url, path)` | `get_from_ascend(base_url, path)` | ✅ Implemented |
| `put_to_apex(base_url, path, json)` | `put_to_ascend(base_url, path, json)` | ✅ Implemented |
| `get_apex_ale_messages(base_url, topic, ...)` | `get_ascend_ale_messages(base_url, topic, ...)` | ✅ Implemented |
| `post_doc_apex(base_url, path, payload, files)` | `post_doc_ascend(base_url, path, payload, files)` | ✅ Implemented |

---

## Environment Variables to Change

| Legacy | Ascend Replacement | Source |
|---|---|---|
| `APEX_BASE_URL` (via `app.config`) | `ASCEND_BASE_URL` | Ascend developer portal |
| `APEX_API_ENTITY` (correspondent code) | `ASCEND_CORRESPONDENT_CODE` | Ascend portal |
| `APEX_ACH_RELATIONSHIP_TOPIC` | Same topic name (verify) | ALE config |
| `APEX_TRANSFER_TOPIC` | Same topic name (verify) | ALE config |
| `APEX_ACATS_TOPIC` | Same topic name (verify) | ALE config |
| — | `ASCEND_API_KEY` | Ascend portal (NEW) |
| — | `ASCEND_PRIVATE_KEY` | RSA PEM from Ascend (NEW) |
| — | `ASCEND_SERVICE_ACCOUNT_NAME` | Ascend portal (NEW) |
| — | `ASCEND_ORGANIZATION` | Ascend portal (NEW) |
| — | `ASCEND_SERVER` | "uat" / "prod" / "sbx" (NEW) |

---

## File-by-File Migration Map

### `cash_process/apex_cash_api.py` — MAIN FILE (20+ Apex calls)

| Function | Apex Call | URL Path | Action |
|---|---|---|---|
| `create_withdrawal()` | `submit_to_apex` | `/sentinel2/api/v1/transfers/achs/withdrawals` | Create ACH withdrawal |
| `create_deposit()` | `submit_to_apex` | `/sentinel2/api/v1/transfers/achs/deposits` | Create ACH deposit |
| `create_ach_relationship()` | `submit_to_apex` | `/sentinel2-counterparty/api/v1/ach_relationships` | Create ACH relationship |
| `create_recurring_deposit()` | `submit_to_apex` | `/scheduled-transfers/api/v1/schedules/achs/deposits` | Create recurring deposit |
| `list_recurring_deposits()` | `get_from_apex` | `/scheduled-transfers/api/v1/schedules/achs?accountNumber=...` | List recurring deposits |
| `change_recurring_deposit_amount()` | `put_to_apex` | `/scheduled-transfers/api/v1/schedules/achs/deposits/{id}/update` | Update recurring amount |
| `cancel_recurring_deposit()` | `put_to_apex` | `/scheduled-transfers/api/v1/schedules/achs/deposits/{id}/cancel` | Cancel recurring deposit |
| `get_apex_ach_relationship()` | `get_from_apex` | `/sentinel2-counterparty/api/v1/ach_relationships/{id}` | Get ACH rel status |
| `list_ach_relationships()` | `get_from_apex` | `/sentinel2-counterparty/api/v1/ach_relationships?account=...&status=...` | List ACH rels |
| `cancel_ach_relationship()` | `submit_to_apex` | `/sentinel2-counterparty/api/v1/ach_relationships/{id}/cancel` | Cancel ACH rel |
| `get_apex_cash_balance()` | `get_from_apex` | `/cash-balances/api/v2/available/{account}` | Get cash balance |
| `get_ira_constraints_account()` | `get_from_apex` | `/sentinel2/api/v1/ira_constraints/{account}/{method}/{direction}` | IRA constraints |
| `get_ira_constraints_source_destination_accounts()` | `get_from_apex` | `/sentinel2/api/v1/ira_constraints/{src}/{dst}` | IRA src/dst constraints |
| `get_apex_ach_relationship_events()` | `get_apex_ale_messages` | ALE topic: `APEX_ACH_RELATIONSHIP_TOPIC` | Poll ACH rel events |
| `get_apex_transfer_events()` | `get_apex_ale_messages` | ALE topic: `APEX_TRANSFER_TOPIC` | Poll transfer events |
| `check_account_good_standing()` | `get_from_apex` | `/atlas/api/v1/accounts/{account}` | Check account active |
| `get_account_info()` | `get_from_apex` | `/atlas/api/v1/accounts/{account}` | Get account info |
| `update_ach_relationships_with_plaid_data()` | `put_to_apex` | `/sentinel2-counterparty/api/v1/ach_relationships/{id}/update_plaid` | Update Plaid data |
| `get_acats_ales()` | `get_apex_ale_messages` | ALE topic: `APEX_ACATS_TOPIC` | Poll ACATS events |
| `cash_recon()` | reads SOD files | Uses `APEX_BASE_URL` for env detection | Cash reconciliation |

### `cash_process/ach_relationship_api.py`
- Imports from `apex_cash_api`: `get_apex_ach_relationship`, `cancel_ach_relationship`, `create_ach_relationship`
- No direct Apex calls — will work once `apex_cash_api.py` is migrated

### `cash_process/process_cash_transfers.py`
- Imports: `get_apex_ale_messages`, `get_from_apex` directly
- Imports: `apex_cash_api` module (uses `apex_cash_api.create_deposit`, `apex_cash_api.create_withdrawal`, etc.)
- Has its own ALE polling logic

### `cash_service_layer/handlers.py`
- Uses `apex_cash_api` functions indirectly through imports

### `views/` — Flask route handlers
- `ach_relationship.py` — uses `ach_relationship_api` (indirect)
- `ach_transfer_deposits.py` — uses `apex_cash_api.create_deposit`
- `ach_transfer_withdrawals.py` — uses `apex_cash_api.create_withdrawal`
- `recurring_deposits.py` — uses `apex_cash_api` recurring functions
- `cash_balances_api.py` — uses `apex_cash_api.get_apex_cash_balance`
- `cash_events_api.py` — references `ascend` (already partially migrated?)
- `ira_constraints.py` — uses `apex_cash_api.get_ira_constraints_*`

### `models/` — Data models
- Reference Apex-specific field names but don't make API calls directly

### `test/` — Tests
- `test_ach_relationship.py`, `test_apex.py`, `test_cash_activity.py`, etc.
- Will need mocked Ascend responses

---

## Migration Strategy

**Phase 1: Feature Flag Routing** (can do NOW without credentials)
- Add `USE_ASCEND = os.environ.get("USE_ASCEND", "false").lower() == "true"`
- In `apex_cash_api.py`, create wrapper functions that route to apex_* or ascend_* based on flag
- All URL paths stay the same (Ascend maintains same REST API paths)

**Phase 2: Auth Configuration** (BLOCKED — needs credentials from Max)
- Set ASCEND_* env vars on dev-ubuntu and UAT
- Test auth token generation
- Verify API responses match expected format

**Phase 3: Integration Testing** (after Phase 2)
- Test each endpoint with real Ascend API
- Verify ALE message format compatibility
- Run cash reconciliation against Ascend data

---

## BLOCKER

**No ASCEND_* environment variables are configured on dev-ubuntu.** Need from Max/Ascend portal:
- `ASCEND_API_KEY`
- `ASCEND_PRIVATE_KEY` (RSA PEM)
- `ASCEND_SERVICE_ACCOUNT_NAME`
- `ASCEND_ORGANIZATION`
- `ASCEND_SERVER`
- `ASCEND_CORRESPONDENT_CODE`
