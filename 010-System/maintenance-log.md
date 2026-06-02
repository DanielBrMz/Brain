---
title: "System Maintenance Log"
type: log
created: 2026-03-19
updated: 2026-03-19
tags: [system, maintenance, log]
---

# System Maintenance Log

---

## 2026-03-19 — Initial Full Maintenance Pass

### Completed

| Task | Result |
|------|--------|
| Full system update (`pacman -Syu`) | All packages up to date |
| Orphan removal (`pacman -Rns $(pacman -Qdtq)`) | 29 orphans removed |
| Pacman cache trim (`paccache -rk2`) | Cache trimmed to last 2 versions; ~4GB recovered |
| User cache audit (`~/.cache`) | Investigated 20GB cache; huggingface (5GB) deferred to user decision |
| Docker prune | Cleaned unused images/containers |
| Swapfile creation | 8GB `/swapfile` created and activated; permanent via `/etc/fstab` |
| `wg-quick@bch.service` | Diagnosed — config file missing/invalid; service disabled to prevent failure |
| Bluetooth config warning | Investigated `Failed to set default system config for hci0` — cosmetic, no action needed |
| WireGuard `bch` interface | Disabled; user to reconfigure if needed |

### Storage After Maintenance

| Before | After |
|--------|-------|
| 613G used (35%) | ~573G used (33%) |

---

## Deferred / Pending

| Item | Status | Notes |
|------|--------|-------|
| `~/.cache/huggingface` (5GB) | **Deferred** | User to decide — may be active model data |
| `/boot` at 59% | Monitor | Clean old kernels if approaches 80% |
| Bluetooth `hci0` warning | Cosmetic | No action needed unless BT issues arise |
| Obsidian vault setup | **Done 2026-03-19** | `~/Brain/` created |
| AUR packages list | Pending | Run `pacman -Qm` to populate [[packages-aur]] |
| Hardware specs | Pending | Run `inxi -Fxz` to populate [[hardware-specs]] |
| Dotfiles index | Pending | Explore `~/.config`, `~/.local` to populate [[dotfiles-index]] |

---

## Maintenance Checklist (recurring)

Run monthly or before major changes:

```bash
# 1. Update all packages
sudo pacman -Syu

# 2. Check for orphans
pacman -Qdtq

# 3. Trim package cache
sudo paccache -rk2

# 4. Check failed services
systemctl --failed

# 5. Check disk usage
df -h / /boot
du -sh ~/.cache/*

# 6. Check journal for errors
sudo journalctl -p 3 -xb
```
