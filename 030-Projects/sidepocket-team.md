---
title: "Sidepocket — Team"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, sidepocket, team, people]
---

# Sidepocket — Team

> Team roster as of 2026-03-20. Slack IDs and roles inferred from #backend, #team-sprintreview, and DM history.

---

## Maxwell Bradley (Max)

- **Slack:** `U05HLGN752N`
- **Role:** Manager / CEO or CTO — runs sprints, product direction, ticket assignment, final decisions
- **Communication:**
  - Sends EOD updates — respond concisely, conversational, paragraphs, **no ticket codes** (use issue titles)
  - Active in DMs for direction-setting and quick decisions
  - Runs #team-sprintreview, pings team for sprint-end summaries
- **Style:** Direct, results-oriented. Gives SSH aliases and 1Password links over Slack DM. Expects unit tests with breaking changes.
- **Known positions:**
  - All microservices must be on same Python version (pickling compatibility) until S3 migration complete
  - Tax feature: no re-auth, no credential storage — awaiting final scope decision
  - Interested in cache service speed diff tests at some point

---

## Yves Perrenoud

- **Slack:** `U06GCJQAE4W`, **GitHub:** `pernu`, **dev-ubuntu user:** `pyves`
- **Role:** DevOps / Infrastructure — ECS, Earthly CI/CD, Docker, S3, AWS infra
- **Current work:**
  - Preparing ECS setup for long-running cache service (UAT first, then prod)
  - Created new S3 bucket `market-data-cache-dev` (renamed from `dev.cache`)
  - Manages Dockerfile for service stack upgrades (TECH-3842)
  - TECH-3843: infra definition files for long-running service
  - TECH-3833: Decommission ElastiCache (assigned, pending TECH-3830 completion)
- **Technical opinions:** Strong views on DynamoDB vs S3 tradeoffs (S3 Express One Zone for low latency but single AZ; DynamoDB for hot keys + querying). Prefers committing alembic migration files alongside model changes (vs. the old gitignored approach).
- **Coordination note:** Daniel waits on Yves for ECS/infra before wiring up cache service deploy.

---

## Tomasz Pado

- **Slack:** `U03PSKTEMNG`, **dev-ubuntu users:** `tomaszp`, `tomaszpdev`
- **Role:** Infrastructure — self-hosted GitHub Actions runners
- **Manages:** GitHub Actions self-hosted runners; Cypress VM runners. When a runner disconnects for an extended period GitHub removes it; reconnect by restarting the VM.

---

## Travis H

- **Slack:** `U02HRS1RR2B`, **dev-ubuntu user:** `travis`
- **Role:** CI/CD — Earthly build system, Cognito migration, regulatory/Apex compliance
- **Earthly:** "It's like makefile and dockerfile had a baby." Travis built and maintains the Earthly pipeline (`util:develop` as reference). Handles GitHub secrets/deploy token strategy for CI.
- **Other priorities:** Cognito migration (part of Apex compliance requirement — "losing our relationship with Apex is an existential risk to the company"), regulatory compliance work.

---

## Samuel Cabrera (Sam)

- **Slack:** `U07CUG851EK`
- **Role:** Full-stack developer
- **Current work:** TECH-3839 — Provider Abstraction Layer + Multi-Account Support (On Code Review). Previously TECH-3819, TECH-3820.

---

## Andrii Zakhariak

- **Slack:** `U0379515LLX`
- **Role:** Frontend / webapp developer
- **Current work:** Bug fixes and UX improvements on the webapp. Active tickets: TECH-3840 (back nav animation freeze, macOS), TECH-3844 (mobile menu active states), TECH-3845 (DRY/accessibility refactor). Completed TECH-3841 (mobile gap fix), TECH-3855, TECH-3861.

---

## José María Soto Vzla / Jose Valenzuela (Chema)

- **Slack:** `U067X046PB6`, **JIRA display name:** Jose Valenzuela
- **Role:** Backend developer — auth migration, WebAuthn/Passkeys
- **Current work:**
  - WebAuthn/Passkeys epic — biometric authentication (TECH-3835, 3836, 3837, 3838)
  - Auth migration investigation: evaluated Auth0 → switched plan to Supabase → ultimately decided to stay on custom auth service
  - Now focused on WebAuthn (passkeys) as the auth upgrade path
  - PR #182 on auth repo — new `webauthn_credential` table + Alembic migration; CI failing due to Earthly/Docker issue on runner (not his code)

---

## Joab Kose

- **Slack:** `U040233JZ1N`
- **Role:** Security
- **Current work:** SEC tickets — GCP API key audit (SEC-922), other SEC-series security investigations. Reports to Max who tracks these closely.

---

## Artur

- **Slack:** `U02J6JN548J`
- **Role:** Director of Business Development

---

## Shri

- **Slack:** `U02JW6VKJLQ`
- **Role:** Infrastructure / backend (mentioned alongside Yves and Travis in build system context)

---

## Server-Only Users (dev-ubuntu)

| User | Notes |
|------|-------|
| `fnazir` | Team member — appears in server user list |
| `mzarq` | Team member — last active Aug 2025 |

---

## Key Relationships for Daniel

- **Max** — direct manager. EOD updates in DMs. Concise, no ticket codes.
- **Yves** — infrastructure partner. Coordinate on ECS/S3 deploy timing before wiring cache service.
- **Chema** — check with him on auth/alembic workflow questions; he's the one working in that space actively.
- **Tomasz** — ping when GitHub Actions runners are down.
- **Travis** — Earthly CI questions; also owns Apex compliance track (separate from Daniel's work).
