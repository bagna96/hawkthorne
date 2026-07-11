#!/usr/bin/env python3
"""Estrattore grafica da ROM GBA (per Ron/Hermione da PoA e Voldemort da PhS).

GBA: grafica quasi sempre LZ77 BIOS (header 0x10) + tile 4bpp + palette BGR555.
  sweep <rom.zip|gba> <outdir> [minKB]  — trova i blob LZ77 validi, li rende in
        GRIGI a larghezza 16 tile (i frame sprite riemergono a vista) e salva
        contact per l'ispezione. Registra offset/size in blobs.txt.
  color <rom> <blob_off> <outdir>       — prova le palette candidate (righe di
        16xu16 plausibili vicino al blob e in tutta la ROM) sul blob scelto.
"""
import os, sys, struct, zipfile

def carica(percorso):
    if percorso.endswith('.zip'):
        z = zipfile.ZipFile(percorso)
        nome = [n for n in z.namelist() if n.lower().endswith('.gba')][0]
        return z.read(nome)
    return open(percorso, 'rb').read()

def lz77(data, massimo=1 << 21):
    if not data or data[0] != 0x10: return None
    size = data[1] | data[2] << 8 | data[3] << 16
    if size < 256 or size > massimo: return None
    out = bytearray(); pos = 4
    try:
        while len(out) < size:
            flags = data[pos]; pos += 1
            for bit in range(8):
                if len(out) >= size: break
                if flags & (0x80 >> bit):
                    b1, b2 = data[pos], data[pos+1]; pos += 2
                    n = (b1 >> 4) + 3
                    back = ((b1 & 0xF) << 8 | b2) + 1
                    if back > len(out): return None
                    for _ in range(n): out.append(out[-back])
                else:
                    out.append(data[pos]); pos += 1
    except IndexError:
        return None
    return bytes(out)

def rendi_grigio(blob, wt=16):
    from PIL import Image
    ntiles = len(blob) // 32
    if ntiles == 0: return None
    ht = (ntiles + wt - 1) // wt
    img = Image.new('L', (wt * 8, ht * 8), 0)
    px = img.load()
    for t in range(ntiles):
        tx, ty = (t % wt) * 8, (t // wt) * 8
        for j in range(64):
            b = blob[t*32 + j//2]
            v = (b & 15) if j % 2 == 0 else (b >> 4)
            px[tx + j % 8, ty + j // 8] = v * 17
    return img

def sweep(percorso, outdir, min_kb=4):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True)
    rom = carica(percorso)
    blobs = []
    i = 0
    while i < len(rom) - 8:
        if rom[i] == 0x10:
            d = lz77(rom[i:i + 1 << 20])
            if d and len(d) >= min_kb * 1024:
                blobs.append((i, len(d), d))
                i += 16
        i += 4
    blobs.sort(key=lambda b: -b[1])
    print('blob LZ77 validi ≥%dKB: %d' % (min_kb, len(blobs)))
    with open(os.path.join(outdir, 'blobs.txt'), 'w') as f:
        for off, sz, _ in blobs: f.write('%#x %d\n' % (off, sz))
    # contact: i primi 48 blob più grossi, in grigio
    quanti = min(48, len(blobs))
    per_riga = 4
    TW, TH = 200, 320
    sheet = Image.new('RGB', (per_riga * (TW + 6) + 6, ((quanti + per_riga - 1)//per_riga) * (TH + 22) + 24), (30, 30, 48))
    d = ImageDraw.Draw(sheet)
    for k in range(quanti):
        off, sz, blob = blobs[k]
        g = rendi_grigio(blob)
        if g is None: continue
        r = min(TW / g.size[0], TH / g.size[1], 1.0)
        g = g.resize((max(1, int(g.size[0]*r)), max(1, int(g.size[1]*r))))
        x = 6 + (k % per_riga) * (TW + 6)
        y = 24 + (k // per_riga) * (TH + 22)
        d.text((x, y - 14), '#%d @%#x %dKB' % (k, off, sz // 1024), fill=(255, 255, 160))
        sheet.paste(g.convert('RGB'), (x, y))
    p = os.path.join(outdir, 'contact_gba.jpg')
    sheet.save(p, quality=80)
    print('contact:', p)

def color(percorso, off, outdir, wt=16):
    """rende il blob a colori con le palette candidate più vicine."""
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True)
    rom = carica(percorso)
    blob = lz77(rom[off:off + 1 << 20])
    # candidate: righe di 32 byte che sembrano palette BGR555 (bit15=0, varietà)
    cands = []
    zona = [(max(0, off - 0x8000), off + 0x8000), (0, len(rom))]
    visti = set()
    for a, b in zona:
        for p in range(a, min(b, len(rom) - 32), 4):
            if p in visti: continue
            ok = True; vals = []
            for k in range(16):
                v = struct.unpack_from('<H', rom, p + k*2)[0]
                if v & 0x8000: ok = False; break
                vals.append(v)
            if ok and len(set(vals)) >= 10 and vals[0] in (0, 0x7FFF):
                cands.append(p); visti.add(p)
                if len(cands) >= (24 if (a, b) == zona[0] else 48): break
        if len(cands) >= 24: break
    print('palette candidate:', len(cands))
    ntiles = len(blob) // 32
    ht = (ntiles + wt - 1) // wt
    for ci, p in enumerate(cands[:24]):
        pal = []
        for k in range(16):
            v = struct.unpack_from('<H', rom, p + k*2)[0]
            pal.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3, 0 if k == 0 else 255))
        img = Image.new('RGBA', (wt * 8, ht * 8), (0, 0, 0, 0))
        px = img.load()
        for t in range(ntiles):
            tx, ty = (t % wt) * 8, (t // wt) * 8
            for j in range(64):
                b = blob[t*32 + j//2]
                v = (b & 15) if j % 2 == 0 else (b >> 4)
                px[tx + j % 8, ty + j // 8] = pal[v]
        img.save(os.path.join(outdir, 'blob%08x_pal%08x.png' % (off, p)))
    print('render a colori in', outdir)

if __name__ == '__main__':
    if sys.argv[1] == 'sweep': sweep(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4)
    elif sys.argv[1] == 'color': color(sys.argv[2], int(sys.argv[3], 0), sys.argv[4])
