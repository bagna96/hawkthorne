#!/usr/bin/env python3
"""Ridisegno mondi 1-5 (v14): costruisce le mappe su griglia e le inietta in index.html."""
import re

IDX = '/Users/bagna/hawkthorne/index.html'

def mkgrid(w, h):
    return [[' '] * w for _ in range(h)]

def put(g, x, y, ch):
    g[y][x] = ch

def hrun(g, x0, x1, y, ch):
    for x in range(x0, x1 + 1): g[y][x] = ch

def ground(g, x0, x1, top=14, bot=17):
    for x in range(x0, x1 + 1):
        for y in range(top, bot): g[y][x] = '#'
        g[bot][x] = 'B'

def pit(g, x0, x1, top=14, spike=True):
    for x in range(x0, x1 + 1):
        for y in range(top, 17): g[y][x] = ' '
        if spike: g[16][x] = '^'
        g[17][x] = 'B'

def solid(g, x0, x1, ytop, ybot=16):
    for x in range(x0, x1 + 1):
        for y in range(ytop, ybot + 1): g[y][x] = 'B'

def plat(g, x, y, w, ch='-'):
    hrun(g, x, x + w - 1, y, ch)

def coins(g, pts):
    for x, y in pts: g[y][x] = 'o'

def door(g, x, y):
    """porta d'uscita alta 3 tile, a filo del bordo: impossibile mancarla"""
    put(g, x, y, 'X'); put(g, x, y - 1, 'X'); put(g, x, y - 2, 'X')

def render(g):
    return [''.join(r).rstrip() or ' ' for r in g]

# ---------------------------------------------------------------- MONDO 1 — LA RADURA (l'aggancio)
def mondo1():
    W, H = 156, 18
    g = mkgrid(W, H)
    ground(g, 0, W - 1)
    # apertura: cadi dal cielo su una scia di monete che punta alla MOLLA
    put(g, 3, 12, 'P')
    coins(g, [(5, 11), (7, 10), (9, 10), (11, 11)])
    put(g, 13, 13, 'J')                    # molla-lancio: il primo WOW
    plat(g, 15, 8, 5); coins(g, [(16, 7), (17, 7), (18, 7)])
    put(g, 19, 7, 'k')                     # cassa subito: bottino in 10 secondi
    put(g, 22, 13, 'p')                    # Pierce, spostato dopo il primo salto
    put(g, 8, 13, 'T'); put(g, 26, 13, 'T')
    # biforcazione: ALTO rischioso e ricco / BASSO coi nemici
    plat(g, 28, 10, 4); coins(g, [(29, 9), (30, 9)])
    put(g, 34, 9, 'm')                     # piattaforma mobile
    plat(g, 41, 9, 4); coins(g, [(42, 8), (43, 8)])
    plat(g, 47, 8, 5, 'q')                 # ponte sbriciolante
    plat(g, 54, 8, 3); put(g, 55, 7, 'g')
    pit(g, 35, 37); pit(g, 52, 54)
    for x in (30, 40, 50, 58): put(g, x, 13, 'e')
    put(g, 33, 8, 'f'); put(g, 57, 9, 'f')
    put(g, 44, 13, 'C'); put(g, 46, 13, 'T')
    # piazza dell'IMBOSCATA (sacco d'oro sospetto)
    put(g, 66, 13, '&'); put(g, 62, 13, 'T'); put(g, 70, 13, 'T')
    coins(g, [(64, 12), (68, 12)])
    # torre del SIGILLO: molla → piattaforma → cima
    put(g, 80, 13, 'J')
    plat(g, 82, 7, 3)
    solid(g, 86, 89, 9)
    solid(g, 84, 85, 12)                   # gradino di cortesia: la torre si scala anche senza molla
    put(g, 87, 8, 'Z')
    put(g, 84, 5, 'f')
    coins(g, [(83, 6), (88, 8)])           # (88,8) sopra la torre
    g[8][88] = 'o'
    put(g, 92, 13, 'T'); put(g, 94, 13, 'e')
    put(g, 100, 13, 'C')
    # stanza SEGRETA a piano terra: sfonda la S con lo scatto
    solid(g, 106, 113, 12, 12)             # tetto della nicchia
    put(g, 106, 13, 'S')
    coins(g, [(108, 13), (110, 13), (112, 13)])
    put(g, 111, 13, 'h')
    # ultimo tratto: mobile + monete alte, nemici sotto
    plat(g, 118, 9, 4); coins(g, [(119, 8), (120, 8)])
    put(g, 126, 8, 'm')
    plat(g, 133, 9, 4); put(g, 134, 8, 'h')
    for x in (120, 128, 136, 142): put(g, x, 13, 'e')
    put(g, 138, 9, 'f'); put(g, 116, 13, 'T'); put(g, 140, 13, 'T')
    pit(g, 123, 125)
    put(g, 146, 13, 'T')
    door(g, 154, 13)
    return render(g)

