---
title: "Monday Queue — 2026-04-28"
type: project
status: active
created: 2026-04-25
updated: 2026-04-28
tags: [sidepocket, queue, ascend]
---

# Monday Queue — 2026-04-28

## 1. ~~Open Apex Solutions Engineering Request — Account-Level TWR~~ DONE

Reply drafted for existing ticket #1108677 with Humaira. Asking if Ascend can compute TWR at account level factoring in deposits/withdrawals. User to post reply on portal.

## 2. ~~Ask Max: Fees/Credits Source of Truth (TECH-3158)~~ RESOLVED

Asked Max — he confirmed fees/credits already flow through Apex via sentinel2 journal entries (`journal_fee_to_corporate_account` / `credit_client_account`). Ascend's balance will already reflect them. TECH-3158 just needs the sentinel2 endpoints migrated to Ascend equivalent, same pattern as other tickets.

## 3. ~~Ask Max: Scheduled Transfers Migration (TECH-3161)~~ SENT

Sent alongside #2. Awaiting Max's reply on whether to consolidate with Ascend's ScheduleTransfers API.

## 4. ~~Ping Tomasz: ECS Security Group Rules~~ SENT

Sent Apr 28. Awaiting Tomasz.

## 5. ~~Follow Up: TECH-3162 PR Reviews~~ IN PROGRESS

Max reviewed util #213 — 3 comments:
1. ~~Fractional orders missing~~ — Fixed: added `quantity_type` param (NOTIONAL/FRACTIONAL) to `place_ascend_order`. Pushed ca7245b.
2. ~~Randomized tests for Modified Dietz~~ — Fixed: added `TestModifiedDietzRandomized` with 300+ seeded random scenarios. Same commit.
3. "Can you see this?" — visibility test, no action needed.

Also fixed in earlier commit (c77c0a6): deduplicated `_build_account_id`, fixed snapshot date range bug, added pagination to cash flows, WIRE withdrawal classification, UTC timezone, input mutation.

Portfolio #367 updated with `quantity_type` passthrough (923720b). App-backend #120 still awaiting Max's review. Asked Max about prod Ascend creds for return comparison.

## 6. Remaining Code Work

| Ticket | What | Blocked on |
|--------|------|------------|
| TECH-3157 | Investor docs migration (accounts service) | Nothing — can build |
| TECH-3159 | Cash transfers migration (cash service) | Nothing — can build |
| TECH-3156 | Account creation migration (accounts service) | Nothing — can build, biggest scope |
| TECH-3158 | Fees/credits — sentinel2 endpoint migration | Nothing — just swap endpoints |
| TECH-3161 | Scheduled transfers to Ascend | Max decision (#3 above) |

## 7. Other Items

- [x] Test Chema's auth PR #193 on EC2 — 24/24 WebAuthn tests pass, 6 pre-existing change_password failures (unrelated)
- [~] Build return comparisons for 8JS05086 — script built and validated. Max asked "do you need EXTs?" — pivot: can run Modified Dietz against same EXT data the current method uses (compare the math, not the data source). Need to ask Max where EXTs land (dev-ubuntu path or S3).
- [x] Update portfolio PR #367: `quantity_type` passthrough pushed (923720b)
