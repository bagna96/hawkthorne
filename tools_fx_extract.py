#!/usr/bin/env python3
"""§S-VFX — estrattore di strisce jutsu dagli sheet DS (The Spriters Resource).

Gli sheet fx_* di 'Naruto Shippuden: Naruto vs Sasuke' sono montaggi a griglia
IRREGOLARE con DUE fondi da rimuovere: quello esterno (verde/teal) e i
RIQUADRI-CELLA (ciano) dietro ogni frame. Il key robusto qui sotto li toglie
entrambi senza intaccare gli orb blu-bianchi o le fiamme:

    bg  = alpha<20  OR  (r < g-25  AND  b < g+50)

cioè "verde/teal/ciano" (g dominante, r basso), mentre orb (r≈g<b) e fiamme
(r>g) restano. Uso: specificare per-effetto (path, banda y, run di colonne,
px per cella) — le bande/colonne si trovano con detect_bands()/detect_cols().

Output: strip single-row PNG (frame affiancati, celle uniformi) pronta per
HAWK_ASSETS + VFX registry (fw=fh=px, cols=len(runs)). venv in scratchpad
(PIL di sistema rotto su arm64).
"""
import sys
from PIL import Image

def isbg(p):
    r, g, b, a = p
    return a < 20 or (r < g - 25 and b < g + 50)

def key(im):
    im = im.convert('RGBA'); px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if isbg(px[x, y]): px[x, y] = (0, 0, 0, 0)
    return im

def detect_bands(path, ymax=400, step=9):
    """Bande verticali di contenuto (y0,y1): righe non tutte-fondo."""
    im = Image.open(path).convert('RGBA'); W, H = im.size; px = im.load()
    rows = [all(isbg(px[x, y]) for x in range(0, W - 1, step)) for y in range(min(ymax, H))]
    out, s = [], None
    for y in range(len(rows)):
        if not rows[y] and s is None: s = y
        if rows[y] and s is not None:
            if y - s > 8: out.append((s, y))
            s = None
    if s is not None: out.append((s, len(rows)))
    return W, H, out

def detect_cols(path, y0, y1, minrun=12, thresh=3):
    """Run di colonne con contenuto nella banda [y0,y1)."""
    im = Image.open(path).convert('RGBA'); W, H = im.size; px = im.load()
    prof = [sum(0 if isbg(px[x, y]) else 1 for y in range(y0, y1)) for x in range(W)]
    runs, s = [], None
    for x in range(W):
        if prof[x] > thresh and s is None: s = x
        if prof[x] <= thresh and s is not None:
            if x - s > minrun: runs.append((s, x))
            s = None
    if s is not None and W - s > minrun: runs.append((s, W))
    return runs

def build(path, y0, y1, runs, px_cell, out):
    """Ritaglia i frame ai run indicati, key + trim, ricentra in celle uniformi, scala."""
    im = Image.open(path).convert('RGBA')
    frames = []
    for a, b in runs:
        fr = key(im.crop((a, y0, b, y1))); bb = fr.getbbox()
        if bb: fr = fr.crop(bb)
        frames.append(fr)
    cell = max(max(f.width, f.height) for f in frames)
    strip = Image.new('RGBA', (cell * len(frames), cell), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (i * cell + (cell - f.width) // 2, (cell - f.height) // 2), f)
    strip = strip.resize((px_cell * len(frames), px_cell), Image.LANCZOS)
    strip.save(out, optimize=True)
    print(out, strip.size, len(frames), 'frame')

# Ricetta v20.0 (già inline in index.html come fx_rasengan / fx_katon):
RECIPES = {
    'fx_rasengan': dict(path='assets/guest/src_tsr/narutoshippudennarutovssasuke/fx_double_rasengan_98910.png',
                        y0=64, y1=142, runs=[(0,159),(161,320),(322,481)], px=56),
    'fx_katon':    dict(path='assets/guest/src_tsr/narutoshippudennarutovssasuke/fx_fireball_rasengan_98912.png',
                        y0=60, y1=204, runs=[(51,188),(235,366),(423,560)], px=64),
}

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'bands':
        print(detect_bands(sys.argv[2]))
    else:
        for name, r in RECIPES.items():
            build(r['path'], r['y0'], r['y1'], r['runs'], r['px'], 'assets/fx/%s.png' % name)
