import importlib.util
import tempfile
import time
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('panel',ROOT/'config/mainframe/shell.py');panel=importlib.util.module_from_spec(spec);spec.loader.exec_module(panel)
class PanelTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();panel.STATE=Path(cls.temp.name);panel.RUNTIME=panel.STATE
  panel.run=lambda *args:'';panel.launch=lambda *args:None
  panel.Shell.listen=lambda self:None;panel.Shell.poll=lambda self:None;panel.Shell.serve_home=lambda self:None
  cls.app=panel.Shell()
 @classmethod
 def tearDownClass(cls):
  for w in cls.app.windows.values():w.destroy()
  cls.temp.cleanup()
 def test_task_crud_and_persistence(self):
  a=self.app;a.tasks=[];a.entry.set_text('Validate the copper focus border');a.add_task(a.entry)
  self.assertEqual(a.tasks[0]['text'],'Validate the copper focus border')
  a.complete(0,True);self.assertIn('"done": true',(panel.STATE/'tasks.json').read_text())
  self.assertEqual(a.task_count.get_text(),'1 / 1');a.remove_task(0);self.assertEqual(a.tasks,[])
 def test_calendar_year_boundary_and_leap_day(self):
  a=self.app;a.cal_year=2026;a.cal_month=12;a.change_month(1);self.assertEqual((a.cal_year,a.cal_month),(2027,1))
  a.cal_year=2024;a.cal_month=2;a.render_calendar();self.assertIn('29',[c.get_text() for c in a.cal_grid.get_children()])
 def test_timer_completion_and_persistence(self):
  a=self.app;a.set_timer('Foco',25);a.toggle_timer();self.assertTrue(a.running)
  a.deadline=time.time()-1;a.tick();self.assertFalse(a.running);self.assertEqual(a.remaining,0);self.assertEqual(a.cycle,2)
  self.assertIn('"running": false',(panel.STATE/'timer.json').read_text())
