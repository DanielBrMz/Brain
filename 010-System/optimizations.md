---
title: "System Optimizations"
type: reference
created: 2026-03-19
updated: 2026-03-19
tags: [system, performance, optimization]
---

# System Optimizations

## Applied (2026-03-19)

### Swap — 8GB Swapfile

**Problem:** No swap configured on 38GB RAM system — OOM risk under memory pressure.

**Solution:**
```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=8192 status=progress
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Persisted via `/etc/fstab`:
```
/swapfile none swap defaults 0 0
```

**Status:** Active. Verify: `swapon --show`

---

### Package Cache Trim

**Problem:** `/var/cache/pacman/pkg/` had grown to ~5.6GB.

**Solution:**
```bash
sudo paccache -rk2   # keep last 2 versions per package
```

**Recovered:** ~4GB

---

### Orphan Removal

29 orphaned packages removed 2026-03-19. See [[packages-orphans]].

---

### Docker Cleanup

Unused Docker images and containers pruned 2026-03-19.

```bash
docker system prune -f
```

---

## Considered / Deferred

| Optimization | Status | Notes |
|-------------|--------|-------|
| zswap | Deferred | Swapfile is sufficient for current workload |
| `~/.cache/huggingface` (5GB) | **Pending user decision** | May be active model cache — do not delete without confirming |
| Preload / profile-based optimization | Not needed | System performs well as-is |
| systemd-oomd | Consider | Could add OOM protection as alternative/complement to swap |

---

## Performance Monitoring

```bash
# Memory pressure
free -h
vmstat 1 5

# Disk I/O
iostat -x 1 5

# CPU / process
htop
top

# Swap usage
swapon --show
cat /proc/swaps
```
