---
title: "Sidepocket — Webapp (Frontend)"
type: project
status: active
created: 2026-03-19
updated: 2026-03-19
tags: [project, sidepocket, nextjs, typescript, frontend]
---

# Sidepocket — Webapp (Frontend)

## Overview

| Field | Value |
|-------|-------|
| **Path** | `~/Documents/Projects/Personal/webapp/` |
| **Purpose** | Sidepocket frontend PWA |
| **Status** | Active |
| **Package manager** | Bun |

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Package manager | Bun |
| API communication | tRPC (type-safe client↔server) |
| State management | Zustand |
| Forms | React Hook Form + Zod |
| Styling | Tailwind CSS 3.4 + NextUI 2.4 (Radix UI) + Emotion, tailwindcss-animate/motion |
| Testing | Cypress (E2E) |
| Linting | ESLint (Airbnb + Prettier) |
| Deployment | PWA; multi-env (dev, qa, uat, prod) |

## Commands

```bash
cd ~/Documents/Projects/Personal/webapp

bun run dev        # Dev server with Turbopack
bun run build      # Production build
bun run lint       # ESLint
bunx cypress open  # E2E tests
```

## Architecture

```
src/
├── app/               # Next.js App Router — pages and layouts
├── middleware.ts      # Auth/routing middleware
└── ...
```

- **Routing:** Next.js App Router under `src/app/`
- **Auth:** Handled via `src/middleware.ts` — authentication and route protection
- **API:** tRPC for type-safe communication with the backend
- **State:** Zustand for client-side global state
- **Forms:** React Hook Form with Zod schema validation
- **PWA:** Service worker configured; multi-environment support

## Environment

Multi-env support: `dev`, `qa`, `uat`, `prod`

```bash
# Check env files
ls .env* ~/Documents/Projects/Personal/webapp/
```

## Related

- [[sidepocket-backend]] — Flask/GraphQL API this app talks to
- [[sp-backend-api-testing]] — testing repository

## Notes

- **TECH-3843** (current branch): Staging BE URL fix + feature flag component
- **TECH-3826-upgrade**: Stack upgrade (syncing with development)
