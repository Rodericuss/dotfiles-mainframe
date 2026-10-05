import json
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class InstallTests(unittest.TestCase):
 def test_reapply_preserves_backup_and_local_hypr_config(self):
  with tempfile.TemporaryDirectory() as folder:
   home=Path(folder);rofi=home/'.config/rofi/config.rasi';rofi.parent.mkdir(parents=True);rofi.write_text('original\n')
   hypr=home/'.config/hypr/hyprland.lua';hypr.parent.mkdir(parents=True);hypr.write_text('-- hardware settings belong to this machine\nhl.monitor({output="TEST",mode="preferred"})\n')
   kitty=home/'.config/kitty/kitty.conf';kitty.parent.mkdir(parents=True);kitty.write_text('map ctrl+x new_window\n')
   def apply(*args):subprocess.run(['python',str(ROOT/'scripts/install.py'),'--home',folder,*args],check=True,stdout=subprocess.DEVNULL)
   apply('--dry-run');self.assertFalse((home/'.config/mainframe').exists())
   apply();apply()
   self.assertEqual(hypr.read_text().count('-- BEGIN MAINFRAME INTEGRATION'),1)
   self.assertIn('output="TEST"',hypr.read_text())
   self.assertIn('map ctrl+x',kitty.read_text());self.assertEqual(kitty.read_text().count('include mainframe.conf'),1)
   manifest=json.loads((home/'.local/state/mainframe/restore.json').read_text())
   self.assertEqual(Path(manifest[str(rofi)]).read_text(),'original\n')
   self.assertIn(str(home), (home/'.config/hypr/hyprpaper.conf').read_text())
   apply('--restore')
   self.assertEqual(rofi.read_text(),'original\n');self.assertNotIn('MAINFRAME INTEGRATION',hypr.read_text());self.assertFalse((home/'.config/mainframe/shell.py').exists())
 def test_themes_firefox_profiles_in_legacy_and_xdg_locations(self):
  with tempfile.TemporaryDirectory() as folder:
   home=Path(folder)
   for root in ('.mozilla/firefox','.config/mozilla/firefox'):
    profile=home/root/'abc.default-release';profile.mkdir(parents=True);(profile/'prefs.js').write_text('')
   subprocess.run(['python',str(ROOT/'scripts/install.py'),'--home',folder],check=True,stdout=subprocess.DEVNULL)
   for root in ('.mozilla/firefox','.config/mozilla/firefox'):
    self.assertIn('BEGIN MAINFRAME FIREFOX',(home/root/'abc.default-release/chrome/userChrome.css').read_text())