# ---------------------------------------------------------------- MONDO 2 — LA FORESTA (verticale)
def mondo2():
    W, H = 120, 18
    g = mkgrid(W, H)
    ground(g, 0, W - 1)
    put(g, 3, 13, 'P')
    for x in (7, 15, 25, 33): put(g, x, 13, 'T')
    for x in (11, 21, 30): put(g, x, 13, 'e')
    coins(g, [(13, 11), (14, 11), (23, 11)])
    put(g, 18, 10, 'f')
    put(g, 34, 13, 'L')                    # Leonard: è in ogni foresta
    put(g, 38, 13, 'C')
    # SALITA tra le chiome: due tronchi giganti (con ARCO al piano terra), rami, corrente
    solid(g, 44, 45, 4)                    # tronco 1
    solid(g, 74, 75, 4)                    # tronco 2
    for tx in (44, 45, 74, 75):            # arco: la strada bassa resta percorribile
        for ty in (12, 13): g[ty][tx] = ' '
    plat(g, 40, 12, 3)
    plat(g, 47, 10, 3); coins(g, [(48, 9)])
    plat(g, 53, 9, 3, 'q')
    plat(g, 58, 8, 3); coins(g, [(59, 7)])
    put(g, 64, 7, 'm')
    plat(g, 70, 6, 3)
    for y in range(5, 13): put(g, 77, y, ':')   # corrente tra i tronchi
    plat(g, 74, 4, 6); coins(g, [(75, 3), (77, 3)]); put(g, 79, 3, 'g')
    put(g, 50, 7, 'f'); put(g, 68, 5, 'f'); put(g, 60, 11, 'f')
    # ridiscesa
    plat(g, 82, 6, 4, 'q'); put(g, 84, 5, 'g')
    plat(g, 88, 9, 3)
    plat(g, 93, 12, 3)
    put(g, 90, 13, 'C'); put(g, 92, 13, 'T')
    # arena del RE GHIANDA: piattaforme laterali per schivare i balzi
    plat(g, 99, 10, 3); plat(g, 110, 10, 3)
    put(g, 105, 12, 'Q')
    put(g, 102, 9, 'f'); put(g, 96, 13, 'T'); put(g, 114, 13, 'T')
    put(g, 112, 9, 'h')
    door(g, 118, 13)
    return render(g)

