#!/usr/bin/env python3
"""S-OSPITI: compone le strip finali per il gioco da assets/guest/.

Output in assets/guest/out/:
  g_<id>.png   — strip a righe (una riga per anim, celle uniformi per riga)
  g_fluffy.png / g_zabuza.png — GRIGLIA per MBOSSES (rowCalm=0, rowRage=1)
  g_konoha_bg.png — sfondo dipinto per il parallasse
  guests.json  — coordinate anims per il registro GUESTS
  contact.jpg  — foglio-contatti per verifica visiva
Uso: venv/bin/python tools_guest_build.py
"""
import os, json
from PIL import Image
from tools_guest_extract import load, bands, segs, compose, GUEST, OUT

os.makedirs(OUT, exist_ok=True)
META = {}
STRIPS = {}   # per contact sheet

def save(key, strip, anims, extra=None):
    strip.save(os.path.join(OUT, key + '.png'), optimize=True)
    META[key] = dict(anims=anims, w=strip.size[0], h=strip.size[1], **(extra or {}))
    STRIPS[key] = strip

def sprite_bands(im, minh=28):
    return [b for b in bands(im) if b[1]-b[0] >= minh]

# ---- template Naruto RPG (6 bande: idle+crit / attack / jutsu+use / swap / hit / dead)
def nrpg(src, key):
    im = load(src)
    bs = sprite_bands(im)
    S = [segs(im, y0, y1) for (y0, y1) in bs]
    if len(bs) == 6:   # naruto/sasuke/rocklee
        picks = {
            'idle': [S[0][0]],
            'walk': S[3][:2],
            'jump': [S[3][1]],
            'atk':  S[1][:5],
            'cast': S[2][:4],
            'hurt': S[4][:2],
            'dead': [b for b in S[5] if b[2]-b[0] >= 30][:3],
        }
    else:              # kakashi (5 bande, niente swap: walk = respiro critico)
        picks = {
            'idle': [S[0][0]],
            'walk': S[0][1:4],
            'jump': [S[2][3] if len(S[2]) > 3 else S[2][-1]],
            'atk':  S[1][:5],
            'cast': S[2][:4],
            'hurt': S[3][:2],
            'dead': [b for b in S[4] if b[2]-b[0] >= 30][:3],
        }
    strip, anims = compose(im, picks)
    save(key, strip, anims)

# ---- Harry: sezione BATTLE side-view (sprite da x>=190)
def harry():
    im = load('hp_harry.png')
    def row(y0, y1):
        return [b for b in segs(im, y0, y1, min_gap=2) if b[0] >= 188]
    idle = row(654, 704)          # 5
    atk  = row(718, 768)          # 8 pose + scia
    item = row(782, 832)          # 2 (bacchetta alzata = salto)
    spec = row(845, 896)
    dmg  = row(911, 960)
    dth  = row(979, 1024)
    picks = {
        'idle': idle[:4],
        'walk': idle[:4],
        'jump': item[:1],
        'atk':  atk[9:14],        # frame con la scia blu della bacchetta
        'cast': spec[:4],
        'hurt': dmg[:2],
        'dead': dth[-3:],
    }
    strip, anims = compose(im, picks)
    save('g_harry', strip, anims)

# ---- creature HP
def doxy():
    im = load('hp_doxy.png')
    ss = segs(im, 3, 27, min_gap=1)
    strip, anims = compose(im, {'fly': ss[:3]})
    save('g_doxy', strip, anims)

def gnome():
    im = load('hp_gnome.png')
    mv = [b for b in segs(im, 3, 35, min_gap=1) if b[2]-b[0] >= 12][:4]   # move oro
    hit = [b for b in segs(im, 65, 97, min_gap=1) if b[2]-b[0] >= 12][:1]
    strip, anims = compose(im, {'walk': mv, 'hurt': hit})
    save('g_gnome', strip, anims)

def tentacula():
    im = load('hp_tentacula.png')
    idle = [b for b in segs(im, 3, 51, min_gap=1) if b[2]-b[0] >= 38][:3]
    bite = [b for b in segs(im, 54, 143, min_gap=1) if b[2]-b[0] >= 38][5:8]
    strip, anims = compose(im, {'walk': idle, 'atk': bite})
    save('g_tentacula', strip, anims)

# ---- NPC scuola
def npcs():
    im = load('hp_snape.png')
    ss = [b for b in segs(im, 121, 174, min_gap=2) if b[2]-b[0] >= 18][:3]
    strip, anims = compose(im, {'idle': ss})
    save('g_snape', strip, anims)
    im = load('hp_filch.png')
    sw = [b for b in segs(im, 11, 62, min_gap=2) if b[2]-b[0] >= 28][:3]   # scopa!
    strip, anims = compose(im, {'idle': sw})
    save('g_filch', strip, anims)
    im = load('hp_dumbledore.png')
    # i frame walk si toccano: taglio a passo fisso 33px dal run x41
    wk = [(41 + k*33, 121, 41 + k*33 + 32, 177) for k in range(2)]
    strip, anims = compose(im, {'idle': wk})
    save('g_dumbledore', strip, anims)

