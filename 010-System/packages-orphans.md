---
title: "Orphaned Packages"
type: log
created: 2026-03-19
updated: 2026-03-19
tags: [system, packages, orphans]
---

# Orphaned Packages

## Current Status

**Orphan count: 0** — all orphans removed 2026-03-19.

---

## History

### 2026-03-19 — Removed 29 Orphans

```bash
sudo pacman -Rns $(pacman -Qdtq)
```

Package names were not captured before removal. Run `git log` or check journal if needed:

```bash
sudo journalctl -b | grep "removed"
```

---

## Ongoing Check

Add to monthly maintenance:

```bash
pacman -Qdtq
```

If output is non-empty, review each package before removing — occasionally a "orphan" is
intentionally installed (e.g., a standalone tool with no reverse deps).

```bash
# Remove all orphans (after reviewing the list)
sudo pacman -Rns $(pacman -Qdtq)
```
