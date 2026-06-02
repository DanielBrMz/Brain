---
title: "User Profile"
type: user
created: 2026-03-19
updated: 2026-03-20 (session 4)
tags: [claude, profile, user, meta]
---

# User Profile

> Claude reads this to understand who you are and how to collaborate effectively.

## Identity

- **Name:** Daniel Barrerasmeraz
- **Username:** brmz (local) / `daniel.barrerasmeraz` (BCH/HMS) / `dbarreras` (Sidepocket jump host)
- **Machine:** Arch Linux (KDE/Wayland, SDDM), 38GB RAM, 1.9TB NVMe

## Roles

### Research Engineer — BCH / HMS
**Boston Children's Hospital + Harvard Medical School**
**FNNDSC** = Fetal-Neonatal Neuroimaging & Developmental Science Center

- Neuroimaging research computing on a shared Ubuntu 24.04 cluster
- Cluster: busan, sejong, hanyang, gangnam — 10× RTX A5000, Kubernetes, NFS home at `/neuro/users/`
- Access via WireGuard `bch` VPN
- See [[../020-Infrastructure/servers-index|servers-index]]

### Tech Lead — Sidepocket Inc

**Sidepocket** is a fintech investment platform — portfolio management, brokerage (Apex), cash/ACH (Plaid), billing (Stripe), notifications (Twilio/OneSignal).

- 8 Python/Flask microservices: `stratz`, `auth`, `accounts`, `app-backend`, `billing`, `events`, `cash`, `portfolio`
- Deployed on AWS ECS; dev infra: RDS PostgreSQL + ElastiCache Redis
- Dev server: `dev-ubuntu` (`172.31.1.203`, AWS EC2) — repos at `/home/ubuntu/code/`
- AWS account: `961086480768` (us-east-1)
- JIRA project: `TECH` — active tickets: TECH-3826 (SQLite unit tests), TECH-3827 (AccountingCacheHandler)
- Git co-author: `DanielBrMz <a01254805@tec.mx>`
- See [[../030-Projects/sidepocket-infrastructure|sidepocket-infrastructure]] for full context

---

## Sidepocket Projects

| Service | Stack | Path |
|---------|-------|------|
| Frontend PWA | Next.js 15, Bun, tRPC, Zustand | `Personal/webapp` |
| Backend API | Flask, Graphene GraphQL, PostgreSQL, Redis | `Personal/sp-app` |
| CMS | Next.js (`sp-endorser-cms`) | `Personal/sp-endorser-cms` |
| Blog (completed) | Next.js 16, Prisma, PostgreSQL | `Personal/nextblog` |
| Microservices | Various | `sp-stratz`, `sp-auth`, `sp-cash`, `sp-util`, etc. |

---

## Stack & Tools

| Category | Tools |
|----------|-------|
| Package managers | Bun (webapp), pip (sp-app), npm (nextblog), paru/yay (AUR) |
| Containerization | Docker, Docker Compose |
| VPN | WireGuard (`bch` → FNNDSC cluster), Cloudflare WARP, NordVPN |
| Deployment | AWS ECS (sp-app), Docker |
| Monitoring | Sentry (sp-app) |
| AI/ML | HuggingFace model cache (~5GB) — experimentation |
| Security | Historically: blackarch, OWASP ZAP |
| Password manager | 1Password (agent at `~/.1password/agent.sock`) |

---

## Working Style

- High-spec local machine — not resource-constrained, prefers local over cloud where practical
- Runs KDE/Wayland — GUI apps available (Obsidian, VS Code, JetBrains)
- Two distinct professional contexts: BCH/HMS research + Sidepocket engineering leadership

## How to Collaborate

- Be direct and terse — skip preamble
- Treat the system as mine to manage — make decisions, don't ask for permission on routine tasks
- Flag deferred items explicitly rather than silently skipping
- Update vault notes when state changes rather than only memory files
