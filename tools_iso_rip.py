#!/usr/bin/env python3
"""Estrazione grafica dalle ISO PSP fornite dall'utente (cartella iso/).

Pipeline:
  cso2iso <file.cso> <out.iso>   — decomprime il formato CISO (blocchi zlib)
  scan <file-o-cartella> <outdir> — cerca e decodifica texture GIM ('MIG.00.1PSP')
                                    e TIM2 dentro QUALSIASI file (raw scan: trova
                                    le immagini anche dentro archivi proprietari)
Le GIM PSP: pixel index4/index8/RGBA, palette RGBA8888/5551/4444, swizzle 16×8.
"""
import sys, os, zlib, struct

# ---------------- CSO -> ISO ----------------
def cso2iso(src, dst):
    f = open(src, 'rb')
    magic, hdr_size, total, block, ver, align = struct.unpack('<4sIQIBB2x', f.read(24))
    assert magic == b'CISO', 'non è un CSO'
    nblocks = total // block
    idx = list(struct.unpack('<%dI' % (nblocks + 1), f.read(4 * (nblocks + 1))))
    out = open(dst, 'wb')
    for i in range(nblocks):
        plain = idx[i] & 0x80000000
        off = (idx[i] & 0x7fffffff) << align
        end = (idx[i+1] & 0x7fffffff) << align
        f.seek(off)
        data = f.read(end - off)
        if plain:
            out.write(data[:block])
        else:
            out.write(zlib.decompressobj(-15).decompress(data)[:block])
        if i % 20000 == 0:
            print('  blocco %d/%d' % (i, nblocks), flush=True)
    out.close()
    print('iso scritta:', dst, os.path.getsize(dst), 'byte')

# ---------------- GIM (PSP) ----------------
def unswizzle(data, w_bytes, h):
    # blocchi 16 byte x 8 righe (standard PSP)
    out = bytearray(len(data))
    bw, bh = w_bytes // 16, h // 8
    i = 0
    for by in range(bh):
        for bx in range(bw):
            for y in range(8):
                dst = ((by*8 + y) * w_bytes) + bx*16
                out[dst:dst+16] = data[i:i+16]
                i += 16
    return bytes(out)

