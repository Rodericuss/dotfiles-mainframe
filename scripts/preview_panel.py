#!/usr/bin/env python3
"""Render the real GTK panel with isolated sample tasks for public screenshots."""
import importlib.util,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('panel',ROOT/'config/mainframe/shell.py');panel=importlib.util.module_from_spec(spec);spec.loader.exec_module(panel)
with tempfile.TemporaryDirectory(prefix='mainframe-preview-') as folder:
 panel.STATE=Path(folder);panel.RUNTIME=Path(folder)
 panel.Shell.listen=lambda self:None;panel.Shell.serve_home=lambda self:None
 app=panel.Shell();app.tasks=[{'text':t,'done':i<3} for i,t in enumerate(['Paleta do Kitty','Ícones do SwayNC','Régua de volume','Bufferline no Neovim','CSS do Sidebery','Tema do Herdr','Testar modo foco'])];app.render_tasks()
 app.windows['dashboard'].show_all();panel.Gtk.main()
