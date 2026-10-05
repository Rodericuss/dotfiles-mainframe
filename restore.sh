#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ "${1:-}" == '--dry-run' ]]; then
  exec python scripts/install.py --restore --dry-run
fi
if [[ -x "$HOME/.config/mainframe/control" ]]; then
  if [[ "$("$HOME/.config/mainframe/control" focus-status)" == true ]]; then
    "$HOME/.config/mainframe/control" focus
  fi
  "$HOME/.config/mainframe/control" stop
fi
systemctl --user stop swaync.service || true
pkill -x swaync || true
pkill -x waybar || true
python scripts/install.py --restore
python - <<'PY'
import json,subprocess
from pathlib import Path
p=Path.home()/'.local/state/mainframe/services.json'
if p.exists():
    state=json.loads(p.read_text())
    if state.get('is-active')=='active':
        subprocess.run(['systemctl','--user','start','mako.service'])
    p.rename(p.with_name('services-restored.json'))
PY
hyprctl reload
nohup waybar > /tmp/mainframe-restored-waybar.log 2>&1 < /dev/null &
printf 'Configuration files restored. Restart your desktop session and browser. See docs/INSTALL.md for Firefox preference and add-on rollback.\n'