def parse_gim(buf, base):
    """decodifica una GIM che inizia a buf[base:]; ritorna PIL Image o None."""
    from PIL import Image
    try:
        # cammina i chunk: cerchiamo image (0x04) e palette (0x05)
        pos = base + 16
        img_blk = pal_blk = None
        guard = 0
        while pos + 16 <= len(buf) and guard < 64:
            guard += 1
            bid, _, sz, hdr = struct.unpack_from('<HHII', buf, pos)
            if sz <= 0 or sz > 1 << 24: break
            if bid == 0x04: img_blk = pos
            elif bid == 0x05: pal_blk = pos
            elif bid == 0x02:   # blocco contenitore: entra
                pos += 16; continue
            if bid in (0x04, 0x05) and img_blk and (pal_blk or bid == 0x04):
                pass
            pos += sz
            if img_blk and (pal_blk or guard > 8): break
        if not img_blk: return None
        def blocco(p):
            dsz, fmt, sw, w, h = struct.unpack_from('<IHHHH', buf, p + 32 - 12 + 0), None, None, None, None
        # header dati immagine: a +16 dal blocco: hdrlen(2) refs.. formato semplificato:
        p = img_blk + 16
        hdrlen, refs, fmt, sw, w, h, bpp = struct.unpack_from('<HHHHHHH', buf, p)
        datap = img_blk + 16 + 32
        if fmt > 5 or w == 0 or h == 0 or w > 2048 or h > 2048: return None
        BPP = {0:16,1:16,2:16,3:32,4:4,5:8}[fmt]
        wb = (w * BPP + 7) // 8
        need = wb * h
        raw = buf[datap:datap + need]
        if len(raw) < need: return None
        if sw == 1:
            hh = h - (h % 8)
            if hh >= 8 and wb % 16 == 0: raw = unswizzle(raw[:wb*hh], wb, hh) + raw[wb*hh:]
        pal = None
        if pal_blk:
            pp = pal_blk + 16
            phl, prefs, pfmt, psw, pw, ph, pbpp = struct.unpack_from('<HHHHHHH', buf, pp)
            pdat = pal_blk + 16 + 32
            n = pw
            pal = []
            for i in range(min(n, 256)):
                if pfmt == 3:
                    r, g, b, a = struct.unpack_from('<BBBB', buf, pdat + i*4)
                elif pfmt in (0, 1, 2):
                    v = struct.unpack_from('<H', buf, pdat + i*2)[0]
                    if pfmt == 0:  # 5650
                        r = (v & 31) << 3; g = ((v >> 5) & 63) << 2; b = ((v >> 11) & 31) << 3; a = 255
                    elif pfmt == 1:  # 5551
                        r = (v & 31) << 3; g = ((v >> 5) & 31) << 3; b = ((v >> 10) & 31) << 3; a = 255 if v >> 15 else 0
                    else:  # 4444
                        r = (v & 15) << 4; g = ((v >> 4) & 15) << 4; b = ((v >> 8) & 15) << 4; a = ((v >> 12) & 15) << 4
                else: return None
                pal.append((r, g, b, a))
        img = Image.new('RGBA', (w, h))
        px = img.load()
        if fmt == 4 and pal:      # index4
            for y in range(h):
                for x in range(w):
                    bt = raw[y*wb + x//2]
                    idx = bt & 15 if x % 2 == 0 else bt >> 4
                    px[x, y] = pal[idx] if idx < len(pal) else (0,0,0,0)
        elif fmt == 5 and pal:    # index8
            for y in range(h):
                for x in range(w):
                    idx = raw[y*wb + x]
                    px[x, y] = pal[idx] if idx < len(pal) else (0,0,0,0)
        elif fmt == 3:            # RGBA8888
            for y in range(h):
                for x in range(w):
                    r, g, b, a = raw[y*wb+x*4:y*wb+x*4+4]
                    px[x, y] = (r, g, b, a)
        elif fmt in (0, 1, 2):    # 16 bit
            for y in range(h):
                for x in range(w):
                    v = struct.unpack_from('<H', raw, y*wb + x*2)[0]
                    if fmt == 0:
                        px[x, y] = ((v & 31) << 3, ((v>>5)&63)<<2, ((v>>11)&31)<<3, 255)
                    elif fmt == 1:
                        px[x, y] = ((v & 31) << 3, ((v>>5)&31)<<3, ((v>>10)&31)<<3, 255 if v>>15 else 0)
                    else:
                        px[x, y] = ((v & 15) << 4, ((v>>4)&15)<<4, ((v>>8)&15)<<4, ((v>>12)&15)<<4)
        else:
            return None
        return img
    except Exception:
        return None

def scan(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    if os.path.isdir(path):
        for r, _, fs in os.walk(path):
            files += [os.path.join(r, f) for f in fs]
    else:
        files = [path]
    tot = 0
    for fp in files:
        try:
            buf = open(fp, 'rb').read()
        except Exception:
            continue
        base = 0
        n_file = 0
        while True:
            i = buf.find(b'MIG.00.1PSP', base)
            if i < 0: break
            img = parse_gim(buf, i)
            if img is not None and img.size[0] >= 16 and img.size[1] >= 16:
                nome = os.path.basename(fp).replace('.', '_')
                img.save(os.path.join(outdir, '%s_%08x.png' % (nome, i)))
                tot += 1; n_file += 1
            base = i + 16
        if n_file:
            print('%s: %d GIM' % (os.path.basename(fp), n_file), flush=True)
    print('TOTALE:', tot, 'texture estratte in', outdir)

if __name__ == '__main__':
    if sys.argv[1] == 'cso2iso': cso2iso(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'scan': scan(sys.argv[2], sys.argv[3])
