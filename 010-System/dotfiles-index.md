---
title: "Dotfiles Index"
type: reference
created: 2026-03-19
updated: 2026-03-22
tags: [system, dotfiles, config]
---

# Dotfiles Index

Key configuration files on this machine.

---

## Shell

| File | Purpose |
|------|---------|
| `~/.zshrc` | Primary shell config (~23K). Powerlevel10k prompt, nvim as editor/pager, XDG dirs |
| `~/.bashrc` | Minimal bash config (21 bytes, essentially empty) |
| `~/.bash_profile` | Bash login config (119 bytes) |

**Shell environment highlights:**
- `EDITOR=nvim`, `VISUAL=nvim`, `MANPAGER='nvim +Man!'`
- XDG dirs configured: `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`
- Powerlevel10k instant prompt enabled

## Editor

| File/Dir | Purpose |
|----------|---------|
| `~/.config/nvim/` | Neovim config (primary editor) |

## Window Manager / Desktop

| File/Dir | Purpose |
|----------|---------|
| `~/.config/hypr/` | Hyprland WM config |
| `~/.config/waybar/` | Waybar status bar |
| `~/.config/rofi-wayland/` | Application launcher |
| `~/.config/swww/` | Wallpaper daemon |
| `~/.config/swayosd/` | OSD notifications |

## Audio

| File/Dir | Purpose |
|----------|---------|
| `~/.config/easyeffects/` | Audio effects and EQ |
| `~/.config/coppwr/` | PipeWire patchbay |

## Git

| File | Purpose |
|------|---------|
| `~/.gitconfig` | Global git config |

## Apps

| File/Dir | Purpose |
|----------|---------|
| `~/.config/obsidian/` | Obsidian config |
| `~/.config/1Password/` | 1Password desktop |
| `~/.config/gh/` | GitHub CLI |
| `~/.config/Code/` | VS Code settings |
| `~/.config/Signal Beta/` | Signal messenger |
| `~/.config/discord/` | Discord (via Vesktop) |
| `~/.config/spotify/` | Spotify client |

## Related

- [[arch-overview|Arch Overview]]
- [[packages-aur|AUR Packages]]
- [[hardware-specs|Hardware Specs]]
