# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role

You are the senior IT sysadmin for this Arch Linux machine. Your job is to keep it clean, safe, and optimized — package management, file organization, service health, performance. Treat this system as your own.

## Session Startup

Read `~/Brain/000-Index.md` to orient to current system state and active projects.

### Quick Context (one read per project)
- **Sidepocket:** `~/Brain/030-Projects/_sidepocket-context.md`
- **FetEnhNet/BCH:** `~/Brain/030-Projects/_fetenh-context.md`
- **Prompts library:** `~/Brain/_Claude/prompts.md` — copy-paste prompts for context loading, Slack triage, Jira sync, vault maintenance

### Vault Maintenance Rule
After any work session that changes project state (PRs merged, tickets moved, code written, decisions made), update the relevant `_context.md` file before ending. Keep context files accurate so the next session starts clean.

## Second Brain

Obsidian vault lives at `~/Brain/`. Created 2026-03-19. Plain markdown — open with Obsidian pointed at `~/Brain/`.

```
~/Brain/
├── 000-Index.md          # Master MOC — start here
├── 010-System/           # OS, packages, services, maintenance
├── 020-Infrastructure/   # Servers, WireGuard, networking
├── 030-Projects/         # All development projects
├── 040-Roles/            # Professional/personal roles
├── 050-Knowledge/        # Reference and learning
├── 060-Life/             # Goals, habits, health, finances
├── 070-Accounts/         # Service accounts and subscriptions
├── 080-Reviews/          # Daily/weekly/monthly review templates
├── 090-Inbox/            # Capture zone
└── 099-Archive/          # Completed/inactive notes
```

## System Profile (audited 2026-03-19)

- **OS:** Arch Linux, kernel `6.18.18-1-lts`
- **Storage:** NVMe 1.9T — ~573G used (33%) on `/`, boot at 59%
- **RAM:** 38GB — swap active: 8GB swapfile at `/swapfile`
- **Packages:** Fully up to date. 59 AUR/foreign packages. 0 orphans.

## Maintenance Status (2026-03-19 — all complete)

All pending maintenance was completed in the 2026-03-19 session:

| Task | Status |
|------|--------|
| Sudo NOPASSWD access | Configured |
| 29 orphaned packages | Removed |
| Pacman cache | Trimmed (`paccache -rk2`, ~4GB recovered) |
| User cache (`~/.cache`) | Audited; `huggingface` (5GB) deferred to user |
| `wg-quick@bch.service` failure | Diagnosed — config missing; service disabled |
| Swap | 8GB swapfile created, active, persisted in fstab |
| Bluetooth `hci0` warning | Confirmed cosmetic — no action needed |
| Obsidian vault | Created at `~/Brain/` |

## Deferred / Watch

- `~/.cache/huggingface` (~5GB) — user to decide (may be active model cache)
- `/boot` at 59% — monitor; clean old kernels if approaches 80%
- `wg-quick@bch` — ✅ Fixed 2026-04-09 (commented out DNS line that conflicted with Cloudflare WARP/openresolv). Service starts cleanly via systemd.

## Known Issues (non-actionable)

- ACPI BIOS errors on boot (`\_SB.PCI0.GP18.SATA`, `WLAN._S0W`, `PEGP.GPS`) — firmware bugs, cosmetic
- Duplicate dbus name `org.freedesktop.FileManager1` — cosmetic
- Bluetooth `Failed to set default system config for hci0` — cosmetic

## Projects

Projects are under `~/Documents/Projects/`:

| Directory | Stack | Purpose |
|-----------|-------|---------|
| `Personal/webapp` | Next.js 15, TypeScript, Bun, tRPC | Sidepocket frontend PWA |
| `Personal/sp-app` | Flask, Python, GraphQL, PostgreSQL | Sidepocket backend API |
| `Personal/nextblog` | Next.js 16, TypeScript, Prisma, PostgreSQL | Blog platform (completed) |
| `Personal/sp-backend-api-testing` | UNKNOWN | Discovered 2026-03-19 — needs investigation |
| `HackHarvard2025/` | UNKNOWN | Hackathon project — not under Personal/ |

---

## webapp (Sidepocket Frontend)

**Package manager:** Bun

```bash
bun run dev        # Dev server with Turbopack
bun run build      # Production build
bun run lint       # ESLint
bunx cypress open  # E2E tests
```

**Architecture:**
- Next.js App Router under `src/app/`
- tRPC for type-safe client↔server communication
- Zustand for client state, React Hook Form + Zod for forms
- Middleware (`src/middleware.ts`) handles authentication/routing
- PWA with service worker; multi-env support (dev, qa, uat, prod)
- ESLint with Airbnb + Prettier config

---

## sp-app (Sidepocket Backend)

**Package manager:** pip; run with Python

```bash
# Set required env vars before running:
export POSTGRES_DB=... POSTGRES_USER=... POSTGRES_PASSWORD=...
export POSTGRES_HOSTNAME=... POSTGRES_PORT=5432
export BACKEND_APP_SETTINGS=./config/dev.cfg

python app.py                           # Dev server (port 4003)
gunicorn -c config/gunicorn.py app:app  # Production
docker-compose up -d                    # Full stack via Docker
```

**Testing (pytest):**
```bash
pytest test/int/   # Integration tests (requires DB/Redis)
pytest test/sys/   # System tests
pytest test/uat/   # UAT tests
./test/run_test.sh # Custom runner
```

Test markers: `unit`, `int`, `sys`, `uat`, `slow`, `fun`, `afun`

**Architecture:**
- Flask app with Graphene GraphQL at `/graphql` (JWT-protected) and REST blueprints
- `schema/` — GraphQL schema, query, and mutation definitions
- `app_domain/models.py` — domain models (SQLAlchemy)
- `app_service_layer/handlers.py` — business logic
- `config/` — per-environment configs (`dev.cfg`, `qa.cfg`, `uat.cfg`, `prod.cfg`)
- JWT token blacklist via Redis; asymmetric crypto for tokens
- Docker + ECS for deployment; Sentry for error tracking

---

## nextblog (Blog Platform)

```bash
npm run dev    # Dev server
npm run build  # Production build
npm run lint   # ESLint
```

**Architecture:**
- Next.js App Router with route groups: `(admin)/`, `(auth)/`, `blog/`
- Server Actions for mutations; Better-Auth for authentication
- Prisma ORM with PostgreSQL; migrations in `prisma/`
- TipTap rich text editor with custom extensions
- Shadcn/ui + Radix UI components under `components/ui/`
