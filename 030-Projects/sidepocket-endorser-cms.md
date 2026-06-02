---
title: "sp-endorser-cms — Endorser Content Management System"
type: project
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [sidepocket, cms, payload, endorser, project]
---

# sp-endorser-cms — Endorser CMS

> Content management system for Sidepocket endorsers (financial advisors). Built on Payload CMS.

## Overview

| Field | Value |
|-------|-------|
| **Stack** | Next.js 15, Payload CMS 3.9, React 19, PostgreSQL, AWS S3, Lexical editor |
| **Package Manager** | pnpm (v9.15) |
| **Local Path** | `~/Documents/Projects/Personal/sp-endorser-cms/` |
| **GitHub** | `Sidepocketinc/sp-endorser-cms` + `Sidepocketinc/endorser-cms` |
| **Integrations** | Cloudflare Stream (video), SendGrid (email), S3 (media storage) |

## Architecture

### CMS Collections
- **Users** — Endorser and admin accounts with role-based access
- **Contents** — Insights/articles published by endorsers
- **Media** — Uploaded media files (S3-backed)
- **APIKeys** — API key management for integrations

### Access Control Roles
`admins`, `adminsAndReviewers`, `adminsOrPublished`, `anyone`, `endorsers`, `reviewers`

### Key Routes
- `/admin/` — Payload admin panel
- `/endorser/dashboard/` — Endorser dashboard (insights, audience, media, settings)
- `/endorser/(AuthPages)/` — Login, signup, password reset, email verification
- `/api/graphql` — GraphQL endpoint
- `/api/upload/` — File upload (TUS resumable)

### Components
- **Admin:** Custom Payload admin UI (login, dashboard, onboarding)
- **Auth:** Login/signup forms, logout
- **Dashboard:** Side navigation, profile, notifications
- **Insights:** Rich text editor (Lexical), media player, drag-and-drop
- **Settings:** Account settings forms

### State Management
- Zustand — `MediaStore.ts` for media state

## Duplicates

Test/scratch clones exist (can be cleaned up):
- `~/Documents/Projects/Sidepocket/Test/sp-endorser-cms/` (on `qa` branch)
- `~/Documents/Projects/Sidepocket/sp-endorser-cms/`

## Related

- [[sidepocket-webapp|Sidepocket Webapp]] — Frontend that consumes endorser content
- [[sidepocket-codebase|Sidepocket Codebase]] — All services documentation
- [[local-project-file-structures|Local File Structures]] — Full file-level documentation
