---
title: "OGLOQ — Primary Workstation"
type: infrastructure
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [infrastructure, ogloq, arch-linux, workstation, local]
---

# OGLOQ — Primary Workstation

> Arch Linux development workstation. Dual GPU, dual NVMe, 38GB RAM.

## Hardware

| Component | Spec |
|-----------|------|
| **CPU** | AMD Ryzen 7 7840HS (16 threads) |
| **GPU (discrete)** | NVIDIA GeForce RTX 4060 Max-Q (8GB VRAM) |
| **GPU (integrated)** | AMD Radeon 780M |
| **RAM** | 38.4 GB |
| **Storage 1** | 1.9T NVMe (MAXIO MAP1602, ext4) — Linux root |
| **Storage 2** | 954G NVMe (Windows NTFS) |
| **Wi-Fi** | Realtek RTL8852BE |
| **Ethernet** | Realtek RTL8111/8168/8211 |
| **Hostname** | OGLOQ |

## Software

| Layer | Technology |
|-------|-----------|
| **OS** | Arch Linux, kernel 6.18.18-1-lts |
| **WM** | Hyprland (Wayland) |
| **Shell** | Zsh + Powerlevel10k |
| **Editor** | Neovim, VS Code |
| **Audio** | PipeWire |
| **Passwords** | 1Password 8 (with SSH agent) |
| **Package mgrs** | pacman, yay, paru |

## Storage

```
/           1.9T ext4   33% used (~573G)
/boot       ~59% used   (monitor; clean old kernels if >80%)
/swapfile   8GB         (active, persisted in fstab)
```

## Network Interfaces

| Interface | Type | Address |
|-----------|------|---------|
| wlan0 | Wi-Fi ("Hopscotch 1") | 10.0.0.34/24 |
| bch | WireGuard VPN | 10.88.88.3/24 |
| CloudflareWARP | WARP tunnel | 172.16.0.2/32 |
| docker0 | Docker bridge | 172.17.0.1/16 |

## Projects (Local)

All under `~/Documents/Projects/`:

| Directory | Stack | Purpose |
|-----------|-------|---------|
| `Personal/webapp` | Next.js 15, TypeScript, Bun | Sidepocket frontend PWA |
| `Personal/sp-app` | Flask, Python, GraphQL | Sidepocket backend API |
| `Personal/nextblog` | Next.js 16, Prisma | Blog platform (completed) |
| `Personal/sp-backend-api-testing` | Cypress 13.13.2 | E2E API testing |
| `HackHarvard2025/` | Flask + React + Mapbox | Boston Daddy (completed) |
| `Support/` | Python, CUDA 12.8 | Multi-tool utility toolkit |

## Key Software

- **Neuroimaging:** freesurfer-bin, fsl (AUR)
- **Gaming/Emulation:** cemu, citra, sudachi
- **VPNs:** nordvpn, cloudflare-warp, WireGuard
- **AUR helpers:** yay 12.5.7, paru 2.1.0
- **Browsers:** Firefox, Chromium, Brave, Vivaldi

## Maintenance Notes

- `/boot` at 59% — clean old kernels if approaches 80%
- `~/.cache/huggingface` (~5GB) — deferred, may be active model cache
- `wg-quick@bch` — re-enable when `/etc/wireguard/bch.conf` is restored
- ACPI BIOS errors on boot — cosmetic, non-actionable

## Related

- [[hardware-specs|Hardware Specs]]
- [[packages-aur|AUR Packages]]
- [[networking|Networking]]
- [[dotfiles-index|Dotfiles]]
