#!/usr/bin/env python3
"""Mainframe Latão · Hyprlock: desenha a parte estática da tela de bloqueio (mostrador,
placa, rótulos) por monitor e escreve backgrounds.conf para o hyprlock.conf.
Geometria copiada do artboard 'Hyprlock · Tela de bloqueio' (1920x1080, centro-relativa)."""
import json, math, os, subprocess
from pathlib import Path
import cairo
import gi
gi.require_version('Pango', '1.0'); gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

CACHE = Path.home()/'.cache/mainframe-lock'
FONT = 'IBM Plex Mono'
ADV = 0.6  # avanço do Plex Mono, em em

def rgb(h, a=1.0):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4)) + (a,)

def sh(*a):
    try: return subprocess.check_output(a, text=True, stderr=subprocess.DEVNULL, timeout=2).strip()
    except (OSError, subprocess.SubprocessError): return ''

def text(cr, s, x, base, size, color, ls=0.0, bold=False, anchor='left'):
    """Texto com letter-spacing via Pango (fallback de glifos); anchor left/right pela caixa CSS."""
    lay = PangoCairo.create_layout(cr)
    fd = Pango.FontDescription.from_string(f"{FONT} {'SemiBold' if bold else 'Regular'}")
    fd.set_absolute_size(size*Pango.SCALE); lay.set_font_description(fd)
    attrs = Pango.AttrList(); attrs.insert(Pango.attr_letter_spacing_new(int(ls*Pango.SCALE))); lay.set_attributes(attrs)
    lay.set_text(s, -1)
    w = lay.get_extents()[1].width/Pango.SCALE
    if anchor == 'right': x -= w
    cr.set_source_rgba(*rgb(color)); cr.move_to(x, base - lay.get_baseline()/Pango.SCALE)
    PangoCairo.show_layout(cr, lay)
    return x + w

def width(s, size, ls=0.0): return len(s)*(size*ADV + ls)

def status_values():
    net = ''
    for line in sh('nmcli', '-t', '-f', 'DEVICE,TYPE,STATE', 'dev').splitlines():
        dev, typ, state = (line.split(':') + ['', '', ''])[:3]
        if state == 'connected' and typ in ('wifi', 'ethernet'): net = dev; break
    opts = {k: sh('hyprctl', 'getoption', f'input:{k}', '-j') for k in ('kb_layout', 'kb_variant')}
    val = {k: (json.loads(v).get('str', '') if v else '') for k, v in opts.items()}
    lay = (val['kb_layout'].split(',')[0] or 'br').upper()
    var = (val['kb_variant'].split(',')[0] or ('abnt2' if lay == 'BR' else '')).upper()
    return net or '—', f'{lay}-{var}' if var else lay

