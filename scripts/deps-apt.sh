#!/usr/bin/env bash
# Mainframe Latão on Debian/Ubuntu: install the desktop tools with apt and the Firefox add-ons
# by policy. Arch users install the same tools with pacman (see docs/INSTALL.md).
# Usage: ./scripts/deps-apt.sh [--dry-run]
set -euo pipefail
command -v apt-get >/dev/null || { echo 'apt-get not found: this script is for Debian/Ubuntu.' >&2; exit 1; }
dry=''; [[ "${1:-}" == '--dry-run' ]] && dry=echo

required=(python3 python3-gi python3-gi-cairo python3-cairo gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1
  hyprland hyprpaper hyprlock waybar rofi sway-notification-center kitty pamixer playerctl
  wl-clipboard cliphist libnotify-bin fontconfig xdg-desktop-portal-hyprland hyprpolkitagent)
optional=(fish starship neovim bat btop firefox network-manager-gnome blueman brightnessctl
  fonts-noto-color-emoji)

$dry sudo apt-get update
$dry sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "${required[@]}" "${optional[@]}"

# Debian ships bat as batcat; activate.sh and the shell config call it bat.
if command -v batcat >/dev/null && ! command -v bat >/dev/null; then
  $dry mkdir -p "$HOME/.local/bin"
  $dry ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
fi

# Firefox add-ons used by the theme (Sidebery, Tridactyl) plus the pt-BR dictionary. The policy file
# is read by both the deb and the snap Firefox; it is replaced, so merge by hand if you keep your own.
policy=/etc/firefox/policies/policies.json
amo=https://addons.mozilla.org/firefox/downloads/latest
read -r -d '' policies <<EOF || true
{
  "policies": {
    "ExtensionSettings": {
      "{3c078156-979c-498b-8990-85f7987dd929}": {"installation_mode": "normal_installed", "install_url": "$amo/sidebery/latest.xpi"},
      "tridactyl.vim@cmcaine.co.uk": {"installation_mode": "normal_installed", "install_url": "$amo/tridactyl-vim/latest.xpi"},
      "pt-BR@dictionaries.addons.mozilla.org": {"installation_mode": "normal_installed", "install_url": "$amo/corretor/latest.xpi"}
    }
  }
}
EOF
if [[ -n "$dry" ]]; then echo "WRITE $policy"; else
  sudo mkdir -p "$(dirname "$policy")"
  printf '%s\n' "$policies" | sudo tee "$policy" >/dev/null
fi

missing=()
command -v yazi >/dev/null || missing+=('yazi (not in apt: snap install yazi --classic, or cargo)')
command -v herdr >/dev/null || missing+=('herdr (install from its release page)')
((${#missing[@]})) && printf 'Not installed by apt:\n' && printf '  - %s\n' "${missing[@]}"

# The theme overlay merges into ~/.config/hypr/hyprland.lua, Hyprland's Lua configuration API.
version=$(Hyprland --version 2>/dev/null | sed -n 's/^Hyprland \([0-9.]*\).*/\1/p' || true)
if [[ -n "$version" ]] && [[ "$(printf '%s\n0.56.0\n' "$version" | sort -V | head -1)" != 0.56.0 ]]; then
  echo "Warning: Hyprland $version from apt; the Lua overlay was tested on 0.56.2 and older releases only read hyprland.conf." >&2
fi
echo 'Next: open Firefox once so it creates a profile, then ./apply.sh and, inside Hyprland, ./activate.sh.'
