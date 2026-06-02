---
title: "BCH VPN Infrastructure"
type: infrastructure
updated: 2026-05-12
tags: [bch, vpn, wireguard, hetzner]
---

# BCH VPN Infrastructure

3-tier WireGuard VPN to access BCH research servers from home, bypassing BCH's institutional VPN (Palo Alto).

## Architecture

```
[Home - OGLOQ]  <--WireGuard-->  [Hetzner VPS Relay]  <--WireGuard-->  [Busan - BCH Gateway]
10.88.88.3                       178.156.223.165                       10.88.88.2
                                 (Port 443)                                  |
                                                                    [BCH Internal Network]
                                                                     10.26.x.x, 10.72.x.x
                                                                             |
                                                          [Hanyang, Sejong, Gangnam servers]
```

## The Three Systems

### 1. Hetzner VPS (178.156.223.165) - The Relay Hub

- **Root access:** `ssh root@178.156.223.165`
- **Role:** WireGuard server that relays traffic between home and BCH
- **Port:** 443 (BCH firewall blocks 51820, allows HTTPS)
- **Config:** `/etc/wireguard/wg0.conf`
- **IP:** 10.88.88.1/24

VPS routes BCH networks via Busan:
```
10.26.66.0/23  via 10.88.88.2 dev wg0
10.26.67.0/24  via 10.88.88.2 dev wg0
10.72.8.0/24   via 10.88.88.2 dev wg0
```

### 2. Busan (10.26.66.171) - BCH Gateway

- **Access:** `ssh busan-vpn` or `ssh daniel.barrerasmeraz@10.88.88.2`
- **Role:** WireGuard peer + NAT gateway to BCH internal servers
- **Elevated access:** `su - toor` then `sudo su`
- **Config:** `/etc/wireguard/wg0.conf`
- **IPs:** Ethernet 10.26.66.171 (BCH), VPN 10.88.88.2 (tunnel)

Busan ONLY routes VPN network through wg0:
```
AllowedIPs = 10.88.88.0/24  # NOT BCH networks -- critical
```
If BCH networks are in AllowedIPs, Busan routes them through VPN instead of local eno1.

### 3. OGLOQ - Home Machine (Arch Linux)

- **Config:** `/etc/wireguard/bch.conf`
- **IP:** 10.88.88.3/24
- **Connect:** `sudo wg-quick up bch`

## Peers

| Peer | IP | PublicKey | Status |
|------|----|-----------|--------|
| VPS (server) | 10.88.88.1 | `PgYctcGgC/VEXjbxTOgSgc7Xhm85fmPPxMxQo6dmfyI=` | Active |
| Busan (BCH) | 10.88.88.2 | `NaZKpijeu83ombqjXAWzNDZO25A/RLy9Vroeuctxayk=` | Active |
| Daniel (home) | 10.88.88.3 | `aYFJpwAZA9Bvf01WirQRjukCfmJUFOaxiFlXAkUcBDc=` | Active |
| Yair Beltran | 10.88.88.4 | (generated on VPS) | Active -- TEMPORARY, remove after BCH ends |

## Adding a New Peer

1. SSH into VPS: `ssh root@178.156.223.165`
2. Generate keys:
```bash
cd /etc/wireguard
wg genkey | tee NAME-private.key | wg pubkey > NAME-public.key
chmod 600 NAME-private.key
```
3. Add peer to `/etc/wireguard/wg0.conf`:
```ini
[Peer]
# name
PublicKey = <public key>
AllowedIPs = 10.88.88.N/32
```
4. Reload: `wg syncconf wg0 <(wg-quick strip wg0)`
5. Create client config:
```ini
[Interface]
Address = 10.88.88.N/24
PrivateKey = <private key>
DNS = 8.8.8.8

[Peer]
PublicKey = PgYctcGgC/VEXjbxTOgSgc7Xhm85fmPPxMxQo6dmfyI=
Endpoint = 178.156.223.165:443
AllowedIPs = 10.88.88.0/24, 10.26.66.0/23, 10.26.67.0/24, 10.72.8.0/24
PersistentKeepalive = 25
```

## Removing a Peer

1. SSH into VPS: `ssh root@178.156.223.165`
2. Remove the `[Peer]` block from `/etc/wireguard/wg0.conf`
3. Reload: `wg syncconf wg0 <(wg-quick strip wg0)`

## Pending Removals

- **yair.beltran (10.88.88.4)** -- added 2026-05-12, remove after BCH project ends (May 22)

## Notes

- BCH user accounts are centralized via NFS/LDAP -- no need to create accounts on servers
- Users only need VPN peer config + their SSH key on BCH servers
- Port 443 chosen because BCH firewall blocks standard WireGuard port (51820)
- Busan auto-starts WireGuard via systemd on reboot
