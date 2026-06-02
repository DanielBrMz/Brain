---
title: "System Services"
type: reference
created: 2026-03-19
updated: 2026-03-19
tags: [system, services, systemd]
---

# System Services

## Status (as of 2026-03-19)

All critical services healthy. Zero failed units.

```bash
# Check at any time
systemctl --failed
systemctl status
```

## Key Services

| Service | Status | Notes |
|---------|--------|-------|
| `NetworkManager.service` | Active | Primary network management |
| `bluetooth.service` | Active | BT works; cosmetic config warning (see [[known-issues]]) |
| `docker.service` | Active | Docker engine |
| `postgresql.service` | Check | Used by sp-app and nextblog projects |
| `redis.service` | Check | Used by sp-app JWT blacklist |
| `sshd.service` | Check | SSH daemon — confirm enabled if remote access needed |
| `wg-quick@bch.service` | **Disabled** | WireGuard `bch` — disabled 2026-03-19; config was invalid |

## Swap

```bash
# Verify swap is active
swapon --show
free -h
```

Expected: `/swapfile  file  8G  0B  -2`

## Service Management Quick Reference

```bash
# Status
systemctl status <service>

# Start / stop / restart
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>

# Enable / disable at boot
sudo systemctl enable <service>
sudo systemctl disable <service>

# View logs
sudo journalctl -u <service> -n 50
```

## TODO

- [ ] Confirm `postgresql` and `redis` service names and status
- [ ] Confirm `sshd` state
- [ ] Document any user-space services (custom scripts, timers)
