---
title: "AUR / Foreign Packages"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [system, packages, aur]
---

# AUR / Foreign Packages

**Count:** 45 packages (as of 2026-03-22)
**AUR Helpers:** yay 12.5.7, paru 2.1.0

## Package List

```
1password 8.12.6-39
ani-cli 4.10-1
backslash-bin 0.2.2-1
brave-bin 1:1.88.132-1
cemu 2.6-4
citra 2:r10112.608383e-1
cloudflare-warp-bin 2026.1.150-1
electron39-bin 39.8.3-1
freesurfer-bin 8.1.0-1
fsl 6.0.7.18-1
gemini-cli-debug 1.0.3-3
jre-jetbrains 25.0.2b329.72-1
libelectron 2026.2-1
libjpeg6-turbo 1.5.3-3
libpng12 1.2.59-2
lobster-git r235.10f1bc7-1
neofetch 7.1.0-2
netflix 1.1.1-1
ngrok 3.37.2-1
noisetorch 0.12.2-4
nordvpn-bin 4.4.0-1
ookla-speedtest-bin 1.2.0-1
paru 2.1.0-2
protonup-qt 2.15.0-1
python-inputs 0.5-4
python-steam 1.6.1-1
qt5-location 5.15.18+kde+r7-2
qt5-remoteobjects 5.15.18-1
qt5-webchannel 5.15.18+kde+r3-1
qt5-webengine 5.15.19-4
r8168 8.055.00-1
slack-desktop 4.47.69-1
spring-boot-cli 3.2.0-1
sudachi-bin 1.0.14-1
tidal-hifi-bin 6.3.0-1
ttf-apple-emoji 18.4-3
ttf-meslo-nerd-font-powerlevel10k 2.3.3-1
uxplay 1:1.73.4-1
vercel 50.33.1-1
visual-studio-code-bin 1.112.0-1
vmware-keymaps 1.0-3
vmware-workstation 25H2-4
yay 12.5.7-1
zoom 6.7.5-1
zsh-theme-powerlevel10k-git r4304.ef83e13c-1
```

## Categories

| Category | Packages |
|----------|----------|
| **Browsers** | brave-bin |
| **Dev Tools** | gemini-cli-debug, paru, spring-boot-cli, vercel, visual-studio-code-bin, yay, backslash-bin |
| **Password Mgmt** | 1password |
| **Media/Streaming** | ani-cli, lobster-git, netflix, tidal-hifi-bin |
| **Communication** | slack-desktop, zoom |
| **Neuroimaging** | freesurfer-bin, fsl |
| **Gaming/Emulation** | cemu, citra, protonup-qt, sudachi-bin |
| **Virtualization** | vmware-workstation, vmware-keymaps, jre-jetbrains |
| **Networking** | cloudflare-warp-bin, ngrok, nordvpn-bin, ookla-speedtest-bin, r8168 |
| **Audio** | noisetorch |
| **Shell/Theme** | neofetch, ttf-apple-emoji, ttf-meslo-nerd-font-powerlevel10k, zsh-theme-powerlevel10k-git |
| **Libraries** | electron39-bin, libelectron, libjpeg6-turbo, libpng12, python-inputs, python-steam, qt5-* |
| **Casting** | uxplay |

## How to Refresh

```bash
pacman -Qm          # List all foreign packages
yay -Syu             # Update AUR packages
paru -Syu            # Alternative AUR helper
```

## Related

- [[arch-overview|Arch Overview]]
- [[maintenance-log|Maintenance Log]]
- [[hardware-specs|Hardware Specs]]
