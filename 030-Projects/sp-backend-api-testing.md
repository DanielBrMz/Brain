---
title: "sp-backend-api-testing"
type: project
status: active
created: 2026-03-19
updated: 2026-03-22
tags: [project, sidepocket, testing, cypress, e2e]
---

# sp-backend-api-testing

> Cypress-based end-to-end testing suite for the Sidepocket backend API.

## Overview

| Field | Value |
|-------|-------|
| **Path** | `~/Documents/Projects/Personal/sp-backend-api-testing/` |
| **Purpose** | E2E API testing against sp-app backend |
| **Status** | Active |
| **Stack** | Cypress 13.13.2, JavaScript |

## Test Coverage

| Suite | What It Tests |
|-------|---------------|
| Accounts | Applications, account lookups |
| Auth/Login | Authentication flows |
| Billing | Subscriptions, endorser relationships |
| Cash | Transfers and deposits |
| Portfolio | Portfolio management |
| App Features | Market data, holdings |

## Commands

```bash
cd ~/Documents/Projects/Personal/sp-backend-api-testing

# Interactive
npm run cy:open-dev       # Cypress UI (dev env)
npm run cy:open-prod      # Cypress UI (prod env)

# Headless
npm run cy:run-dev        # Run GET tests (dev)
npm run cy:run-prod       # Run GET tests (prod)
npm run cy:run-dev-full-test  # All tests including mutations
```

## Structure

- Test data managed via fixtures and utilities
- Dual-environment support: dev and prod
- Docker container support for headless CI testing
- Test results analyzed by `Support/analysis/cypress/cypress_analyzer.py`

## Related

- [[sidepocket-backend|Sidepocket Backend (sp-app)]]
- [[sidepocket-webapp|Sidepocket Webapp]]
- [[support-project|Support Toolkit]] -- cypress_analyzer.py for failure analysis
- [[sidepocket-codebase|Codebase]]
