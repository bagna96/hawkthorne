#!/usr/bin/env python3
"""Genera i fogli-contatti della LIBRERIA TSR (assets/guest/src_tsr/<gioco>/)
→ scratchpad/catalogo_<gioco>.jpg, con nome e dimensioni per ogni sheet."""
import os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'assets', 'guest', 'src_tsr')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'

THUMB_W, THUMB_H, COLS = 200, 150, 5
for gioco in sorted(os.listdir(SRC)):
    gdir = os.path.join(SRC, gioco)
    if not os.path.isdir(gdir): continue
    files = sorted(f for f in os.listdir(gdir) if f.endswith('.png'))
    if not files: continue
    rows = (len(files) + COLS - 1) // COLS
    sheet = Image.new('RGB', (COLS * (THUMB_W + 8) + 8, rows * (THUMB_H + 34) + 40), (30, 30, 48))
    d = ImageDraw.Draw(sheet)
    d.text((8, 6), gioco.upper() + '  (%d sheet)' % len(files), fill=(245, 212, 66))
    for i, f in enumerate(files):
        try:
            im = Image.open(os.path.join(gdir, f)).convert('RGBA')
        except Exception:
            continue
        w0, h0 = im.size
        r = min(THUMB_W / w0, THUMB_H / h0, 1.0)
        im = im.resize((max(1, int(w0 * r)), max(1, int(h0 * r))))
        x = 8 + (i % COLS) * (THUMB_W + 8)
        y = 28 + (i // COLS) * (THUMB_H + 34)
        d.rectangle([x, y, x + THUMB_W, y + THUMB_H], fill=(24, 24, 40))
        sheet.paste(im, (x + (THUMB_W - im.size[0]) // 2, y + (THUMB_H - im.size[1]) // 2), im)
        d.text((x, y + THUMB_H + 3), f.rsplit('_', 1)[0][:26] + '  %dx%d' % (w0, h0), fill=(200, 200, 230))
    p = os.path.join(OUT, 'catalogo_%s.jpg' % gioco)
    sheet.save(p, quality=80)
    print(p, sheet.size)
