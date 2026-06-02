---
title: "Hardware Specifications"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [system, hardware, specs]
---

# Hardware Specifications

## System

| Component | Value |
|-----------|-------|
| **Hostname** | `OGLOQ` |
| **Chassis** | Laptop (ASUS ROG or similar, AMD + NVIDIA combo) |
| **OS** | Arch Linux |
| **Kernel** | 6.18.18-1-lts |

## CPU

| Spec | Value |
|------|-------|
| Model | AMD Ryzen 7 7840HS w/ Radeon 780M Graphics |
| Architecture | x86_64 |
| Cores | 8 (16 threads) |
| Base/Max | 419 MHz -- 5138 MHz |
| Cache | L1d 256 KiB, L1i 256 KiB, L2 8 MiB, L3 16 MiB |
| Virtualization | AMD-V |
| NUMA nodes | 2 |

## Memory

| Spec | Value |
|------|-------|
| Total | 38.4 GiB (~40 GB) |
| Swap | 8 GB swapfile at `/swapfile` |

## Storage

```
nvme0n1       1.9T   (primary, Linux)
+-nvme0n1p1     1G   /boot  (vfat, EFI)
+-nvme0n1p2   1.9T   /      (ext4)

nvme1n1     953.9G   (secondary, Windows dual-boot)
+-nvme1n1p1    16M   (reserved)
+-nvme1n1p2 953.1G   (ntfs, Windows)
+-nvme1n1p3   730M   (ntfs, recovery)
```

| Detail | Value |
|--------|-------|
| Primary NVMe | MAXIO Technology MAP1202 (DRAM-less), 1.9T |
| Secondary NVMe | 953.9G, NTFS (Windows dual-boot, unmounted) |
| Usage | ~573G used (33%) on primary, as of 2026-03-19 |

## GPU

| GPU | Model | Notes |
|-----|-------|-------|
| Discrete | NVIDIA GeForce RTX 4060 Max-Q / Mobile (AD107M) | CUDA 12.8 capable |
| Integrated | AMD/ATI Phoenix1 (Radeon 780M) | Display output |

## Network Adapters

| Adapter | Type | Details |
|---------|------|---------|
| wlan0 | Wi-Fi | Realtek RTL8852BE PCIe 802.11ax |
| eth0 | Ethernet | Realtek RTL8111/8168/8211/8411 PCIe Gigabit |

## Audio

| Component | Details |
|-----------|---------|
| NVIDIA HD Audio | AD107 High Definition Audio Controller |
| AMD HD Audio | Family 17h/19h/1ah HD Audio Controller |
| ACP | AMD ACP/ACP3X/ACP6x Audio Coprocessor |
| Pipeline | PipeWire + WirePlumber |

## Other

| Component | Details |
|-----------|---------|
| USB | USB 3.2 Gen2 xHCI + USB4/Thunderbolt NHI |
| Security | AMD Platform Security Processor |
| Sensors | AMD Sensor Fusion Hub (V2) |
| Ethernet driver | r8168 (AUR, for Realtek NIC) |

## Related

- [[arch-overview|Arch Overview]]
- [[../020-Infrastructure/networking|Networking]]
- [[packages-aur|AUR Packages]]
