#!/usr/bin/env python3
import json,subprocess
try:
 v=int(subprocess.check_output(['pamixer','--get-volume'],text=True));mute=subprocess.check_output(['pamixer','--get-mute'],text=True).strip()=='true'
 full=min(10,max(0,round(v/10)))
 print(json.dumps({'text':('VOL ▯▯▯▯▯▯▯▯▯▯ MUDO' if mute else 'VOL <span foreground="#C8743F">'+'▮'*full+'▯'*(10-full)+'</span> '+str(v)), 'class':'muted' if mute else 'active','tooltip':'Volume · rolar para ajustar · clique para silenciar'}))
except (OSError,ValueError,subprocess.SubprocessError):print(json.dumps({'text':'VOL —','class':'unavailable'}))
