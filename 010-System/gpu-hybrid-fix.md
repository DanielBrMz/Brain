---
title: "Hybrid GPU Boot Fix — AMD iGPU Primary + NVIDIA PRIME Offload"
type: reference
created: 2026-04-23
updated: 2026-04-23
tags: [system, gpu, nvidia, amd, sddm, boot]
---

# Hybrid GPU Boot Fix

## Problem

SDDM required multiple reboots (up to 11 attempts) to display the login screen. Root cause: Xorg picked the NVIDIA dGPU (`card0`) as primary, but the laptop panel is physically wired to the AMD iGPU (`card1`). NVIDIA reported `Cannot find any crtc or sizes` → black screen.

## Hardware

- **AMD iGPU:** Phoenix1 (PCI 06:00.0) — drives the laptop panel
- **NVIDIA dGPU:** RTX 4060 Max-Q (PCI 01:00.0) — available via PRIME offload

## Fix (4 layers)

### 1. Xorg GPU Config
**File:** `/etc/X11/xorg.conf.d/10-gpu-primary.conf`

Forces AMD iGPU as primary display. NVIDIA is still available but doesn't claim the screen.

### 2. Early KMS
**File:** `/etc/mkinitcpio.conf` → `MODULES=(amdgpu)`

Loads AMD GPU driver in initramfs so the display is ready before SDDM starts.

### 3. NVIDIA DRM Modesetting
**Files:**
- `/etc/default/grub` → `nvidia-drm.modeset=1` kernel param
- `/etc/modprobe.d/nvidia-drm.conf` → `options nvidia-drm modeset=1` (redundant, survives GRUB changes)

### 4. Pacman Hook (self-healing)
**Files:**
- `/etc/pacman.d/hooks/90-nvidia-update.hook` — triggers on nvidia/kernel/mkinitcpio updates
- `/usr/local/bin/gpu-boot-verify` — verification script that:
  - Re-adds `amdgpu` to MODULES if missing (pacnew overwrite protection)
  - Restores nvidia-drm.modeset if missing
  - Regenerates Xorg GPU config if deleted
  - Regenerates initramfs + GRUB
  - Warns if `/boot` exceeds 80%

## Using the NVIDIA GPU

```bash
# Gaming / OpenGL / Vulkan rendering
prime-run <application>

# CUDA / PyTorch (works without prime-run)
python train.py          # CUDA finds the GPU automatically
nvidia-smi               # Always available

# Verify
__NV_PRIME_RENDER_OFFLOAD=1 glxinfo | grep "OpenGL renderer"
```

## Boot Partition Space

`/boot` is 1GB (EFI). Fallback presets disabled for both kernels to save ~189MB. Two kernels installed (`linux` + `linux-lts`). If space becomes tight, remove the unused `linux` package.

## Maintenance

None required — the pacman hook handles updates automatically. If boot issues recur:

```bash
# Manual verification
sudo /usr/local/bin/gpu-boot-verify
```
