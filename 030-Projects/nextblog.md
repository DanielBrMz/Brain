---
title: "nextblog — Blog Platform"
type: project
status: completed
created: 2026-03-19
updated: 2026-03-19
tags: [project, nextjs, prisma, postgresql, blog, completed]
---

# nextblog — Blog Platform

## Overview

| Field | Value |
|-------|-------|
| **Path** | `~/Documents/Projects/Personal/nextblog/` |
| **Purpose** | Blog platform |
| **Status** | **Completed** — archive candidate |
| **Package manager** | npm |

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript |
| ORM | Prisma |
| Database | PostgreSQL |
| Auth | Better-Auth |
| UI Components | Shadcn/ui + Radix UI |
| Rich Text | TipTap (custom extensions) |
| Mutations | Server Actions |

## Commands

```bash
cd ~/Documents/Projects/Personal/nextblog

npm run dev    # Dev server
npm run build  # Production build
npm run lint   # ESLint
```

## Architecture

```
nextblog/
├── (admin)/    # Admin route group
├── (auth)/     # Auth route group
├── blog/       # Public blog routes
├── components/
│   └── ui/     # Shadcn/ui + Radix UI components
└── prisma/     # Prisma schema + migrations
```

- **Routing:** Next.js App Router with route groups: `(admin)/`, `(auth)/`, `blog/`
- **Mutations:** Server Actions (no separate API layer)
- **Auth:** Better-Auth
- **DB:** Prisma ORM + PostgreSQL; migrations in `prisma/`
- **Editor:** TipTap rich text with custom extensions

## Status Notes

Project is marked complete. Consider archiving to `099-Archive/` once confirmed no
further development is planned. Keeps `030-Projects/` clean.

## Archive Decision

- [ ] Confirm no active users or deployments
- [ ] Confirm no planned features
- [ ] Move to `099-Archive/` and update [[projects-index]]
