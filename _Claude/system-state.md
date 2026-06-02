---
title: "System State"
type: project
created: 2026-03-19
updated: 2026-03-20 (session 4)
tags: [claude, system, state, meta]
---

# System State

> Canonical record of machine state for Claude. Cross-reference [[../010-System/arch-overview|arch-overview]]
> and [[../010-System/maintenance-log|maintenance-log]] for full detail.

## Current State (verified 2026-03-19)

| Resource | Value |
|----------|-------|
| `/` disk | 1.9T total — **573G used (33%)** |
| `/boot` | 1020M total — 596M used (59%) — monitor |
| RAM | 38GB — 10GB used, 28GB free |
| Swap | 8GB swapfile at `/swapfile` — active (520MB used) |
| Orphans | **0** — cleared 2026-03-19 |
| Failed units | **0** — all services healthy |
| Packages | Fully up to date; 59 AUR packages |

## Deferred / Pending User Decision

| Item | Size | Status |
|------|------|--------|
| `~/.cache/huggingface/` | 5.0GB | User to decide — ML model weights |
| `~/Videos/` | 6.4GB | User content — not touched |
| `/boot` growth | 59% | Monitor — clean old kernels if >80% |

## Maintenance History

### Session 1 — 2026-03-19
- Removed 36 orphaned packages (1,058 MiB freed)
- User cache cleaned: pip, spotify, browsers, vscode-cpptools, selenium, electron, yay (~10GB freed)
- `wg-quick@bch.service` fixed (resolvconf signature mismatch → `sudo resolvconf -u`)
- 8GB swapfile created, activated, persisted in `/etc/fstab`
- Bluetooth cosmetic warning confirmed non-actionable

### Session 2 — 2026-03-19
- Docker prune: 46 containers, all unused images — **34.67GB freed**
- `sp-endorser-cms/.next` removed — 1.4GB freed
- Python `__pycache__` cleaned across projects
- Journals vacuumed to 200MB — 270MB freed
- **Total freed: ~36GB** (609G → 573G)

### Session 3 — 2026-03-19
- Obsidian Brain vault built at `~/Brain/` (36 files, 10 folders)
- CLAUDE.md updated to current state
- Claude memory migrated into vault at `_Claude/`

### Session 4 — 2026-03-20
- SSH config audited and all servers successfully connected
- BCH = Boston Children's Hospital, FNNDSC = Fetal-Neonatal Neuroimaging & Developmental Science Center
- Domain confirmed: `galena.fnndsc` — neuroscience compute cluster with NFS home (`/neuro/users/`)
- Auth: `id_ed25519` (passphrase in 1Password) — works; SSH config `IdentityAgent` override needed for headless use
- `wireguard.md` corrected: `bch` active since session 1; `wg0` home VPN server documented
- All 4 FNNDSC nodes probed: busan (251GB RAM), sejong (235GB, disk 76%⚠), hanyang (K8s node, 1.8TB storage), gangnam (K8s master, memory pressure⚠)
- AWS `cache` connected: Amazon Linux 2023, dormant — no services running
- `servers-index.md` fully populated with roles, specs, users, services, watch items
- `sshpass` installed (for password-auth SSH workflows)

## Services (all healthy)

| Service | Status | Notes |
|---------|--------|-------|
| `wg-quick@bch.service` | Active | Fixed session 1 |
| `bluetooth.service` | Active | Cosmetic hci0 warning only |
| `docker.service` | Active | |
| `sshd.service` | Active | |
| `NetworkManager.service` | Active | |
| `warp-svc.service` | Active | Cloudflare WARP |

## Discovered Projects (not in original CLAUDE.md)

| Path | Status | Notes |
|------|--------|-------|
| `Personal/sp-backend-api-testing/` | Unknown | Likely Sidepocket API testing |
| `Projects/HackHarvard2025/` | Unknown | Hackathon — not under Personal/ |
| `Personal/sp-endorser-cms` | Active | 1.5G; `.next` cache cleared |
| `Personal/sp-stratz`, `sp-auth`, `sp-cash`, `sp-util`, `sp-accounts`, `sp-events` | Active | Sidepocket microservices |

## Related Notes

- [[../010-System/arch-overview|arch-overview]] — full OS/hardware detail
- [[../010-System/maintenance-log|maintenance-log]] — complete task history
- [[../010-System/services|services]] — service inventory