# ---------------------------------------------------------------- MONDO 3 — IL VILLAGGIO (tetti e barili)
def mondo3():
    W, H = 156, 18
    g = mkgrid(W, H)
    ground(g, 0, W - 1)
    put(g, 3, 13, 'P')
    put(g, 6, 13, 'u')
    plat(g, 8, 12, 2)
    # casa A e casa B: i TETTI sono il percorso ricco
    solid(g, 12, 18, 10); coins(g, [(14, 9), (16, 9)])
    plat(g, 20, 9, 4, 'q')                 # ponte di assi tra i tetti
    solid(g, 26, 33, 9); put(g, 30, 8, 'g')
    put(g, 37, 8, 'm')
    put(g, 15, 13, 'e'); put(g, 24, 13, 'e'); put(g, 22, 6, 'f')
    # CAMPANILE del sigillo: corrente ascensionale (con arco al piano terra)
    solid(g, 48, 50, 5)
    for tx in (48, 49, 50):
        for ty in (12, 13): g[ty][tx] = ' '
    for y in range(6, 14): put(g, 46, y, ':')
    plat(g, 47, 4, 1)
    put(g, 49, 4, 'Z')
    put(g, 44, 13, 'u'); put(g, 52, 5, 'f')
    put(g, 42, 13, 'e')
    # catena di BARILI a domino + casse
    put(g, 56, 13, 'C')
    for x in (58, 60, 62): put(g, x, 13, '!')
    put(g, 64, 13, 'k'); put(g, 65, 13, 'k')
    put(g, 68, 13, 'b')                    # Britta e la torcia (canone)
    # piazza dell'imboscata
    put(g, 76, 13, '&'); put(g, 73, 13, 'T'); put(g, 79, 13, 'T')
    put(g, 84, 13, 'a')                    # Annie & Shirley e il fabbro "caduto"
    put(g, 88, 13, 'w')
    put(g, 96, 13, 'H')                    # banco di Hilda
    put(g, 104, 13, 't')                   # forgia di Troy & Abed
    put(g, 100, 13, 'u')
    # leva → cancello-tesoro
    put(g, 110, 13, 'C')
    put(g, 112, 13, '=')
    solid(g, 115, 121, 11, 11)             # tetto della cripta
    put(g, 115, 12, '9'); put(g, 115, 13, '9')
    coins(g, [(117, 13)]); put(g, 118, 13, 'g'); put(g, 119, 13, 'h'); put(g, 120, 13, 'g')
    # tetti finali (con gradino sopra la fossa)
    plat(g, 122, 11, 3)
    solid(g, 126, 132, 9); coins(g, [(128, 8), (130, 8)])
    plat(g, 134, 8, 4, 'q')
    solid(g, 140, 145, 10); put(g, 142, 9, 'h')
    for x in (128, 136, 144): put(g, x, 13, 'e')
    put(g, 138, 6, 'f'); put(g, 131, 6, 'f'); put(g, 124, 13, 'T'); put(g, 148, 13, 'T')
    pit(g, 122, 124)
    door(g, 154, 13)
    return render(g)

# ---------------------------------------------------------------- MONDO 4 — IL LAGO DI GIN (zattere)
def mondo4():
    W, H = 120, 17
    g = mkgrid(W, H)
    # fondale e gin: superficie a riga 12
    for x in range(W):
        g[16][x] = 'B'
        for y in range(12, 16): g[y][x] = '~'
    # molo di partenza
    solid(g, 0, 8, 11)
    put(g, 3, 10, 'P'); put(g, 6, 10, 'D')     # Duncan: "familiarità professionale"
    # traversata: zattere mobili, isole, assi sbriciolanti
    put(g, 12, 11, 'm')
    solid(g, 22, 26, 12); coins(g, [(23, 11), (25, 11)])
    plat(g, 30, 10, 4, 'q')
    solid(g, 40, 44, 12); put(g, 42, 11, 'C')
    put(g, 50, 11, 'm')
    coins(g, [(14, 10), (32, 9), (51, 9)])
    put(g, 18, 8, 'f'); put(g, 36, 7, 'f')
    # arena del BETAFISH: due isolotti e gin aperto
    solid(g, 56, 58, 12); solid(g, 66, 68, 12)
    put(g, 62, 12, 'V')
    put(g, 60, 8, 'f')
    # risalita in corrente + tesoro sommerso
    for y in range(6, 12): put(g, 76, y, ':')
    plat(g, 73, 5, 4); put(g, 74, 4, 'g'); coins(g, [(76, 4)])
    for x in range(80, 85):
        for y in range(12, 16): g[y][x] = '~'
    put(g, 82, 15, 'g')                        # tesoro in fondo al gin: nuota (e reggi l'alcol)
    solid(g, 88, 92, 12)
    plat(g, 96, 10, 4, 'q')
    put(g, 98, 7, 'f')
    coins(g, [(89, 11), (91, 11), (97, 9)])
    # molo d'arrivo
    solid(g, 104, 119, 11)
    put(g, 108, 8, 'h')
    plat(g, 107, 9, 3)
    door(g, 116, 10)
    return render(g)

