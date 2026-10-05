#!/usr/bin/env python3
"""Explicit local theme deployment with a persistent per-file rollback manifest."""
import argparse,datetime,json,os,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--dry-run',action='store_true');p.add_argument('--restore',action='store_true');p.add_argument('--home',type=Path,default=Path.home());a=p.parse_args()
home=a.home;state=home/'.local/state/mainframe';manifest_path=state/'restore.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
backup=state/'backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
def write(target,data,mode=0o644):
 if a.dry_run:print('WRITE',target);return
 if str(target) not in manifest:
  if target.exists() or target.is_symlink():
   saved=backup/str(len(manifest));saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved,follow_symlinks=False);manifest[str(target)]=str(saved)
  else:manifest[str(target)]=None
  state.mkdir(parents=True,exist_ok=True);temp=manifest_path.with_suffix('.tmp');temp.write_text(json.dumps(manifest,indent=2));temp.replace(manifest_path)
 target.parent.mkdir(parents=True,exist_ok=True)
 tmp=target.with_name(target.name+'.mainframe-tmp');tmp.write_bytes(data);tmp.chmod(mode);tmp.replace(target)
 print('OK',target)
def block(old,name,text):
 begin=f'/* BEGIN {name} */';end=f'/* END {name} */'
 old=re.sub(re.escape(begin)+'.*?'+re.escape(end)+'\n?','',old,flags=re.S)
 return old.rstrip()+'\n'+begin+'\n'+text.rstrip()+'\n'+end+'\n'
def read(p):return p.read_text() if p.exists() else ''
if a.restore:
 for name,saved in reversed(list(manifest.items())):
  target=Path(name)
  if a.dry_run:print('RESTORE',target);continue
  if saved:
   if target.is_symlink():target.unlink()
   shutil.copy2(saved,target,follow_symlinks=False)
  else:target.unlink(missing_ok=True)
 if not a.dry_run and manifest_path.exists():manifest_path.rename(state/('restored-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.json'))
 sys.exit(0)
for src in sorted((ROOT/'config').rglob('*')):
 if not src.is_file() or '__pycache__' in src.parts:continue
 if src.relative_to(ROOT/'config').as_posix() in ('hypr/hyprland.lua','kitty/kitty.conf'):continue
 data=src.read_bytes()
 if src.name=='hyprpaper.conf':data=('splash = false\nwallpaper {\n    monitor =\n    path = '+str(home/'.config/mainframe/wallpaper.png')+'\n}\n').encode()
 write(home/'.config'/src.relative_to(ROOT/'config'),data,0o755 if src.name in ('control','volume-bar','clock') else 0o644)
for src in sorted((ROOT/'fonts').glob('*')):write(home/'.local/share/fonts/mainframe'/src.name,src.read_bytes())
# Preserve existing Kitty keymaps, shell integration and local settings.
kitty=home/'.config/kitty/kitty.conf';old=read(kitty)
old=old.replace('# Mainframe Latão theme overlay\n','')
old=re.sub(r'^include (?:neobrutal|mainframe)\.conf\s*$', '', old, flags=re.M)
write(kitty,(old.rstrip()+'\n\n# Mainframe Latão theme overlay\ninclude mainframe.conf\n').encode())
# Add the Lua theme last, keeping hardware/input/workspace configuration intact.
hypr=home/'.config/hypr/hyprland.lua';old=read(hypr)
if old:
 if '-- Mainframe Latão: the final visual settings' in old:old=old[:old.index('-- Mainframe Latão: the final visual settings')]
 old=re.sub(r'-- BEGIN MAINFRAME INTEGRATION.*?-- END MAINFRAME INTEGRATION\n?', '', old,flags=re.S)
 # These shortcuts are intentionally supplied by the theme, not registered twice.
 old='\n'.join(line for line in old.splitlines() if not (line.strip().startswith('hl.bind(') and any(x in line for x in ['"SUPER + TAB"','"SUPER + T"','"SUPER + N"','"SUPER + ALT + F"','"XF86MonBrightnessUp"','"XF86MonBrightnessDown"','"XF86AudioRaiseVolume"','"XF86AudioLowerVolume"','"XF86AudioMute"','"XF86AudioMicMute"','"F7"','"SUPER + SPACE"','"SUPER + O"','mainMod .. " + SPACE"','mainMod .. " + O"'])))
 old='\n'.join(line for line in old.splitlines() if 'hl.exec_cmd("~/.config/mainframe/control start")' not in line and 'hl.exec_cmd("~/.config/neobrutal/control start")' not in line)
 old+='\n-- BEGIN MAINFRAME INTEGRATION\ndofile(os.getenv("HOME") .. "/.config/hypr/mainframe.lua")\n-- END MAINFRAME INTEGRATION\n'
 write(hypr,old.encode())
