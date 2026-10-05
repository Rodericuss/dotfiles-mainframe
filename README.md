# Mainframe Latão

![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=flat-square&logo=archlinux&logoColor=white)
![Hyprland](https://img.shields.io/badge/Hyprland-58E1FF?style=flat-square&logo=hyprland&logoColor=black)
![Neovim](https://img.shields.io/badge/Neovim-57A143?style=flat-square&logo=neovim&logoColor=white)
![Fish](https://img.shields.io/badge/Fish_Shell-4AAE46?style=flat-square&logo=fishshell&logoColor=white)
![License](https://img.shields.io/badge/License-OFL_·_MIT-B8925A?style=flat-square)

**A brass-and-phosphor desktop for deliberate work.**

Mainframe Latão brings the visual language of analog instruments to a modern Hyprland desktop: near-black panels, fine brass rules, copper controls and luminous green selections. Windows tile with fine gaps that leave room for the wallpaper and for your attention; only the Yazi scratchpad floats.

![Mainframe dashboard](docs/images/dashboard.png)

Designed from the supplied Mainframe HTML and screenshot references, then implemented and checked in a running Arch Linux session. The desktop keeps its Portuguese labels; this project presentation is in English.

[Installation and rollback](docs/INSTALL.md)

## The desktop

| Surface | Included behavior |
| --- | --- |
| Hyprland / Hyprpaper | Sharp borders, opaque surfaces, tiled windows with a floating Yazi scratchpad, instrument wallpaper |
| Waybar | Roman workspaces, live CPU/RAM, segmented volume, network and clock |
| Dashboard | Live clock and system readings, persistent tasks, Pomodoro timer, calendar, playerctl media controls |
| Focus mode | Tiled windows with wide gaps, hidden bar, do-not-disturb, elapsed-time HUD, Yazi parked top-left |
| Rofi / clipboard | Application modes, searchable clipboard, pin/delete/copy actions |
| SwayNC | Compact notification center, volume, focus and mute controls |
| Kitty / Fish / Starship | IBM Plex Mono, block cursor, coordinated shell and prompt |
| Neovim | Native colorscheme, rectangular buffer tabs, Lualine integration, editor focus mode |
| **Yazi** | Phosphor selection, brass directories, copper search, square status line and themed code previews |
| Firefox / Sidebery | Brass browser chrome, vertical tabs, local clock/search home page |
| Herdr / Bat / Btop / GTK 3 | Matching application colors, syntax previews, system monitor and widgets |

### File navigation

![Yazi with Mainframe theme](docs/images/yazi.png)

### Editing

![Neovim with Mainframe theme](docs/images/neovim.png)

### Browser

![Firefox and Sidebery](docs/images/firefox.png)

### Launch and focus

| Launcher | Focus mode |
| --- | --- |
| ![Rofi](docs/images/launcher.png) | ![Focus mode](docs/images/focus.png) |

### Volume OSD

![Volume instrument OSD](docs/images/volume.png)

## Design language

| Token | Value | Role |
| --- | --- | --- |
| Near black | `#0D0C09` | Desktop and terminal canvas |
| Panel | `#15130E` | Cards and controls |
| Brass | `#B8925A` | Borders, labels and structure |
| Copper | `#C8743F` | Active window and actions |
| Phosphor | `#9EEA8E` | Selection, clock and live values |
| Parchment | `#E9DFC8` | Primary text |
| Patina | `#5BA89B` | Media and secondary information |

IBM Plex Mono and IBM Plex Sans Condensed are bundled under the SIL Open Font License. Two-pixel outlines, square corners and opaque backgrounds keep the interface crisp.

The reference workstation is a **32-inch display at 1920 × 1080, scale 1**. Applications tile; the floating Yazi scratchpad is 1160 × 740. Physical screen size alone does not determine UI scale; adjust these logical-pixel sizes for other resolutions and scale factors.

## Quick start

This is a theme overlay for an existing Arch/Hyprland Lua desktop. It does not provision a fresh OS or install application packages. Read the [requirements and integration notes](docs/INSTALL.md) first.

```sh
git clone https://github.com/Rodericuss/dotfiles-mainframe.git
cd dotfiles-mainframe
./apply.sh --dry-run
./apply.sh
./activate.sh
```

The installer backs up every managed file before its first replacement. Reapplying preserves that original backup. Existing Hyprland hardware configuration and Kitty keymaps are retained; theme-owned application configuration files are replaced.

| Shortcut | Action |
| --- | --- |
| `Super + Tab` / `Super + T` | Dashboard |
| `Super + Space` | Application launcher |
| `Super + O` | Clipboard history |
| `Super + N` | Notification center |
| `F7` | Swap `hypr_config1.lua`/`hypr_config2.lua` when present; otherwise window focus mode |
| `F8` | Focus mode: windows stay tiled with wide gaps, bar hidden, DND, elapsed-time HUD; the Yazi scratchpad parks top-left |
| Media volume keys | Volume and instrument OSD |
| `:MainframeFocus` / `<leader>uz` | Neovim focus mode |

```sh
./restore.sh --dry-run
./restore.sh
```

See the rollback notes for browser preferences and the optional new-tab extension.

## Validation

Tested in the actual Wayland session with Hyprland 0.56.2, Kitty 0.48.2, Rofi 2.0.0, Waybar 0.15.0, SwayNC 0.12.6 and Yazi 26.9.1. Screenshots are real `grim` captures; dashboard tasks are isolated sample data. No personal browser tabs or conversations are included.

Automated checks cover installer dry-run, repeated application, backup restoration, task persistence, timer completion and calendar boundaries. Live checks cover compositor configuration, Yazi startup, focus round-trips with tiled windows and the Yazi scratchpad, volume display and Firefox new-tab routing.

```sh
python -m unittest discover -s tests -v
```

## Credits

Based on the Mainframe Latão reference artwork and HTML supplied for this project. Built on [Hyprland](https://hypr.land), [Yazi](https://yazi-rs.github.io), [IBM Plex](https://github.com/IBM/plex), GTK and the applications listed above. [New Tab Override](https://addons.mozilla.org/firefox/addon/new-tab-override/) is an optional, separately installed Firefox adapter.

Fonts retain their [OFL license](fonts/OFL.txt). Upstream applications and reference artwork retain their respective rights.
