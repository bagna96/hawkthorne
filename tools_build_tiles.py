#!/usr/bin/env python3
"""S-GRAFICA: texture-tile per bioma (REVIEW-FIX v21.8).
Genera strip 160x32 (5 celle: wall|fill|fillVar|dirt|dirtVar) per m1-m6+trn,
ritaglia bg_m6 (cella parco 1,2 di nrpg_nar_battlebg, pipeline identica a m1-m5),
salva in assets/guest/out/ e INIETTA i base64 in index.html (idempotente).
Deterministico: rigenerare = stesso output. MAI base64 nel contesto."""
import os, re, base64
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'guest', 'out')
IDX = os.path.join(ROOT, 'index.html')
CS = 32  # lato cella

def hx(c):
    return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))

# palette per bioma: [muro chiaro, muro scuro, giunti] [roccia fill, fill scuro] [terra, terra scura, sasso]
BIOMES = {
    'm1':  dict(wall=('#7a7a88', '#66667a', '#4e4e5e'), fill=('#5e5e6c', '#50505e'),
                dirt=('#8a5a34', '#6b4527', '#9a8a72')),
    'm2':  dict(wall=('#5e7062', '#4c5c50', '#37453c'), fill=('#46564a', '#3a473e'),
                dirt=('#6e4c2c', '#553a20', '#6a8a5e')),
    'm3':  dict(wall=('#8a7a66', '#746654', '#584c3e'), fill=('#665a4a', '#564c3e'),
                dirt=('#8a5a34', '#6b4527', '#a29280')),
    'm4':  dict(wall=('#645278', '#524262', '#3c3048'), fill=('#4a3c58', '#3e3248'),
                dirt=('#6e5064', '#57404f', '#8a7090')),
    'm5':  dict(wall=('#3c3650', '#2e2a3e', '#201c2c'), fill=('#2a2638', '#221e2e'),
                dirt=('#3a3040', '#2c2432', '#5a5272')),
    'm6':  dict(wall=('#8a8a92', '#76767e', '#5c5c64'), fill=('#6a6a72', '#5a5a62'),
                dirt=('#7a5a3e', '#60462e', '#98988e')),
    'trn': dict(wall=('#463358', '#382848', '#281c34'), fill=('#322442', '#281c36'),
                dirt=('#3c2c4a', '#2e2138', '#c9a227')),
}

def h2(x, y, s=0):          # hash deterministico per pixel
    return ((x * 73 + y * 37 + x * y * 7 + s * 131) >> 0) % 100

def put(px, x, y, col):
    px[x, y] = col

def cell_wall(px, ox, pal, top=True):
    """Corsi di mattoni 8px, giunti sfalsati; se top, prima fila più chiara."""
    c1, c2, cj = hx(pal[0]), hx(pal[1]), hx(pal[2])
    for y in range(CS):
        row = y // 8
        for x in range(CS):
            col = c1 if h2(x + ox, y) % 3 else c2
            if y % 8 == 7: col = cj                                # giunto orizzontale
            joint = (x + (8 if row % 2 else 0)) % 16 == 15         # giunto verticale sfalsato
            if joint and y % 8 != 7: col = cj
            if top and y < 2: col = tuple(min(255, v + 34) for v in c1)
            elif h2(x + ox, y, 3) < 6: col = tuple(max(0, v - 18) for v in col)  # scheggiature
            put(px, ox + x, y, col)

def cell_fill(px, ox, pal, var=False):
    """Muratura interna: blocchi grandi poco contrastati (il fondale non urla)."""
    c1, c2 = hx(pal[0]), hx(pal[1])
    for y in range(CS):
        for x in range(CS):
            col = c1 if h2(x + ox, y, 1) % 4 else c2
            if (x % 16 == 15 and (y // 16 + x // 16) % 2 == 0) or y % 16 == 15:
                col = tuple(max(0, v - 14) for v in col)           # giunti radi
            if var and h2(x + ox, y, 5) < 4:
                col = tuple(max(0, v - 26) for v in col)           # sassi incassati
            put(px, ox + x, y, col)

def cell_dirt(px, ox, pal, var=False):
    """Terra: base + granelli scuri + qualche sasso chiaro (var: radice/sasso grande)."""
    c1, c2, c3 = hx(pal[0]), hx(pal[1]), hx(pal[2])
    for y in range(CS):
        for x in range(CS):
            r = h2(x + ox, y, 2)
            col = c2 if r < 22 else (c3 if r > 97 else c1)
            put(px, ox + x, y, col)
    if var:  # sasso 5x4 + radice obliqua, posizioni fisse
        for dx in range(5):
            for dy in range(4):
                put(px, ox + 8 + dx, 18 + dy, c3 if (dx + dy) % 3 else hx(pal[1]))
        for k in range(8):
            put(px, ox + 20 + k, 6 + k // 2, c2)

def build_tileset(name, pal):
    im = Image.new('RGB', (CS * 5, CS))
    px = im.load()
    cell_wall(px, 0, pal['wall'], top=True)
    cell_fill(px, CS, pal['fill'])
    cell_fill(px, CS * 2, pal['fill'], var=True)
    cell_dirt(px, CS * 3, pal['dirt'])
    cell_dirt(px, CS * 4, pal['dirt'], var=True)
    p = os.path.join(OUT, 'tiles_' + name + '.png')
    im.save(p, optimize=True)
    return p

def build_bg_m6():
    """Cella (col 1, row 2) 'parco': pipeline bg_m1-m5 — inset 2px, via barra nera, quantizza 160."""
    sheet = Image.open(os.path.join(ROOT, 'assets', 'guest', 'nrpg_nar_battlebg.png')).convert('RGB')
    cw, ch = sheet.width // 3, sheet.height // 3          # ~266x186
    x0, y0 = 1 * cw + 2, 2 * ch + 2
    cell = sheet.crop((x0, y0, x0 + cw - 4, y0 + ch - 4))
    cell = cell.crop((0, 0, cell.width, cell.height - 16))  # barra nera a fondo cella
    cell = cell.quantize(160)
    p = os.path.join(OUT, 'bg_m6.png')
    cell.save(p, optimize=True)
    return p

def inject(keys):
    src = open(IDX, encoding='utf-8').read()
    lines = src.split('\n')
    anchor = next(i for i, l in enumerate(lines) if l.startswith('window.HAWK_ASSETS.bg_m5'))
    for k in keys:
        b64 = base64.b64encode(open(os.path.join(OUT, k + '.png'), 'rb').read()).decode()
        newline = 'window.HAWK_ASSETS.%s = "data:image/png;base64,%s";' % (k, b64)
        hit = next((i for i, l in enumerate(lines) if l.startswith('window.HAWK_ASSETS.%s ' % k)), None)
        if hit is not None:
            lines[hit] = newline
            print('sostituito', k)
        else:
            lines.insert(anchor + 1, newline)
            anchor += 1
            print('aggiunto', k, len(b64), 'b64 chars')
    open(IDX, 'w', encoding='utf-8').write('\n'.join(lines))

if __name__ == '__main__':
    keys = []
    for name, pal in BIOMES.items():
        p = build_tileset(name, pal)
        keys.append('tiles_' + name)
        print(name, os.path.getsize(p), 'bytes')
    p = build_bg_m6()
    keys.append('bg_m6')
    print('bg_m6', os.path.getsize(p), 'bytes')
    inject(keys)
    print('peso index.html:', os.path.getsize(IDX))