def render(w, h, path, user, net, kb):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); cr = cairo.Context(s)
    cr.set_source_rgba(*rgb('#080705')); cr.paint()
    cx, cy = w/2, h/2
    X = lambda dx: cx + dx - 960   # coordenadas do artboard -> monitor (centradas)
    Y = lambda dy: cy + dy - 540

    # mostrador
    cr.set_line_width(1); cr.set_source_rgba(*rgb('#14120D')); cr.arc(cx, cy, 470, 0, 2*math.pi); cr.stroke()
    cr.set_line_width(1.5); cr.set_source_rgba(*rgb('#2A2419')); cr.arc(cx, cy, 400, 0, 2*math.pi); cr.stroke()
    for a in range(0, 360, 6):
        r = math.radians(a); L = 20 if a % 30 == 0 else 8
        cr.move_to(cx + math.cos(r)*400, cy + math.sin(r)*400)
        cr.line_to(cx + math.cos(r)*(400-L), cy + math.sin(r)*(400-L))
    cr.stroke()
    cr.set_line_width(2); cr.set_source_rgba(*rgb('#6E5836')); cr.arc(cx, cy, 440, math.pi*0.8, math.pi*1.15); cr.stroke()

    # placa do operador: left 660 top 560 w 600 h 199, borda 2px
    px, py, pw, ph = X(660), Y(560), 600, 199
    cr.set_source_rgba(*rgb('#15130E')); cr.rectangle(px, py, pw, ph); cr.fill()
    cr.set_line_width(2); cr.set_source_rgba(*rgb('#B8925A')); cr.rectangle(px+1, py+1, pw-2, ph-2); cr.stroke()
    for rx, ry in ((px+7, py+7), (px+pw-14, py+7), (px+7, py+ph-14), (px+pw-14, py+ph-14)):
        cr.arc(rx+3.5, ry+3.5, 3.5, 0, 2*math.pi); cr.fill()
    L, R = X(694), X(1226)
    text(cr, 'OPERADOR', L, Y(606), 11, '#B8925A', ls=4.4)
    text(cr, f'[{user.upper()}]', R, Y(606), 18, '#E9DFC8', anchor='right')
    text(cr, 'SENHA', L, Y(638), 11, '#B8925A', ls=4.4)
    # campo: fundo + borda 1px latão + linha inferior 2px (o hyprlock acende a linha por cima)
    cr.set_source_rgba(*rgb('#0D0C09')); cr.rectangle(L, Y(649), 532, 56); cr.fill()
    cr.set_line_width(1); cr.set_source_rgba(*rgb('#6E5836')); cr.rectangle(L+0.5, Y(649)+0.5, 531, 55); cr.stroke()
    cr.rectangle(L, Y(703), 532, 2); cr.fill()
    text(cr, '↵ destravar', L, Y(733), 12, '#6E5836')
    text(cr, 'esc limpar', R, Y(733), 12, '#6E5836', anchor='right')

    # selo TRAVADO (top-left 32/28, altura 32)
    tw = 14 + width('TRAVADO', 12, 3) + 14
    dw = 14 + width('desde 00:00', 12) + 14
    cr.set_source_rgba(*rgb('#C8743F')); cr.rectangle(33, 29, tw, 30); cr.fill()
    text(cr, 'TRAVADO', 47, 48, 12, '#0D0C09', ls=3, bold=True)
    cr.set_line_width(1); cr.set_source_rgba(*rgb('#3A3224')); cr.rectangle(32.5, 28.5, tw+dw+1, 31); cr.stroke()

    # barra de status (bottom-left 32/28); BAT é label vivo do hyprlock, NET/TECLADO vão no fundo
    cells = [('BAT', '100%'), ('NET', net), ('TECLADO', kb)]
    colors = ['#9EEA8E', '#5BA89B', '#B8925A']
    x0 = 32; top = h - 28 - 32; x = x0 + 1
    for i, (k, v) in enumerate(cells):
        cw = 14 + width(f'{k} {v}', 12) + 14
        if i:
            cr.set_source_rgba(*rgb('#3A3224')); cr.rectangle(x, top+1, 1, 30); cr.fill(); x += 1
            t = text(cr, k + ' ', x + 14, top + 20, 12, '#CFC4AA'); text(cr, v, t, top + 20, 12, colors[i])
        x += cw
    cr.set_line_width(1); cr.set_source_rgba(*rgb('#3A3224')); cr.rectangle(x0+0.5, top+0.5, x-x0, 31); cr.stroke()

    # rodapé
    text(cr, 'MAINFRAME LATÃO · TERMINAL Nº 07', w-32, h-31, 11, '#3A3224', ls=3.85, anchor='right')
    s.write_to_png(str(path))

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    mons = json.loads(sh('hyprctl', 'monitors', '-j') or '[]')
    user = os.environ.get('USER', 'operador'); net, kb = status_values()
    blocks = []
    for m in mons:
        w, h = round(m['width']), round(m['height'])
        p = CACHE/f"{m['name']}.png"; render(w, h, p, user, net, kb)
        blocks.append(f"background {{\n    monitor = {m['name']}\n    path = {p}\n    color = rgb(080705)\n}}\n")
    (CACHE/'backgrounds.conf').write_text('\n'.join(blocks))

if __name__ == '__main__':
    main()
