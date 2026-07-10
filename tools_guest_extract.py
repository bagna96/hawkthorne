#!/usr/bin/env python3
"""S-OSPITI: estrazione sprite ospiti (HP/Naruto) da assets/guest/.

Modalità:
  scan <file>      — chroma-key + dump bande orizzontali e segmenti colonna (per capire il layout)
  preview <file> <maxw> — salva anteprima ridotta in scratchpad per ispezione visiva
  build            — genera le strip finali in assets/guest/out/ + guests.json (coordinate anims)
  inject           — inline base64 in index.html (HAWK_ASSETS + loadImg), idempotente

Le strip sono "a righe": una riga per animazione, frame uniformi bottom-center.
Il JSON prodotto contiene { chiave: { anims: { nome: [y, fw, fh, n] }, w, h } }.
"""
import sys, os, json, base64
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
GUEST = os.path.join(ROOT, 'assets', 'guest')
OUT = os.path.join(GUEST, 'out')
SCRATCH = os.environ.get('SCRATCH', '/tmp')

def chroma(im, tol=12):
    im = im.convert('RGBA')
    px = im.load()
    bg = px[0, 0][:3]
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if abs(r-bg[0]) <= tol and abs(g-bg[1]) <= tol and abs(b-bg[2]) <= tol:
                px[x, y] = (0, 0, 0, 0)
    return im

def bands(im, min_gap=2):
    """righe orizzontali con pixel opachi -> bande [y0,y1)"""
    w, h = im.size
    px = im.load()
    rows = [any(px[x, y][3] > 8 for x in range(w)) for y in range(h)]
    out, y = [], 0
    while y < h:
        if rows[y]:
            y0 = y
            while y < h and (rows[y] or (y+min_gap <= h and any(rows[y:y+min_gap]))):
                y += 1
            out.append((y0, y))
        else:
            y += 1
    return out

def segs(im, y0, y1, min_gap=3):
    """segmenti di colonne opache nella banda -> [(x0,x1,bbox)]"""
    w = im.size[0]
    px = im.load()
    cols = [any(px[x, y][3] > 8 for y in range(y0, y1)) for x in range(w)]
    out, x = [], 0
    while x < w:
        if cols[x]:
            x0 = x
            gap = 0
            while x < w and gap < min_gap:
                gap = gap + 1 if not cols[x] else 0
                x += 1
            x1 = x - gap
            # bbox verticale reale del segmento
            ys = [y for y in range(y0, y1) for xx in range(x0, x1) if px[xx, y][3] > 8]
            bb = (x0, min(ys), x1, max(ys)+1) if ys else (x0, y0, x1, y1)
            out.append(bb)
        else:
            x += 1
    return out

def key_trim(fr, tol=14):
    """secondo passaggio: molti sheet hanno RIQUADRI-cella di un colore
    diverso dallo sfondo esterno — key sul colore dell'angolo del frame,
    poi ritaglio al contenuto reale."""
    fr = fr.convert('RGBA')
    px = fr.load()
    w, h = fr.size
    corners = [px[0,0], px[w-1,0], px[0,h-1], px[w-1,h-1]]
    for c in corners:
        if c[3] > 8:   # angolo opaco = riquadro da rimuovere
            bg = c[:3]
            for y in range(h):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if a > 8 and abs(r-bg[0]) <= tol and abs(g-bg[1]) <= tol and abs(b-bg[2]) <= tol:
                        px[x, y] = (0, 0, 0, 0)
    bb = fr.getbbox()
    return fr.crop(bb) if bb else fr

def compose(im, picks, scale=1.0):
    """picks = {anim: [bbox,...]} -> (strip_img, anims_json)
    strip: una riga per anim, celle uniformi per riga, bottom-center."""
    rows = []
    for name, boxes in picks.items():
        frames = [key_trim(im.crop(b)) for b in boxes]
        fw = max(f.size[0] for f in frames)
        fh = max(f.size[1] for f in frames)
        rows.append((name, frames, fw, fh))
    W = max(len(fs)*fw for n, fs, fw, fh in rows)
    H = sum(fh for n, fs, fw, fh in rows)
    strip = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    anims, y = {}, 0
    for name, frames, fw, fh in rows:
        for i, fr in enumerate(frames):
            strip.paste(fr, (i*fw + (fw-fr.size[0])//2, y + fh-fr.size[1]), fr)
        anims[name] = [y, fw, fh, len(frames)]
        y += fh
    if scale != 1.0:
        W2, H2 = max(1, round(W*scale)), max(1, round(H*scale))
        strip = strip.resize((W2, H2), Image.NEAREST)
        anims = {n: [round(v[0]*scale), round(v[1]*scale), round(v[2]*scale), v[3]] for n, v in anims.items()}
    return strip, anims

def load(name, tol=12):
    return chroma(Image.open(os.path.join(GUEST, name)), tol)

def cmd_scan(fname):
    im = load(fname)
    print(fname, im.size)
    for (y0, y1) in bands(im):
        ss = segs(im, y0, y1)
        widths = [b[2]-b[0] for b in ss]
        print(f"banda y{y0}-{y1} (h{y1-y0}): {len(ss)} seg, larghezze {widths[:20]}")

def cmd_preview(fname, maxw):
    im = load(fname)
    r = min(1.0, maxw / im.size[0])
    im2 = im.resize((int(im.size[0]*r), int(im.size[1]*r)))
    bg = Image.new('RGB', im2.size, (40, 40, 60))
    bg.paste(im2, (0, 0), im2)
    out = os.path.join(SCRATCH, os.path.splitext(fname)[0] + '_prev.jpg')
    bg.save(out, quality=80)
    print(out, 'ratio', round(r, 4))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'scan': cmd_scan(sys.argv[2])
    elif cmd == 'preview': cmd_preview(sys.argv[2], int(sys.argv[3]))
    elif cmd == 'build':
        import tools_guest_build as B  # config separata
        B.run()
