#!/usr/bin/env python3
"""Estrattore grafica da ROM Nintendo DS (le ROM dell'utente in iso/, MAI in git).

Formati standard DS:
  filesystem: FNT (0x40) + FAT (0x48) dell'header ROM
  NARC ('NARC') = sub-archivi con lo stesso FAT/FNT — ricorsione
  LZ77 BIOS (primo byte 0x10) — decompressione
  NCGR ('RGCN') = tile 4/8bpp · NCLR ('RLCN') = palette BGR555 · abbinati per nome/vicinanza

Uso:
  python3 tools_nds_rip.py rip <rom.nds|zip> <outdir> [--max N]
Risultato: PNG per ogni NCGR decodificato (con la palette più vicina) + log.
"""
import os, re, sys, struct, zipfile, tempfile

def lz77(data):
    """decompressione LZ77 BIOS GBA/DS (header 0x10 + size 24bit)."""
    if not data or data[0] != 0x10: return None
    size = data[1] | data[2] << 8 | data[3] << 16
    if size == 0 or size > 1 << 23: return None
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
                    for _ in range(n): out.append(out[-back])
                else:
                    out.append(data[pos]); pos += 1
    except IndexError:
        return None
    return bytes(out)

def leggi_fs(rom):
    """filesystem DS -> lista (percorso, bytes)."""
    fnt_off, fnt_sz, fat_off, fat_sz = struct.unpack_from('<IIII', rom, 0x40)
    n = fat_sz // 8
    fat = [struct.unpack_from('<II', rom, fat_off + i*8) for i in range(n)]
    files = []
    def walk(dir_id, base):
        sub_off, first_id = struct.unpack_from('<IH', rom, fnt_off + (dir_id & 0xFFF) * 8)
        pos = fnt_off + sub_off
        fid = first_id
        while True:
            ln = rom[pos]; pos += 1
            if ln == 0: break
            nome = rom[pos:pos + (ln & 0x7F)].decode('ascii', 'replace'); pos += ln & 0x7F
            if ln & 0x80:
                sub = struct.unpack_from('<H', rom, pos)[0]; pos += 2
                walk(sub, base + nome + '/')
            else:
                a, b = fat[fid]
                files.append((base + nome, rom[a:b])); fid += 1
        return
    walk(0xF000, '')
    return files

def spacchetta(nome, data, out, profondita=0):
    """ricorsione: LZ77, NARC; ritorna lista (nome, bytes) di file 'foglia'."""
    if profondita > 3: return [(nome, data)]
    if data[:1] == b'\x10':
        d = lz77(data)
        if d and len(d) > len(data) // 2: return spacchetta(nome + '.lz', d, out, profondita + 1)
    if data[:4] == b'NARC':
        try:
            fat_off = data.find(b'BTAF')
            nfil = struct.unpack_from('<I', data, fat_off + 8)[0] & 0xFFFF
            fimg = data.find(b'GMIF')
            base = fimg + 8
            fogli = []
            for i in range(nfil):
                a, b = struct.unpack_from('<II', data, fat_off + 12 + i*8)
                fogli += spacchetta('%s#%d' % (nome, i), data[base+a:base+b], out, profondita + 1)
            return fogli
        except Exception:
            return [(nome, data)]
    return [(nome, data)]

def leggi_nclr(data):
    """palette: lista di liste (una per blocco da 16) RGBA."""
    i = data.find(b'TTLP')
    if i < 0: return None
    sz, fmt, _, dlen, doff = struct.unpack_from('<IIIII', data, i + 4)
    pal_data = data[i + 4 + doff : i + 4 + doff + dlen]
    cols = []
    for k in range(0, len(pal_data) - 1, 2):
        v = struct.unpack_from('<H', pal_data, k)[0]
        cols.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3, 255))
    return cols

def render_ncgr(data, pal, nome):
    from PIL import Image
    i = data.find(b'RAHC')
    if i < 0: return None
    sz, h_t, w_t, bit, _, _, tlen, toff = struct.unpack_from('<IHHIIIII', data, i + 4)
    bpp = 8 if bit == 4 else 4      # bit: 3=4bpp, 4=8bpp
    raw = data[i + 4 + toff - 8 + 8:]
    raw = data[i + 12 + (toff - 8):(i + 12 + (toff - 8) + tlen)] if tlen else raw
    ntiles = len(raw) // (64 if bpp == 8 else 32)
    if ntiles == 0: return None
    if w_t == 0xFFFF or w_t == 0:
        w_t = 32 if ntiles >= 32 else max(1, ntiles)
    h_t2 = (ntiles + w_t - 1) // w_t
    img = Image.new('RGBA', (w_t * 8, h_t2 * 8), (0, 0, 0, 0))
    px = img.load()
    p0 = pal[0] if pal else [(i2*17, i2*17, i2*17, 255) for i2 in range(16)]
    for t in range(ntiles):
        tx, ty = (t % w_t) * 8, (t // w_t) * 8
        if bpp == 4:
            for j in range(64):
                b = raw[t*32 + j//2]
                v = b & 15 if j % 2 == 0 else b >> 4
                if v: px[tx + j % 8, ty + j // 8] = p0[v] if v < len(p0) else (255, 0, 255, 255)
        else:
            for j in range(64):
                v = raw[t*64 + j]
                if v: px[tx + j % 8, ty + j // 8] = p0[v % len(p0)] if p0 else (v, v, v, 255)
    return img

def rip(percorso, outdir, maxfile=4000):
    os.makedirs(outdir, exist_ok=True)
    if percorso.endswith('.zip'):
        z = zipfile.ZipFile(percorso)
        interno = [n for n in z.namelist() if n.endswith('.nds')][0]
        rom = z.read(interno)
    else:
        rom = open(percorso, 'rb').read()
    files = leggi_fs(rom)
    print('file nel filesystem:', len(files))
    fogli = []
    for nome, data in files[:maxfile]:
        if len(data) < 16: continue
        fogli += spacchetta(nome, data, outdir)
    print('file dopo NARC/LZ77:', len(fogli))
    palette = {}
    ncgr = []
    for nome, data in fogli:
        if b'RLCN' in data[:4]: palette[nome] = leggi_nclr(data)
        elif b'RGCN' in data[:4]: ncgr.append((nome, data))
    print('NCGR:', len(ncgr), '· NCLR:', len(palette))
    pnome = sorted(palette)
    salvati = 0
    for nome, data in ncgr:
        # palette più vicina per prefisso di nome
        best, bl = None, -1
        stem = re.sub(r'\.(ncgr|ncbr|lz|cgr).*$', '', nome.lower())
        for pn in pnome:
            ps = re.sub(r'\.(nclr|lz|clr).*$', '', pn.lower())
            l = os.path.commonprefix([stem, ps])
            if len(l) > bl: bl, best = len(l), pn
        img = render_ncgr(data, [palette[best]] if best else None, nome)
        if img and img.size[1] >= 16:
            fn = re.sub(r'[^A-Za-z0-9_.#-]', '_', nome) + '.png'
            img.save(os.path.join(outdir, fn))
            salvati += 1
    print('PNG salvati:', salvati, 'in', outdir)

if __name__ == '__main__':
    rip(sys.argv[2], sys.argv[3]) if sys.argv[1] == 'rip' else print('uso: rip <rom> <outdir>')
