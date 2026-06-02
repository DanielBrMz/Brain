---
title: "Known Issues — Non-Actionable"
type: reference
created: 2026-03-19
updated: 2026-03-19
tags: [system, issues, cosmetic]
---

# Known Issues — Non-Actionable

All items below are confirmed cosmetic or firmware-level — no user action required.

---

## ACPI / BIOS Errors on Boot

**Symptom:** Boot log shows errors like:
```
ACPI Error: \_SB.PCI0.GP18.SATA ...
ACPI Error: WLAN._S0W ...
ACPI Error: PEGP.GPS ...
```

**Cause:** Firmware bugs in the BIOS ACPI tables. Very common on consumer hardware.

**Impact:** None — these do not affect functionality or stability.

**Action:** None. Cannot be fixed without a BIOS update from the manufacturer.

---

## Duplicate D-Bus Name: org.freedesktop.FileManager1

**Symptom:** Journal may show:
```
Failed to activate service 'org.freedesktop.FileManager1': timed out
```
or duplicate name warnings.

**Cause:** Multiple file managers (e.g., Nautilus, Thunar) both registering the same D-Bus name.

**Impact:** Cosmetic. File manager operations work normally.

**Action:** None unless file manager behavior is broken.

---

## Bluetooth: Failed to set default system config for hci0

**Symptom:**
```
Failed to set default system config for hci0
```

**Cause:** BlueZ config mismatch or incomplete adapter initialization. Common with certain adapters.

**Impact:** Bluetooth continues to function. Pairing and connections work normally.

**Action:** None unless BT issues arise. If BT stops working, investigate `/etc/bluetooth/main.conf`.

---

## Resolved Issues (archived here for reference)

| Issue | Resolution | Date |
|-------|-----------|------|
| `wg-quick@bch.service` failing | Disabled — config was missing/invalid | 2026-03-19 |
| 29 orphaned packages | Removed via `pacman -Rns` | 2026-03-19 |
| No swap configured | 8GB swapfile created and activated | 2026-03-19 |
| Firefox no internet on IPv4-only networks | gai.conf IPv4 preference + Firefox user.js | 2026-03-30 |
| SDDM intermittent boot failure (multi-reboot) | GPU primary config + early KMS + pacman hook — see [[gpu-hybrid-fix]] | 2026-04-23 |
| WiFi capped at 54 Mbps (Comcast HT-MCS bug) | Patched mac80211 in /updates/ + rtw89 ASPM/PS options — see [[wifi-fix]] | 2026-05-03 |
| Integrated camera USB autosuspend disconnect | udev rule: /etc/udev/rules.d/50-camera-autosuspend.rules | 2026-05-03 |
