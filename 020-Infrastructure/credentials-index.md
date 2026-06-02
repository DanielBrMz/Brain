---
title: "Credentials Index"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [infrastructure, credentials, security]
---

# Credentials Index

> **IMPORTANT:** This note is an INDEX only. Never store passwords, tokens, or private keys
> in plaintext in Obsidian. Use 1Password and reference entries by name only.

---

## Credential Storage

| Tool | Location | Notes |
|------|----------|-------|
| 1Password 8 | Desktop app (AUR: `1password 8.12.6`) | Primary password manager. SSH agent via `~/.1password/agent.sock` |

---

## SSH Keys

| Key | Location | Purpose | Hosts |
|-----|----------|---------|-------|
| `id_rsa` | `~/.ssh/id_rsa` | Sidepocket infra | dev-ubuntu, GitHub |
| `id_ed25519` | `~/.ssh/id_ed25519` | BCH/HMS cluster | sejong, busan, hanyang, gangnam |
| `sp-python-cache.pem` | `~/.ssh/` | AWS EC2 access | cache (54.162.5.34, ec2-user) |

**SSH Agent:** 1Password agent (`IdentityAgent ~/.1password/agent.sock`) configured for all hosts.

**SSH Config highlights:**
- BCH cluster: busan, hanyang, sejong, gangnam (direct + VPN variants)
- dev-ubuntu: jump host via 172.31.1.203
- cache: AWS EC2 at 54.162.5.34

---

## GPG Keys

Not currently configured for git signing.

---

## Service API Keys (reference names only)

| Service | Where Stored | Notes |
|---------|-------------|-------|
| GitHub PAT | System keyring (via `gh auth`) | DanielBrMz, full-scope token |
| Sidepocket tokens | `.env` files in project dirs | Per-environment (dev/qa/uat/prod) |
| Cloudflare WARP | System service | cloudflare-warp-bin |
| NordVPN | nordvpn-bin CLI | -- |

---

## Project Environment Variables

Project-specific env vars are in `.env` files or config files:
- [[../030-Projects/sidepocket-backend|sp-app env vars]] -- Postgres, Redis, app settings
- [[../030-Projects/sidepocket-webapp|webapp env vars]] -- multi-env config

## Related

- [[servers-index|Servers Index]]
- [[../070-Accounts/accounts-index|Accounts Index]]
- [[networking|Networking]]
