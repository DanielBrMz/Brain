---
title: "Arch Linux — System Overview"
type: reference
created: 2026-03-19
updated: 2026-03-19
tags: [system, arch, linux, hardware]
---

# Arch Linux — System Overview

## OS & Kernel

| Field | Value |
|-------|-------|
| **OS** | Arch Linux (rolling release) |
| **Kernel** | `6.18.18-1-lts` (LTS branch) |
| **Shell** | bash |
| **User** | brmz |

## Storage

| Mount | Size | Used | Use% | Notes |
|-------|------|------|------|-------|
| `/` | 1.9T NVMe | ~573G | 33% | Healthy — audited 2026-03-19 |
| `/boot` | — | — | 59% | Monitor; clean old kernels if needed |

> Boot at 59% — flag if it climbs above 80%.

## Memory

| Field | Value |
|-------|-------|
| **RAM** | 38 GB |
| **Swap** | 8 GB swapfile at `/swapfile` — active as of 2026-03-19 |
| **zswap** | Not configured (swapfile is sufficient) |

## Packages

| Category | Count | Notes |
|----------|-------|-------|
| Official (pacman) | ~1500+ | Fully up to date as of 2026-03-19 |
| AUR / foreign | 59 | See [[packages-aur]] |
| Orphans | 0 | All 29 removed 2026-03-19 |

## Maintenance Posture (as of 2026-03-19)

- Packages: fully up to date
- Orphans: cleared
- Cache: trimmed (paccache -rk2 applied)
- Swap: active
- Services: all healthy
- Failed services: none

## Related Notes

- [[maintenance-log]] — full history of changes
- [[services]] — running service inventory
- [[known-issues]] — cosmetic/non-actionable issues
- [[packages-aur]] — AUR package list
- [[hardware-specs]] — detailed hardware (run `inxi -Fxz` to populate)
- [[optimizations]] — applied performance tuning
