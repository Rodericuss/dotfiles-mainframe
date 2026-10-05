# Installation and operation

## Requirements

Use an existing Wayland session with **Hyprland's Lua configuration API**, tested on 0.56.2. Older `hyprland.conf` installations require a manual port. The installer does not replace monitor, input, device or workspace setup.

Required desktop tools: Python 3, `python-gobject`, `python-cairo`, GTK 3, `gtk-layer-shell`, Hyprland, Hyprpaper, Waybar, Rofi, SwayNC, Kitty, `pamixer`, `playerctl`, `wl-clipboard`, `cliphist`, `libnotify` and Fontconfig. Optional integrations use Fish, Starship, Neovim, Bat, Btop, Firefox, Sidebery and Herdr. Notification shortcuts use `nm-connection-editor` and `blueman-manager`; brightness uses `brightnessctl` on supported internal panels. A Nerd Font fallback supplies file icons in terminal applications.

On Arch, install missing packages using your normal package workflow. Package installation, account setup and editor plugin downloads are outside this installer.

## Apply

Run `./apply.sh --dry-run` to see every destination, then `./apply.sh`. The script copies theme files, installs the bundled fonts, merges a final Lua overlay into an existing `~/.config/hypr/hyprland.lua`, and appends a Kitty include. Existing application theme files such as Rofi, Waybar and Yazi are replaced after backup. It also updates Firefox profiles that contain `prefs.js`.

`./activate.sh` rebuilds font and Bat caches, reloads Hyprland, restarts the panel, Waybar and Hyprpaper, and starts SwayNC as the notification owner. It stops Mako for this session. It does not change service enablement. Reopen terminal applications to load their new themes and restart Firefox for its CSS.

The panel starts with Hyprland through the Lua overlay. Logs and user data are under `~/.local/state/mainframe/`; the local control socket is under `$XDG_RUNTIME_DIR/mainframe-$UID/`.

For clipboard history, your session must already run `wl-paste --watch cliphist store`. Start that watcher once through your existing autostart configuration. The theme does not start duplicate clipboard collectors.

## Editor integration

The supplied lazy.nvim specification is at `config/nvim/lua/custom/plugins/neobrutalist.lua`, matching the existing workstation's plugin layout. It overrides its prior theme integration and uses existing Cyberdream/Lualine plugin declarations. Import this spec in your own lazy.nvim setup if it is not already importing `custom.plugins`.

For another plugin manager, the colorscheme itself is independent:

```lua
vim.cmd.colorscheme('mainframe')
require('mainframe.ui').setup()
```

Lualine's theme is available as `mainframe`. Neo-tree in the screenshots belongs to the existing editor configuration and is not installed by this repository.

## Firefox

The installer enables user stylesheets and adds managed blocks to `userChrome.css`, `userContent.css` and `user.js`. If Sidebery is installed, its profile-specific extension UUID is detected and its UI is themed. Without Sidebery, native tabs remain visible. It sets a local Mainframe home page and session restoration at startup.

The dashboard also serves the same static page at `http://127.0.0.1:47831/`. This server binds only to loopback and serves only the home page; it does not expose the filesystem or task state. For a themed **new tab**, install [New Tab Override](https://addons.mozilla.org/firefox/addon/new-tab-override/) and set its custom URL to that address. The extension is optional and is not bundled or installed by `apply.sh`. It was configured on the reference workstation.

## Rollback

`./restore.sh --dry-run` lists file restoration. `./restore.sh` leaves focus mode, stops the Mainframe panel and SwayNC, restores backed-up files, reloads Hyprland and restarts Waybar. It restarts Mako if Mako was active when Mainframe first took over. Restart the desktop session to reload the original wallpaper and application processes.

The manifest is `~/.local/state/mainframe/restore.json`; backups are in its `backups/` directory. Keep these until you are satisfied. Reapply keeps the first backup, so rollback returns to the state before the theme's initial installation. Files created by the theme are removed; existing files are restored. User tasks and timer data remain in the state directory.

Firefox persists values from `user.js` into `prefs.js`. Restoring `user.js` does **not** reset those live preferences. To undo them, reset `toolkit.legacyUserProfileCustomizations.stylesheets`, `sidebar.position_start`, `sidebar.revamp`, `browser.startup.page` and `browser.startup.homepage` to your previous choices in `about:config`/Settings. Remove New Tab Override separately if you installed it for this theme. Restart Firefox afterward.

## Scope and customization

- Geometry is tuned for 1920 × 1080 at scale 1. Edit `config/hypr/mainframe.lua` for different logical dimensions; edit the dashboard sizes in `config/mainframe/shell.py` for smaller screens.
- GTK 3 widgets are themed. This is not a global GTK 4/libadwaita theme; SwayNC has its own GTK 4 stylesheet.
- Media controls display real playerctl data. With no player, the card explicitly shows an idle state. Calendar navigation does not imply calendar-provider integration.
- External-monitor brightness requires hardware support; unsupported screens receive an explanatory notification rather than a fabricated gauge value.
- Herdr is themed through its supported configuration tokens; its internal layout remains controlled by Herdr.
- Focus mode restores geometry, DND and bar visibility under ordinary use. Avoid manually toggling Waybar while focus mode is active.
