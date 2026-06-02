---
title: "IPv6 — System Configuration & Fix"
type: reference
created: 2026-03-30
updated: 2026-03-30
tags: [system, network, ipv6, firefox, cloudflare-warp]
---

# IPv6 — System Configuration & Fix

## Problem

Firefox would not connect to the internet on IPv4-only networks (e.g., `bchguest` at BCH), while Brave worked fine.

**Root cause chain:**
1. `bchguest` (and many networks this machine connects to) is **IPv4-only** — no router advertisements, no DHCPv6
2. WARP assigns a local IPv6 address (`2606:4700:cf1:1000::4/128`) but in **split-tunnel mode only** — no IPv6 default route exists
3. By default, Linux `getaddrinfo()` prefers IPv6 — so Firefox got AAAA records and tried to connect via IPv6
4. IPv6 connections failed (no route to host), but Firefox's Happy Eyeballs fallback was too slow, making pages appear broken
5. Secondary issue: `prefs.js` was owned by root (written by an accidental root Firefox session), so Firefox couldn't read its own settings, compounding the problem

## Why Brave Worked

Brave/Chromium implements Happy Eyeballs v2 more aggressively and falls back to IPv4 within ~300ms. Firefox's fallback was slower or broken when the failure mode was "no route" rather than timeout.

## Infrastructure Context

| Component | Status |
|-----------|--------|
| Network (bchguest) | IPv4-only, no IPv6 RA |
| Cloudflare WARP | Running, split-tunnel mode (Sidepocket org) |
| WARP mode switch | **Disabled by org policy** — cannot enable full gateway |
| System IPv6 kernel | Enabled (`disable_ipv6 = 0`) |
| IPv6 default route | None |

## Fixes Applied

### 1. System-wide: `/etc/gai.conf` — Prefer IPv4

Uncommented the recommended line to make `getaddrinfo()` return IPv4 addresses first:

```
precedence ::ffff:0:0/96  100
```

**File:** `/etc/gai.conf` (line 54)
**Effect:** All applications (curl, Firefox, Python, etc.) now prefer IPv4 over IPv6 system-wide.
**Persistent:** Yes — survives reboots.

### 2. Firefox: `user.js` — Disable IPv6 DNS

Defense-in-depth for Firefox's own resolver:

```javascript
// ~/.mozilla/firefox/kipclfop.default-release/user.js
user_pref("network.dns.disableIPv6", true);
```

### 3. Fixed: `prefs.js` owned by root

`prefs.js` was owned by root because Firefox was accidentally run as root during debugging. Fixed with:

```bash
chown brmz:brmz ~/.mozilla/firefox/kipclfop.default-release/prefs.js
```

**Lesson:** Never run Firefox as root. If Firefox breaks, check file ownership in `~/.mozilla/`.

## Reverting (if you connect to a network with real IPv6)

### Re-enable system IPv6 preference

In `/etc/gai.conf`, comment the line back out:

```
#precedence ::ffff:0:0/96  100
```

### Remove Firefox override

Delete or comment out the line in `~/.mozilla/firefox/kipclfop.default-release/user.js`.

## Verification

```bash
# Confirm IPv4 is returned first by getaddrinfo
python3 -c "import socket; print(socket.getaddrinfo('google.com', 443)[0])"
# Expected: (<AddressFamily.AF_INET: 2>, ...)

# Confirm IPv6 has no default route (expected on IPv4-only networks)
ip -6 route show | grep default || echo "no IPv6 default route"

# Test IPv4 connectivity
curl -4 --max-time 5 https://www.google.com -o /dev/null -w "%{http_code}"

# Test IPv6 connectivity (will fail on IPv4-only networks — expected)
curl -6 --max-time 5 https://www.google.com -o /dev/null -w "%{http_code}"
```

## If You Want Real IPv6 (Future)

Options, in order of effort:

| Option | How | Notes |
|--------|-----|-------|
| Enable WARP gateway mode | `warp-cli set-mode warp` | Blocked by Sidepocket org policy |
| Hurricane Electric tunnel | [tunnelbroker.net](https://tunnelbroker.net) free account + `sit` tunnel config | Requires IPv4 public IP |
| Wait for network upgrade | Ask BCH IT / ISP | Long term |
