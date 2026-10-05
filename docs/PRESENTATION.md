<p align="center"><img src="images/wordmark.svg" alt="Mainframe Latão wordmark" width="100%"></p>

# Mainframe Latão — theme presentation

*A brass-and-phosphor desktop for deliberate work.*

[Open the standalone slide deck](presentation.html) after cloning or downloading this repository. Arrow keys navigate; **F** enters fullscreen.

The idea is an instrument panel that happens to be a workstation. Brass marks the structure, copper identifies the active control, and phosphor green is reserved for the values that need attention. Empty space is part of the composition: on the reference 32-inch display, the wallpaper remains visible around the dashboard and the Yazi scratchpad.

![Dashboard and wallpaper](images/dashboard.png)

**01 — The command desk.** The panel brings together a clock, live CPU and memory, a Pomodoro timer, player information, persistent tasks and a navigable calendar. The screenshot uses isolated sample tasks; the installed dashboard loads the user's own state.

![Yazi](images/yazi.png)

**02 — Navigation.** Yazi extends the same palette to directory names, selection, search, status and code previews. The scratchpad is 1160 × 740 logical pixels at the reference resolution and sits over the wallpaper.

![Neovim](images/neovim.png)

**03 — Creation.** Neovim has a native colorscheme, rectangular buffer tabs and a matching Lualine palette. The file tree in this capture comes from the existing editor setup.

![Firefox](images/firefox.png)

**04 — Research.** Firefox and Sidebery frame a local start page with a live clock, search and direct links. The page is available only on the workstation's loopback address when the Mainframe panel runs.

![Launcher](images/launcher.png)

**05 — Control.** Rofi is compact, typographic and keyboard-led. The system remains consistent through the notification center, volume OSD and Fish prompt.

![Focus](images/focus.png)

**06 — Focus.** F8 keeps windows tiled, opens generous margins, hides Waybar, enables do-not-disturb and shows an elapsed HUD. The floating Yazi scratchpad moves to the upper-left edge of the work area. F7 can switch a separately installed Hyprland config pair.

![Volume gauge](images/volume.png)

**07 — Feedback.** A small analog gauge makes volume changes visible without occupying the desktop. The readings come from the real audio device.

## Materials

| Material | Color | Function |
| :--- | :--- | :--- |
| Blackened steel | `#0D0C09` | Canvas |
| Dark enamel | `#15130E` | Surface |
| Brushed brass | `#B8925A` | Structure |
| Warm copper | `#C8743F` | Action |
| Phosphor | `#9EEA8E` | Signal |
| Parchment | `#E9DFC8` | Text |

The exact surfaces and setup instructions are in the [project README](../README.md) and [installation guide](INSTALL.md). The bundled IBM Plex fonts are under the [SIL Open Font License](../fonts/OFL.txt).
