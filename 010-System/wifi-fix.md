---
title: "WiFi Fix — Comcast HT-MCS + RTW89 Stability"
type: reference
created: 2026-05-03
updated: 2026-05-19
tags: [system, wifi, kernel, mac80211]
---

# WiFi Fix

## Problem

RTL8852BE (wlan0) was stuck at **54 Mbps** (legacy 802.11a) despite being a WiFi 6 card.

**Root cause:** Comcast/Xfinity gateways set all bits to `0xFF` in the Basic HT-MCS Set, including MCS 16-76 (3+ spatial streams). The kernel checks that all "required" MCS rates are supported by the STA — since the card only supports 2 streams, it fails and disables HT entirely.

Journal fingerprint:
```
wlan0: required MCSes not supported, disabling HT
```

## Defense-in-Depth (4 layers)

### Layer 1 — Patched mac80211.ko

Patch `net/mac80211/mlme.c` to skip the MCS check for bytes 2+ (3+ stream rates). Only enforces MCS 0-15 (bytes 0-1), which is the valid range for basic rates.

Installed at: `/usr/lib/modules/<kver>/updates/mac80211.ko`
(`/updates/` takes priority over the kernel's own module directory.)

### Layer 2 — Pacman Hook (primary)

`/etc/pacman.d/hooks/91-mac80211-patch.hook` — triggers on `linux`, `linux-lts`, and their `-headers` packages. Runs `/usr/local/bin/rebuild-mac80211` after every kernel upgrade to build the patched module for all installed kernels.

### Layer 3 — Boot-Time Systemd Service (safety net)

`/etc/systemd/system/mac80211-patch.service` — runs `rebuild-mac80211 --check-running` on boot. Uses `ConditionPathExists=!/usr/lib/modules/%v/updates/mac80211.ko` so it only fires when the patched module is missing for the booted kernel. If triggered, it downloads source, builds the module, and hot-reloads the WiFi stack (unloads rtw89 + mac80211, loads patched mac80211, reloads rtw89, reconnects WiFi).

### Layer 4 — NetworkManager Dispatcher (alert)

`/etc/NetworkManager/dispatcher.d/90-check-wifi-ht` — runs on every wlan0 `up` event. Checks if the connection is at 54 Mbps and logs a warning via `logger` if HT appears disabled. Does NOT auto-fix (module reload drops the connection, bad UX). Just alerts so the user knows to investigate.

## Files

| File | Purpose |
|------|---------|
| `/usr/local/bin/apply-mcs-patch.py` | Python: applies the MCS patch to a fresh mlme.c |
| `/usr/local/bin/rebuild-mac80211` | Bash: download, patch, build, install mac80211.ko |
| `/etc/pacman.d/hooks/91-mac80211-patch.hook` | Pacman: trigger rebuild on kernel upgrades |
| `/etc/systemd/system/mac80211-patch.service` | Systemd: boot-time safety net |
| `/etc/NetworkManager/dispatcher.d/90-check-wifi-ht` | NM: last-resort 54 Mbps alert |
| `/var/cache/mac80211-patch/` | Cached kernel source tarballs |
| `/var/log/mac80211-patch.log` | Build log |

## rebuild-mac80211 Modes

```bash
sudo rebuild-mac80211              # Build for all kernels with headers (pacman hook)
sudo rebuild-mac80211 --check-running  # Build + hot-reload for running kernel if missing (boot service)
sudo rebuild-mac80211 --reload     # Just hot-reload (assumes module already built)
sudo rebuild-mac80211 6.18.32-1-lts   # Build for a specific kernel version
```

## RTW89 Driver Options

`/etc/modprobe.d/rtw89.conf`:
```
options rtw89_pci disable_aspm=y
options rtw89_core disable_ps_mode=y
```

- `disable_aspm=y` — prevents PCIe ASPM from cutting power to the WiFi card
- `disable_ps_mode=y` — disables WiFi power save mode (reduces disconnects/latency)

## Verification

```bash
iw dev wlan0 link          # expect rx/tx bitrate >> 54 Mbps (HE-MCS, 200+ Mbps)
dmesg | grep "disabling HT"  # should return nothing
journalctl -u mac80211-patch  # check boot service status
cat /var/log/mac80211-patch.log  # full build log
```

## When This Becomes Unnecessary

If upstream `mac80211` adds tolerance for broken APs (ignore Basic MCS > station capability), or Comcast pushes a firmware update to their gateways, all of this can be removed:

```bash
sudo systemctl disable mac80211-patch.service
sudo rm /etc/systemd/system/mac80211-patch.service
sudo rm /etc/pacman.d/hooks/91-mac80211-patch.hook
sudo rm /etc/NetworkManager/dispatcher.d/90-check-wifi-ht
sudo rm /usr/local/bin/rebuild-mac80211 /usr/local/bin/apply-mcs-patch.py
sudo rm -rf /var/cache/mac80211-patch /var/log/mac80211-patch.log
# Remove patched modules from all kernel dirs:
sudo rm -f /usr/lib/modules/*/updates/mac80211.ko
sudo depmod -a
```

## Incident Log

### 2026-05-19: Script syntax bug

Rebuild script had `local cleanup() { ... }` — invalid bash syntax that caused silent abort under `set -euo pipefail`. The pacman hook was failing on every kernel upgrade since creation. Fixed by removing the bad line, then rewrote the entire script with:
- Source tarball caching (`/var/cache/mac80211-patch/`)
- `--check-running` mode for boot-time safety net
- `--reload` mode for hot-swapping the module
- Per-kernel error isolation (one failure doesn't block others)
- Logging to `/var/log/mac80211-patch.log`
- Stale cache cleanup

Added systemd boot service and NM dispatcher as defense layers 3 and 4.