else:print('Hyprland: no existing Lua config; source ~/.config/hypr/mainframe.lua manually.')
# Compatibility entry points for existing startup commands and launchers.
for name,command in [('control','"$@"')]:
 write(home/'.config/neobrutal'/name,b'#!/usr/bin/env bash\nexec "$HOME/.config/mainframe/control" "$@"\n',0o755)
write(home/'scripts/f1_hypr_conf.sh',b'#!/usr/bin/env bash\nexec "$HOME/.config/mainframe/control" focus\n',0o755)
# Match installed profiles, including Firefox profile groups absent in profiles.ini.
for profile in sorted(p for root in ('.mozilla/firefox','.config/mozilla/firefox') for p in (home/root).glob('*')):
 prefs=profile/'prefs.js'
 if not profile.is_dir() or not prefs.exists():continue
 uuid=None
 for match in re.finditer(r'user_pref\("extensions.webextensions.uuids",\s*("(?:\\.|[^"\\])*")\s*\);',read(prefs)):
  try:uuid=json.loads(json.loads(match.group(1))).get('{3c078156-979c-498b-8990-85f7987dd929}')
  except (ValueError,AttributeError):pass
 css=(ROOT/'config/firefox/userChrome.css').read_text()
 if not uuid:css=css.replace('#TabsToolbar { display:none !important; }','').replace('#sidebar-header { display:none !important; }','')
 chrome=profile/'chrome/userChrome.css';old=read(chrome)
 old=re.sub(r'/\* BEGIN NEOBRUTAL FIREFOX \*/.*?/\* END NEOBRUTAL FIREFOX \*/','',old,flags=re.S)
 if old.startswith('/* Neobrutal browser chrome.'):old=''
 write(chrome,block(old,'MAINFRAME FIREFOX',css).encode())
 content=profile/'chrome/userContent.css';old=read(content);old=re.sub(r'/\* BEGIN NEOBRUTAL SIDEBERY \*/.*?/\* END NEOBRUTAL SIDEBERY \*/','',old,flags=re.S)
 css='@-moz-document url("about:blank"),url("about:newtab"),url("about:home") { html,body { background:#0D0C09 !important; color:#CFC4AA !important; } }\n'
 if uuid and re.fullmatch('[a-fA-F0-9-]{36}',uuid):css+='@-moz-document url-prefix("moz-extension://'+uuid+'/") {\n'+(ROOT/'config/firefox/sidebery.css').read_text()+'\n}\n'
 write(content,block(old,'MAINFRAME CONTENT',css).encode())
 user=profile/'user.js';settings='user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);\nuser_pref("sidebar.position_start", true);\nuser_pref("sidebar.revamp", false);\nuser_pref("browser.startup.page", 3);\nuser_pref("browser.startup.homepage", '+json.dumps((home/'.config/mainframe/home.html').as_uri())+');\n'
 write(user,block(read(user),'MAINFRAME PREFERENCES',settings).encode())
print('Manifest:',manifest_path)
