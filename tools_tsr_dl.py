#!/usr/bin/env python3
"""Scarica la LIBRERIA di sheet Naruto/HP da The Spriters Resource.

Manifest per gioco (slug → lista (asset_id, nome)). L'immagine vera sta in
/media/assets/<bucket>/<id>.png dentro la pagina dell'asset (mai /download/).
Idempotente: salta i file già scaricati. Output: assets/guest/src_tsr/<gioco>/.
Uso: python3 tools_tsr_dl.py [gruppo]   (gruppi: naruto1 naruto2 hp all)
"""
import os, re, sys, time, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'guest', 'src_tsr')

def fetch(url, binario=False):
    r = subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0', '--max-time', '60', url], capture_output=True)
    return r.stdout if binario else r.stdout.decode('utf-8', 'replace')

MANIFEST = {
 'naruto1': {
  'ds_dsi/narutoshippudennarutovssasuke': [
    (98910,'fx_double_rasengan'),(98911,'fx_otto_porte'),(98912,'fx_fireball_rasengan'),
    (98913,'fx_giant_tree'),(98914,'fx_sakura_guard'),(98915,'fx_rasenbomb'),
    (98916,'fx_shadow_bind'),(98917,'fx_beast_hammer'),(98918,'fx_beast_multistrike'),
    (98919,'fx_wooden_bolt'),
    (98901,'naruto'),(98920,'naruto_3code'),(98921,'naruto_4code'),(98908,'sasuke'),
    (98897,'kakashi'),(98902,'rocklee'),(98903,'sai'),(98904,'sakura'),(98906,'shikamaru'),
    (98893,'deidara'),(98894,'itachi'),(98895,'jiraiya'),(98896,'kabuto'),(98898,'kisame'),
    (98899,'neji'),(98900,'orochimaru'),(98905,'sasori'),(98907,'yamato'),
    (98882,'en_bear'),(98883,'en_claw_ninja'),(98884,'en_crab_ninja'),(98885,'en_flail_ninja'),
    (98886,'en_ink'),(98887,'en_pole_ninja'),(98888,'en_puppet'),(98889,'en_scythe_ninja'),
    (98890,'en_sound_ninja'),(98891,'items'),(98909,'npcs'),
  ],
  'ds_dsi/narutoshinrumble': [
    (53907,'naruto'),(54581,'sasuke'),(54589,'kakashi'),(53906,'sakura'),(54570,'sai'),
    (54569,'pain'),(73406,'deidara'),(54571,'jugo'),(54582,'karin'),(54583,'suigetsu'),
    (69478,'mugshots'),
  ],
  'ds_dsi/narutoshippuudendairansenkagebunshinemaki': [
    (99007,'fx_effects'),(99005,'naruto'),(99015,'sasuke'),(99009,'itachi'),(99006,'deidara'),
    (99010,'kisame'),(99012,'orochimaru'),(99014,'sasori'),(99008,'en_generici'),(99013,'rashoumon'),
  ],
 },
 'naruto2': {
  'ds_dsi/narutoshippudenninjacouncil4': [
    (89533,'naruto'),(89534,'sakura'),(89537,'gaara'),(89538,'kakashi'),(98863,'jiraiya'),
    (98866,'guy'),(98867,'neji'),(98868,'rocklee'),(98870,'shikamaru'),(98871,'temari'),
    (98872,'tenten'),(98873,'tsunade'),(89536,'deidara'),(89535,'itachi'),(98865,'kisame'),
    (98869,'sasori'),(98859,'chiyo'),(98864,'kankuro'),
    (98860,'en_puppet'),(98861,'en_sand'),(98862,'en_sound'),
  ],
  'ds_dsi/narutopotn2': [
    (15352,'summ_gamakitchi'),(20543,'summ_gamabunta'),(16549,'summ_manda'),
    (15361,'summ_katsuyu'),(16551,'summ_cani_ninja'),(28065,'summ_shukaku'),
    (15349,'naruto'),(79187,'naruto_9code'),(16552,'sasuke'),(15357,'kakashi'),(15381,'gaara'),
    (15356,'itachi'),(15360,'kisame'),(16550,'orochimaru'),(15369,'zabuza'),(15362,'haku'),
    (16547,'jiraiya'),(20542,'tsunade'),(15364,'rocklee'),(15363,'neji'),(15353,'guy'),
    (15370,'sound4_kimimaro'),(79186,'enemies'),
  ],
 },
 'hp': {
  'game_boy_gbc/harrypotterthechamberofsecrets': [
    (27356,'harry'),(16455,'weasleys'),(16438,'fantasmi'),(16427,'npc_diagon'),
    (16417,'basilisco'),(29001,'folletto_cornovaglia'),(16446,'mandragola'),(28996,'doxy'),
    (27363,'gnomo'),(16454,'tentacula'),(16445,'ragno_grande'),(28998,'granchio_fuoco'),
    (28957,'gytrash'),(27771,'ghoul'),(28999,'lumaca_carnivora'),(29000,'goblin'),
    (28960,'serpente'),(28958,'mano'),(28995,'armatura'),(16452,'salamandra'),(16453,'teschio'),
  ],
  'game_boy_gbc/harrypotterthephilosophersstone': [
    (32056,'harry'),(32697,'battle_bg'),(21139,'mugshots'),
  ],
  'game_boy_advance/harrypotterthechamberofsecrets': [
    (30926,'items'),(81456,'npc_diagon'),(81459,'hagrid'),(81971,'objects'),
  ],
 },
}

def dl(slug, aid, nome):
    gioco = slug.split('/')[1]
    ddir = os.path.join(OUT, gioco)
    os.makedirs(ddir, exist_ok=True)
    dest = os.path.join(ddir, '%s_%d.png' % (nome, aid))
    if os.path.exists(dest) and os.path.getsize(dest) > 4000:
        return 'skip'
    try:
        pg = fetch('https://www.spriters-resource.com/%s/asset/%d/' % (slug, aid))
        m = re.search(r'/media/assets/[^"]+\.png', pg)
        if not m: return 'NO-URL'
        time.sleep(0.8)
        img = fetch('https://www.spriters-resource.com' + m.group(0), binario=True)
        if len(img) < 4000: return 'PICCOLO'
        open(dest, 'wb').write(img)
        return 'ok %dKB' % (len(img)//1024)
    except Exception as e:
        return 'ERR ' + str(e)[:40]

if __name__ == '__main__':
    gruppi = sys.argv[1:] or ['all']
    if 'all' in gruppi: gruppi = list(MANIFEST)
    for g in gruppi:
        for slug, items in MANIFEST[g].items():
            for aid, nome in items:
                print(slug.split('/')[1], nome, dl(slug, aid, nome), flush=True)
                time.sleep(0.8)
