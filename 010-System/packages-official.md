---
title: "Official Packages (pacman)"
type: reference
created: 2026-03-19
updated: 2026-03-19
tags: [system, packages, pacman]
---

# Official Packages (pacman)

The full package list is too large to enumerate here. Use pacman directly.

## Useful Queries

```bash
# Total installed package count
pacman -Q | wc -l

# List explicitly installed packages (not pulled in as deps)
pacman -Qe

# List explicitly installed, excluding deps
pacman -Qen   # official only
pacman -Qem   # AUR/foreign only

# Search installed packages
pacman -Qs <keyword>

# Show info about a package
pacman -Qi <package>

# List files owned by a package
pacman -Ql <package>

# Find which package owns a file
pacman -Qo /path/to/file
```

## Package Groups of Interest

```bash
# Base system
pacman -Qg base-devel

# Check for packages in a specific group
pacman -Sg <group>
```

## Orphan Check

```bash
# List orphans (installed as deps, no longer needed)
pacman -Qdtq

# Remove orphans
sudo pacman -Rns $(pacman -Qdtq)
```

> Last orphan cleanup: 2026-03-19 — 29 removed. Count: 0.

## Cache Management

```bash
# Show cache size
du -sh /var/cache/pacman/pkg/

# Trim to last 2 versions of each package
sudo paccache -rk2

# Remove all cached versions of uninstalled packages
sudo paccache -ruk0
```

> Last cache trim: 2026-03-19 (`paccache -rk2`)
