---
title: "WireGuard VPN"
type: reference
created: 2026-03-19
updated: 2026-04-09
tags: [infrastructure, wireguard, vpn, networking]
---

# WireGuard VPN

## Interfaces

| Interface | Role | Status | Notes |
|-----------|------|--------|-------|
| `bch` | BCH work VPN (client) | **Active** — enabled, handshake live | Enabled since session 1 (2026-03-19) |
| `wg0` | Home VPN (server) | Present in config | This machine serves 2 peers |

---

## bch (Work VPN)

- **Endpoint:** `178.156.223.165:51820`
- **This machine IP:** `10.88.88.3/24`
- **Routed subnets:**

| Subnet | Covers |
|--------|--------|
| `10.88.88.0/24` | VPN peer subnet (busan-vpn = 10.88.88.2) |
| `10.26.66.0/23` | BCH internal — busan (10.26.66.171), sejong (10.26.66.103) |
| `10.26.67.0/24` | BCH internal — hanyang (10.26.67.148) |
| `10.72.8.0/24` | BCH segment — gangnam (10.72.8.45) |

- **Service:** `wg-quick@bch.service` — enabled, active, persistent keepalive every 25s
- **DNS:** Commented out (was `8.8.8.8`) — see history
- **Endpoint port:** 443 (not 51820 — updated from original config)

### History

1. **2026-03-19 (session 1):** Failed state — fixed via `sudo resolvconf -u` (resolvconf signature mismatch)
2. **2026-04-09:** Failed again — Cloudflare WARP overwrote `/etc/resolv.conf` directly, breaking openresolv's signature tracking. `resolvconf -a bch` errored with "signature mismatch". **Fix:** commented out `DNS = 8.8.8.8` from `/etc/wireguard/bch.conf` — we don't need BCH DNS, just routing. Service now starts cleanly via systemd. All 4 BCH servers confirmed reachable (sejong, busan, hanyang, gangnam).

---

## wg0 (Home VPN Server)

This machine runs a WireGuard server for personal/home use.

- **Interface IP:** `10.0.0.1/24`
- **Listen port:** `51820`
- **Peers:** `10.0.0.2`, `10.0.0.3` (2 clients)
- Keys: `home-private.key`, `home-public.key` in `/etc/wireguard/`

---

## Quick Reference

```bash
# Show active interfaces
sudo wg show

# Check bch service
systemctl status wg-quick@bch.service

# Restart bch
sudo systemctl restart wg-quick@bch.service

# Bring up / down manually
sudo wg-quick up bch
sudo wg-quick down bch

# List all config files
ls /etc/wireguard/
```

---

## Related Notes

- [[servers-index]] — server inventory (all BCH servers reachable via bch VPN)
- [[networking]] — network topology
