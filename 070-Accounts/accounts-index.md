---
title: "Accounts -- Index"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [accounts, subscriptions, index]
---

# Accounts -- Index

> Service accounts and subscriptions. No passwords here -- reference 1Password.

## Development & Hosting

| Service | Purpose | Account | Notes |
|---------|---------|---------|-------|
| GitHub | Code hosting | DanielBrMz (HTTPS, full-scope PAT) | Personal + Sidepocketinc org, 25 public repos |
| AWS | ECS deployment (Sidepocket) | Via Sidepocket org | No local CLI config, SSH-only (cache EC2) |
| Sentry | Error tracking (sp-app) | Via Sidepocket org | MCP integration available |
| Jira / Confluence | Project management | Sidepocket Atlassian cloud | Cloud ID in Claude memory |
| Vercel | Frontend deployment | -- | vercel CLI installed (AUR) |
| ngrok | Tunneling | -- | ngrok CLI installed (AUR) |

## Productivity & Tools

| Service | Purpose | Notes |
|---------|---------|-------|
| Obsidian | Second brain | Free tier, vault at `~/Brain/`, v1.8.9 |
| 1Password | Password manager | Desktop + CLI, SSH agent integration |
| VS Code | Code editor | v1.112.0 |
| Slack | Sidepocket workspace | Desktop app (AUR) |
| Zoom | Video calls | Desktop app (AUR) |

## Networking / VPN

| Service | Notes |
|---------|-------|
| Cloudflare WARP | Active tunnel (172.16.0.2) |
| NordVPN | Installed (AUR), status unknown |
| WireGuard (BCH) | Active VPN to BCH cluster (10.88.88.3) |

## Media & Entertainment

| Service | Notes |
|---------|-------|
| Tidal HiFi | Desktop client (AUR) |
| Netflix | Desktop wrapper (AUR) |
| ani-cli | Anime streaming CLI |
| lobster-git | Media streaming CLI |

## Gaming

| Service | Notes |
|---------|-------|
| ProtonUp-Qt | Steam/Proton manager |
| Cemu | Wii U emulator |
| Citra | 3DS emulator |
| Sudachi | Switch emulator |
| VMware Workstation | Virtualization |

## Credentials Location

Passwords and API keys stored in: **1Password**

See [[../020-Infrastructure/credentials-index|Credentials Index]] for SSH/GPG keys.

## Related

- [[../020-Infrastructure/credentials-index|Credentials Index]]
- [[../010-System/packages-aur|AUR Packages]]
