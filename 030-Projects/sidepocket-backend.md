---
title: "Sidepocket — Backend API"
type: project
status: active
created: 2026-03-19
updated: 2026-03-19
tags: [project, sidepocket, flask, graphql, postgresql, backend]
---

# Sidepocket — Backend API (sp-app)

## Overview

| Field | Value |
|-------|-------|
| **Path** | `~/Documents/Projects/Personal/sp-app/` |
| **Purpose** | Sidepocket backend API |
| **Status** | Active |
| **Package manager** | pip |

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask |
| Language | Python |
| API | Graphene GraphQL (`/graphql`) |
| REST | Blueprints for additional endpoints |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Cache / Auth | Redis (JWT blacklist) |
| Auth | JWT (asymmetric crypto) |
| Error tracking | Sentry |
| Deployment | Docker + AWS ECS |
| Testing | pytest |

## Commands

```bash
cd ~/Documents/Projects/Personal/sp-app

# Required env vars
export POSTGRES_DB=...
export POSTGRES_USER=...
export POSTGRES_PASSWORD=...
export POSTGRES_HOSTNAME=...
export POSTGRES_PORT=5432
export BACKEND_APP_SETTINGS=./config/dev.cfg

python app.py                           # Dev server (port 4003)
gunicorn -c config/gunicorn.py app:app  # Production

docker-compose up -d                    # Full stack via Docker
```

## Testing

```bash
pytest test/int/   # Integration tests (requires DB + Redis)
pytest test/sys/   # System tests
pytest test/uat/   # UAT tests
./test/run_test.sh # Custom test runner
```

**Test markers:** `unit`, `int`, `sys`, `uat`, `slow`, `fun`, `afun`

## Architecture

```
sp-app/
├── app.py                      # Entry point
├── schema/                     # GraphQL schema, queries, mutations
├── app_domain/
│   └── models.py               # SQLAlchemy domain models
├── app_service_layer/
│   └── handlers.py             # Business logic
├── config/
│   ├── dev.cfg
│   ├── qa.cfg
│   ├── uat.cfg
│   ├── prod.cfg
│   └── gunicorn.py
└── test/
    ├── int/
    ├── sys/
    └── uat/
```

- **GraphQL:** Graphene at `/graphql` — JWT-protected
- **REST:** Flask blueprints for additional endpoints
- **Auth:** JWT with asymmetric crypto; Redis blacklist for token revocation
- **DB:** SQLAlchemy models in `app_domain/models.py`
- **Business logic:** `app_service_layer/handlers.py`
- **Config:** Per-environment configs in `config/`

## Environments

| Env | Config file |
|-----|------------|
| dev | `./config/dev.cfg` |
| qa | `./config/qa.cfg` |
| uat | `./config/uat.cfg` |
| prod | `./config/prod.cfg` |

## Deployment

- Docker + ECS for production deployment
- `docker-compose.yml` for local full-stack development

## Related

- [[sidepocket-webapp]] — Next.js frontend
- [[sp-backend-api-testing]] — testing repository
- [[../020-Infrastructure/servers-index|Servers]] — ECS/deployment details

## Notes

- **TECH-3826** (current branch): Python package upgrades -- Flask, gunicorn, psycopg2, celery, redis, graphene (downgraded to 2.x for compat), SQLAlchemy
- **Redis to S3 Parquet migration**: Architecting columnar storage to replace ElastiCache