# ---- griglie MBOSSES (2 righe: calma / furia, celle uniformi)
def grid(key, im, rows, scale=1.0):
    from tools_guest_extract import key_trim
    rows = [[key_trim(im.crop(b)) for b in r] for r in rows]
    cw = max(f.size[0] for r in rows for f in r)
    ch = max(f.size[1] for r in rows for f in r)
    cols = max(len(r) for r in rows)
    g = Image.new('RGBA', (cw*cols, ch*len(rows)), (0,0,0,0))
    for ri, r in enumerate(rows):
        for ci in range(cols):
            fr = r[ci % len(r)]    # se una riga ha meno frame, ripeti
            g.paste(fr, (ci*cw + (cw-fr.size[0])//2, ri*ch + ch-fr.size[1]), fr)
    if scale != 1.0:
        g = g.resize((max(1,round(g.size[0]*scale)), max(1,round(g.size[1]*scale))), Image.NEAREST)
        cw, ch = round(cw*scale), round(ch*scale)
    g.save(os.path.join(OUT, key + '.png'), optimize=True)
    META[key] = dict(grid=[cw, ch, cols, len(rows)], w=g.size[0], h=g.size[1])
    STRIPS[key] = g

def fluffy():
    im = load('hp_fluffy.png')
    walk = [b for b in segs(im, 4, 100, min_gap=2) if b[2]-b[0] >= 100][:4]
    rage = [b for b in segs(im, 208, 372, min_gap=2) if 80 <= b[2]-b[0] <= 100][:4]
    grid('g_fluffy', im, [walk, rage], scale=0.8)

def zabuza():
    im = load('nrpg_nar_zabuza.png')
    bs = sprite_bands(im)
    calm = segs(im, *bs[0])[:3]
    rage = segs(im, *bs[1])[:3]
    grid('g_zabuza', im, [calm, rage])

# ---- nemici Konoha dalla griglia nrpg_nar_enemies (celle da banda/segmento)
def kono_enemies():
    im = load('nrpg_nar_enemies.png')
    bs = bands(im)
    def cells(bi, idx):
        ss = segs(im, *bs[bi])
        return [ss[i] for i in idx if i < len(ss)]
    strip, anims = compose(im, {'walk': cells(3, [6])})           # tigre (i 3 seg sono varianti di colore)
    save('g_tigre', strip, anims)
    strip, anims = compose(im, {'fly': cells(0, [0,1])})          # corvo 2 frame
    save('g_corvo', strip, anims)
    strip, anims = compose(im, {'walk': cells(11, [0,1,2])})      # ninja oscuro (fila uniforme banda 11)
    save('g_ninja', strip, anims)
    # (i candidati ninja delle bande 6-11 sono stati esaminati una tantum:
    #  scelta finale = banda 11 segs 0-2; niente più strip cand_*)

# ---- sfondo Konoha (cella r2c1 del foglio 3x3, senza barra UI in basso)
def konoha_bg():
    im = Image.open(os.path.join(GUEST, 'nrpg_nar_battlebg.png')).convert('RGB')
    cell = im.crop((267, 374, 533, 548))
    cell.save(os.path.join(OUT, 'g_konoha_bg.png'), optimize=True)
    META['g_konoha_bg'] = dict(w=cell.size[0], h=cell.size[1])
    STRIPS['g_konoha_bg'] = cell.convert('RGBA')

def contact():
    W = max(s.size[0] for s in STRIPS.values()) + 160
    H = sum(s.size[1] + 18 for s in STRIPS.values()) + 10
    sheet = Image.new('RGB', (W, H), (44, 44, 66))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    y = 5
    for k, s in STRIPS.items():
        d.text((4, y + 2), k, fill=(255, 255, 160))
        sheet.paste(s, (150, y), s if s.mode == 'RGBA' else None)
        y += s.size[1] + 18
    p = os.path.join(OUT, 'contact.jpg')
    sheet.save(p, quality=82)
    print('contact:', p, sheet.size)

def run():
    nrpg('nrpg_naruto.png', 'g_naruto')
    nrpg('nrpg_nar_sasuke.png', 'g_sasuke')
    nrpg('nrpg_nar_rocklee.png', 'g_rocklee')
    nrpg('nrpg_nar_kakashi.png', 'g_kakashi')
    harry(); doxy(); gnome(); tentacula(); npcs(); fluffy(); zabuza()
    kono_enemies(); konoha_bg()
    with open(os.path.join(OUT, 'guests.json'), 'w') as f:
        json.dump(META, f, indent=1)
    for k, m in META.items():
        print(k, m.get('anims', m.get('grid')), m['w'], 'x', m['h'])
    contact()

if __name__ == '__main__':
    run()
