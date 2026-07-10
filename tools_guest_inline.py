#!/usr/bin/env python3
"""Inietta le strip di assets/guest/out/ in index.html (HAWK_ASSETS, riga unica).
Idempotente: sostituisce la chiave se già presente. La riga loadImg è a parte
(una sola riga a lista, vedi regola 14). MAI base64 nel contesto: solo qui."""
import os, re, base64, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'guest', 'out')
IDX = os.path.join(ROOT, 'index.html')

KEYS = ['g_naruto','g_sasuke','g_rocklee','g_kakashi','g_harry',
        'g_doxy','g_gnome','g_tentacula','g_snape','g_filch','g_dumbledore',
        'g_fluffy','g_zabuza','g_tigre','g_corvo','g_ninja','g_konoha_bg',
        # v16 — Stranger Things + atlante Hogwarts (S-GRAFICA)
        'st_eleven','st_hopper','st_demodog','st_demobat','st_demogrey',
        'st_demogorgon','st_vecna','st_upside_far','st_upside_near','g_hogtiles']

lines = open(IDX, encoding='utf-8').read().split('\n')
hi = next(i for i, l in enumerate(lines) if l.startswith('window.HAWK_ASSETS'))
row = lines[hi]
assert row.rstrip().endswith('};')
for k in KEYS:
    b64 = base64.b64encode(open(os.path.join(OUT, k + '.png'), 'rb').read()).decode()
    entry = '"%s": "data:image/png;base64,%s"' % (k, b64)
    pat = re.compile('"%s": "data:image/png;base64,[A-Za-z0-9+/=]*"' % k)
    if pat.search(row):
        row = pat.sub(entry, row)
        print('sostituito', k)
    else:
        row = row[:row.rindex('}')] + ', ' + entry + row[row.rindex('}'):]
        print('aggiunto', k, len(b64), 'b64 chars')
lines[hi] = row
open(IDX, 'w', encoding='utf-8').write('\n'.join(lines))
print('HAWK_ASSETS ok, riga lunga', len(row))
