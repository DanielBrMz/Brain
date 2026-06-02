---
title: "Networking"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [infrastructure, networking, dns, firewall]
---

# Networking

## Interfaces

| Interface | Type | IP | Notes |
|-----------|------|----|-------|
| wlan0 | Wi-Fi (Realtek RTL8852BE, 802.11ax) | 10.0.0.34/24 | Primary connection ("Hopscotch 1") |
| bch | WireGuard | 10.88.88.3/24 | BCH VPN tunnel (active) |
| CloudflareWARP | Tunnel | 172.16.0.2/32 | Cloudflare WARP (active) |
| docker0 | Bridge | 172.17.0.1/16 | Docker (no containers running) |
| lo | Loopback | 127.0.0.1/8 | -- |

**IPv6:** 2601:189:8501:eff0::dff5/128 on wlan0

## DNS

| Setting | Value |
|---------|-------|
| Resolver | systemd-resolved (resolv.conf mode: foreign) |
| DNS (wlan0) | 75.75.75.75, 75.75.76.76 (Comcast/Xfinity) |
| DNS (global) | 127.0.2.2, 127.0.2.3 (Cloudflare WARP local proxy) |
| Fallback DNS | Quad9 (9.9.9.9), Cloudflare (1.1.1.1), Google (8.8.8.8) |
| DNSSEC | Not supported |
| DNSOverTLS | Disabled |

## Network Manager

- **Tool:** NetworkManager
- **Wi-Fi backend:** iwd or wpa_supplicant
- **Saved networks:** 30+ WiFi profiles

## Firewall

Docker iptables rules only (FORWARD chain DROP policy, DOCKER-USER chain). No custom firewall configured -- INPUT/OUTPUT chains are ACCEPT.

## VPN

- **WireGuard (bch):** Active at 10.88.88.3/24. Previously marked as disabled but currently UP.
- **Cloudflare WARP:** Active at 172.16.0.2/32.
- **NordVPN:** Installed (AUR) but status unknown.
- See [[wireguard|WireGuard]] for BCH VPN details.

## Related

- [[wireguard|WireGuard]]
- [[servers-index|Servers Index]]
- [[../010-System/arch-overview|Arch Overview]]
- [[../010-System/hardware-specs|Hardware Specs]]
