#!/usr/bin/env bash
set -euo pipefail
control="$HOME/.config/mainframe/control"
[[ -x "$control" ]] || { echo 'Run ./apply.sh first.' >&2; exit 1; }
fc-cache -f "$HOME/.local/share/fonts/mainframe"
command -v bat >/dev/null && bat cache --build >/dev/null
"$control" stop
pkill -x waybar || true
"$control" start
hyprctl reload
swaync-client --skip-wait -R >/dev/null
swaync-client --skip-wait -rs >/dev/null
if command -v hyprpaper >/dev/null; then
  pkill -x hyprpaper || true
  nohup hyprpaper > "$HOME/.local/state/mainframe/hyprpaper.log" 2>&1 < /dev/null &
fi
printf 'Mainframe is active. Reopen terminal apps; restart Firefox to load its chrome CSS.\n'