# ---------------------------------------------------------------- MONDO 5 — LE CAVERNE (buio, lava, leve)
def mondo5():
    W, H = 156, 18
    g = mkgrid(W, H)
    hrun(g, 0, W - 1, 0, 'B')
    for y in range(H): g[y][0] = 'B'; g[y][W - 1] = 'B'
    ground(g, 1, W - 2)
    put(g, 3, 12, 'P')
    put(g, 6, 13, 'i'); put(g, 16, 13, 'i')
    put(g, 10, 13, 'e'); put(g, 20, 13, 'e')
    coins(g, [(13, 12), (14, 12)])
    # LAVA 1: ponte di assi sbriciolanti sopra il fuoco
    for x in range(26, 37):
        for y in range(14, 17): g[y][x] = '~'
    plat(g, 26, 12, 11, 'q')
    put(g, 24, 13, 'i'); put(g, 38, 13, 'i')
    put(g, 31, 9, 'f')
    put(g, 42, 13, 'C')
    # leva e cancello (muro fino al soffitto: NON si scavalca)
    put(g, 46, 13, '=')
    solid(g, 52, 52, 1, 11)
    put(g, 52, 12, '9'); put(g, 52, 13, '9')
    put(g, 49, 13, 'i')
    coins(g, [(54, 13), (55, 13)])
    put(g, 56, 13, 'k')
    # ASCENSORE alla galleria alta (mensole sospese: sotto si continua a camminare)
    put(g, 60, 8, 'n')
    solid(g, 64, 70, 8, 9); put(g, 67, 7, 'g'); put(g, 66, 13, 'i')
    plat(g, 72, 8, 4, 'q')
    solid(g, 78, 84, 8, 9); coins(g, [(80, 7), (82, 7)]); put(g, 79, 7, '!')
    put(g, 75, 5, 'f'); put(g, 86, 6, 'f')
    plat(g, 86, 10, 3)
    put(g, 90, 13, 'e'); put(g, 94, 13, 'C'); put(g, 92, 13, 'i')
    # IMBOSCATA al buio (con una torcia di cortesia)
    put(g, 100, 13, '&'); put(g, 103, 13, 'i')
    # LAVA 2: isolotti
    for x in range(108, 119):
        for y in range(14, 17): g[y][x] = '~'
    solid(g, 111, 112, 12, 13); solid(g, 115, 116, 12, 13)
    put(g, 106, 13, 'i'); put(g, 120, 13, 'i')
    put(g, 113, 9, 'f')
    # Gilbert, poi la REGINA DEI PIPISTRELLI
    put(g, 126, 13, 'R')
    put(g, 124, 13, 'i'); put(g, 132, 13, 'i')
    plat(g, 132, 10, 3); plat(g, 142, 10, 3)
    put(g, 137, 8, 'Y')
    put(g, 135, 13, 'e'); put(g, 145, 13, 'e')
    for y in range(5, 13): put(g, 148, y, ':')
    put(g, 148, 4, 'g'); plat(g, 146, 4, 2)
    put(g, 144, 9, 'h')
    put(g, 140, 4, 'f')
    door(g, 153, 13); put(g, 150, 13, 'i')
    return render(g)

# ---------------------------------------------------------------- iniezione
BUILD = { 'MONDO 1': mondo1, 'MONDO 2': mondo2, 'MONDO 3': mondo3, 'MONDO 4': mondo4, 'MONDO 5': mondo5 }
REQUIRED = {
    'MONDO 1': 'P X Z C p J m q & S'.split(),
    'MONDO 2': 'P X Q C L : q m'.split(),
    'MONDO 3': 'P X Z C b a t H = 9 & ! q m :'.split(),
    'MONDO 4': 'P X V C D ~ m q :'.split(),
    'MONDO 5': 'P X Y C R = 9 & i ~ n q :'.split(),
}

src = open(IDX).read()
for nome, fn in BUILD.items():
    rows = fn()
    txt = ''.join(r for r in rows)
    for ch in REQUIRED[nome]:
        assert ch in txt, f'{nome}: manca la tile {ch!r}'
    i = src.index(f"name:'{nome}")
    j = src.index('rows:[', i)
    k = src.index(']', src.index('rows:[', i) + 6)
    # trova la vera fine dell'array (ultima riga chiusa da "],")
    k = src.index(']},', j)
    block = 'rows:[\n' + '\n'.join('"%s",' % r.replace('"', '') for r in rows) + '\n'
    src = src[:j] + block + src[k:]
    print(nome, 'OK —', len(rows), 'righe ×', max(len(r) for r in rows), 'col')
open(IDX, 'w').write(src)
print('iniettato in index.html')
