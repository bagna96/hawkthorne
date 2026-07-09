# PROMPT V10 — Hawkthorne "Leggendario" (campagna multi-sessione)

> Autosufficiente: contesto, regole, architettura, storia, asset, fasi.
> Leggi PRIMA le memorie `hawkthorne-assets`, `fan-content-fidelity` e
> `game-feel-expectations` (gusti dell'utente: juice + roguelite, PS5).

## CONTESTO (stato v10.6 — Sessioni 1-4 completate)
Progetto `~/hawkthorne`: platformer 8-bit tributo a Community S3E20
"Digital Estate Planning". Live: https://bagna96.github.io/hawkthorne/
(repo `bagna96/hawkthorne`, branch main, GitHub Pages).
- `index.html` = gioco COMPLETO single-file (~1.2MB, asset base64 inline nel
  blocco HAWK_ASSETS; `assets.js` copia esterna; script python di
  rigenerazione nei commit v7/v8).
- 20 personaggi giocabili (sprite autentici Project Hawkthorne), costumi,
  super a barra Meraviglia, tratti passivi, boons negozio, scivolata/schianto,
  7 mondi (hub, radura, foresta+Re Ghianda, villaggio, lago di gin,
  caverne+Gilbert, trono+Cornelius), co-op locale 2P, co-op online WebRTC,
  gamepad PS5+rumble, musica procedurale WebAudio, save localStorage `hawk_save`.
- V10.1-2: registri `ENEMIES`/`VFX`/`ACHIEVEMENTS`/`QUESTS`+quest-engine/
  `MBOSSES` (hopper/swooper/leaper)/`ACTS` (intro/end, pendingCut). Atto I e
  II completi, nuoto+ubriachezza nel gin, NPC a terra (groundAt), tutorial
  adattivo tastiera/PS5, Gilbert alleato/giocabile a fine Atto II.
- V10.4 (S3): `BIOMES` + `CHUNKS[]` (17 spezzoni 12 righe, tag {b, d, i/o
  quota}); `genLevel(seed,prof)` mulberry32 (salita ≤2, cap start/end,
  mini-boss ogni 3, iniezione seeded); `remixDef` = Linea Oscura (overlay
  `difference` post-drawTiles, élite, dark off; ogni 5 profondità);
  PARTITA INFINITA (SAVE.endlessBest) e SFIDA DEL GIORNO (`#seed=N` URL);
  endless solo locale; `loadLevel` accetta def-oggetto (lvlIdx=-1).
- V10.5 (feedback "gioco piatto"): `PERKS` (14) + scelta 1-di-3 a carte
  dopo ogni profondità (openPerks/updatePerk/drawPerk); statua orbitante,
  vampirismo, resurrezione, furia... JUICE: `hitstop`, squash&stretch,
  coyote+jump buffer, polvere, popup/anelli nei `parts` (txt/ring/ng/sway/
  sz), `ambientFX()` meteo per bioma, parallasse 3 piani tinta (`shade()`),
  stalattiti+lucciole nel dark. Menù OPZIONI (SAVE.opts) e TRUCCHI
  (god/infSoul/monete/sblocchi — `cheatDirty` spegne award e record).
- V10.6 (S4, ROGUELITE LEGGENDARIO): `WEAPONS` (6 armi, ognuna cambia lo
  stile: penna crit-alle-spalle, mazza smash+lancio, dodgeball rimbalzante,
  paintball, keytar onda perforante, lancia-lava; 2 slot swap TAB/L1, drop
  da casse/boss/negozio/porta in `wdrops[]`, `wsfx`+rumble per arma);
  `SYNERGIES` (8 coppie nominate, `checkSynergies`, offerte pesate ×3);
  carta POM (livelli `bl(id)`, rendimenti calanti) alternata al BANCO DI
  HILDA ogni 2 profondità; cassa maledetta 'x' (perk gratis, `curse`=20:
  1 colpo=morte); porta 'W' con anteprima accanto alla 'X'; BOSS ogni 5
  (arena, `mboss.boss2`: telegraph 32f '!', 2 fasi, interfase invulnerabile
  con ondata, remix dal 10°, cuore pietà, arma garantita; Linea Oscura →
  %7); musica a LAYER (`musicLayers`) + `stinger(...)`; pausa da Options,
  Incubo/costumi da pad.
- V10.7 (S5 tappa 1, MONDO VIVO): MINIMAPPA (`drawMinimap`, segue il pg,
  toggle Opzioni); META-PROGRESSIONE PERMANENTE `SAVE.meta`/`SAVE.shards`
  (Frammenti ⬡ dai boss: mboss +2/3, boss +5) + registro `ABILITIES` + stato
  `abilities` ("Albero di Hawkthorne" dal titolo, `hasAbil(id)`); movimento
  sbloccabile: `djump`, `dash` (roll=Shift, pad R1/b5; atk pad solo ▢/b2),
  `walljump`.
- V10.8 (S5 tappa 2 + rework): mosse base GRATIS/subito (`BASE_ABIL`,
  `hasAbil` = BASE||meta); l'Albero → NEGOZIO in Monete (`SAVE.wallet`) con 7
  poteri avanzati (`ABILITIES`: triplejump/airdash/dashblade/glide/groundslam/
  reflect/coinmagnet, effetti in updateOnePlayer). `grantShards`→ora dà Monete.
  INTERACT: 'J' molla (bounce), 'S' blocco segreto solido sfondabile con dash
  (`breakSecret`); iniettati in genLevel. Motore `GUIDE`+`showGuide` (voce
  Abed, SAVE.flags.seen, no marker perenni): guide moves/bounce/secret.
  +4 armi (spadalaser/ascia/shuriken/bazooka). VFX esterno CC0 `fx_firework`
  (repo hawkthorne, 6×373×340) via `playFX`/`fxShots`/`drawFXShots`.
- Debug: `.goto .step .tp .soul .super .kill .dmg .beatRival .p2 .give .gems
  .boon .forge .incubo .next .fakeGuest .reset .info .quest .mbkill .gen
  .remix .arma .pom .maledici .syn .god .perk .shards(n=+monete) .unlock(id?)`.

## §RICERCA (S4.6) — "MONDO VIVO", da web+GitHub (in gran parte consumata)
Movente: l'utente trova il gioco "asettico". Restano da applicare (tappa 3):
- **AMBIENTE REATTIVO** (300mind, gamedesignskills): far vivere lo spazio
  (bestioline, luci, chiacchiere NPC) e ampliare gli interattivi: leve→
  cancelli gated dalle abilità, torce, casse esplosive, blocchi spingibili,
  correnti, appigli. Fatti: molla, blocco segreto, mini-guide (v10.8).
- **MONDO VIVO SISTEMICO** (Terraria happiness): regole intrecciate che
  toccano l'economia (userà i punti-casa HP). Storytelling ambientale.
- **POTERI = INCANTESIMI ELEMENTALI** (Wizard of Legend + Hogwarts Legacy):
  cast rapidi chainabili mentre scatti, colori-firma, 4 slot HUD, chiavi
  colorate (Wingardium=giallo). Registro `SPELLS`. Base della magia HP (S6).
  Spell-craft profondo (Noita) = evoluzione futura.
- **MINI-GUIDE / MOVIMENTO** ✅ fatti (v10.7-8). Da fare: pogo, mantle, combo aeree.
Fonti: gamedeveloper.com (invisible tutorials; env. storytelling),
300mind.studio + gamedesignskills.com (ambienti interattivi),
terraria.wiki.gg (NPC happiness), choostgames.com (spell-craft), gamerant.com (Hogwarts
Legacy combat), github.com/topics/2d-platformer.

## VINCOLI NON NEGOZIABILI
1. **Single-file, zero dipendenze runtime** (no CDN/font/fetch). Deve girare
   da doppio-click file:// e su Pages. Browser di riferimento utente: Safari;
   testa lì. Chrome ok per sviluppo.
2. **Sprite Community intoccabili** (personaggi principali = autentici
   hawkthorne-journey). Tutto il resto — mondi, nemici, NPC, VFX — libertà
   totale, anche fuori dagli schemi. CC0/free-no-attribution ammessi.
3. Testo di gioco in **italiano**, ironia/humor nero/british (Duncan).
   Battute fedeli alla serie dove esistono.
4. Stile: **48px**, palette scura coerente. Musica: **solo procedurale** WebAudio.
5. Commit frequenti + push immediato. Memoria aggiornata a fine sessione.
6. **PS5-first**: l'utente gioca soprattutto col controller. Ogni menù o
   schermata nuova DEVE essere navigabile da pad (glifi ✕▢◯△ nei testi);
   rumble come feedback. Difficoltà: accessibile ma crescente (stile
   Hades) — la profondità punisce, l'inizio accoglie.

## §TOKEN — anti-spreco per Claude Code (obbligatorio)
- MAI rileggere `index.html` intero (~4000 righe): `grep -n` + read mirati.
- Edit chirurgici (`edit_block`/str_replace), mai riscritture di blocchi sani.
- Batch: pianifica 3-5 modifiche correlate, applicale in sequenza, UN solo
  ciclo di test alla fine (non test dopo ogni riga).
- Nuovi contenuti = **righe nei registri dati** (§ARCHITETTURA), non funzioni
  ad-hoc. Se stai scrivendo >30 righe di codice per UN nemico, fermati:
  stai violando l'architettura.
- Screenshot solo per decidere; analisi video max 2 tentativi poi fix di classe.
- Non rigenerare `assets.js` per aggiunte singole: appendi la chiave base64
  al blocco HAWK_ASSETS con uno script mirato.

## §ARCHITETTURA — data-driven (rifattorizza in Sessione 1)
Tutto il contenuto vive in registri JS compatti dentro index.html. Ogni
elemento nuovo = una riga. Il motore legge i registri, mai hardcode sparso.
- `WORLDS[]`: {id, nome, tileset, palette, parallax[], meteo, musicaSeed,
  spawn[], portali[], hazards[], boss}
- `ENEMIES[]`: {id, sheet, layout(fw,fh,cols), anim{}, hp, ai, drop, taglia}
  → ai = riferimento a comportamenti riusabili: patrol, chase, fly, swarm,
  jump, ranged, boss-pattern(fasi[]).
- `QUESTS[]`: {id, atto, giver, mondo, obiettivo{tipo,target,n}, ricompensa,
  dialoghi{start,mid,end}, next} → tipi obiettivo: kill, collect, reach,
  talk, escort, survive. Il quest-engine è UNO, generico.
- `VFX[]`: {id, sheet, fw, fh, frames, loop, blend} → un solo player VFX.
- `SUPERS[]` e `COMBO_SUPERS[]` (matrice coppie): {id, vfx, danno, durata,
  livelli[3]}.
- `DIALOGHI`: stringhe brevi (max 2 righe a battuta), tono Duncan/nero,
  memorizzate nelle quest o in `LORE[]` per NPC ambientali.
- `ACHIEVEMENTS[]`: {id, nome, cond, toast}.
Beneficio: 10 nemici nuovi ≈ 10 righe + sheet. Il cuore della V10.

## §ASSET — fonti e pipeline
### Fonte 1 (autentica, scriptabile): repo hawkthorne-journey
`https://raw.githubusercontent.com/hawkthorne/hawkthorne-journey/master/src/images/{characters,npc,enemies,...}`
Regole rodate: `sleep 1` tra file (rate-limit), verifica png >5KB.
Layout noti: personaggi 12×16 frame 48×48 (mappa ANIM, riga destra,
sinistra=riga−1); hilda 32×48; babyabed 20×25; **acorn 220×40 = 10 col di
22×20** (0-1 morte, 2-5 camminata, 6-9 IN FIAMME — usate per gli élite;
il vecchio taglio 44×40 spezzava lo sprite in 3); hippy 48×48 (6×2);
bat 30×22 (5col); cornelius boss 200×220 (3×5); acornBoss 75×75 (8×7);
cornelius_lightning 144×192 (3col).

### Fonte 2 (CC0, scriptabile via curl)
- **LPC Universal Spritesheet** (github LiberatedPixelCup/Universal-LPC-
  Spritesheet-Character-Generator, raw `/master/spritesheets/...` — licenze
  miste: usa SOLO le righe CC0 di CREDITS.csv). NPC generici e varianti.
- **OpenGameArt CC0** (`opengameart.org/content/cc0-resources`, `/content/
  cc0-tiles-tilesets`): tileset caverna/villaggio/NES-like, file diretti.
- **Kenney** (kenney.nl, tutto CC0, zip via curl -L): particelle, UI, tile.

### Fonte 3 (free, NON scriptabile): itch.io — l'utente scarica lo zip, o salta
Pack free consigliati per i super elementali: **Foozle "Pixel Magic Effects"**
(foozlecc.itch.io, no-attribution), **pimen**, BDragon1727, ansimuz, CodeManu.

### Regole integrazione asset esterni
- Verifica visiva OBBLIGATORIA (rendering di prova) prima dell'inline.
- Riscalatura/adattamento a 48px e palette scura: ok ricolorare via canvas
  offline o script python (PIL) in fase di build asset.
- Registra ogni asset esterno in `CREDITS.md` (fonte, licenza, uso) anche
  se CC0 — igiene del progetto.
- Se un asset non convince visivamente: scarta. Meglio procedurale coerente
  che sprite bello ma alieno allo stile.

## §STORIA — campagna in 4 atti (spina S3E20 + espansione)
Narratore-meta: **Abed** rompe la quarta parete a inizio/fine atto (2 righe,
stile "questo è chiaramente il livello tutorial"). La storia PORTA il
giocatore, ma resta leggera: niente muri di testo, gameplay prima di tutto.
- **ATTI I-II**: ✅ fatti (Sigilli del Testamento; campioni di Gilbert →
  Gilbert alleato per dignità, non avidità).
- **ATTO III — Il Trono** (trono + GREENDALE): Cornelius "vero" (l'insulto
  finale programmato) + nuovo: il suo codice infetta Greendale. Quest a
  Greendale: il Dean (3 costumi) dà 3 incarichi, Chang boss "EL TIGRE" con
  fulmini, Leonard ruba monete (mini-caccia). Livello segreto PAINTBALL
  (ingresso nascosto, tutto ricolorato a schizzi, arma-vernice temporanea).
- **ATTO IV — La Linea Temporale Oscura** (post-game, originale): battuto
  Cornelius, il gioco "si corrompe": glitch visivi voluti, mondi remix in
  palette invertita, versioni malvagie dei personaggi (pizzetto di feltro
  disegnato via canvas sugli sprite — NON tocca i png originali), Abed-Oscuro
  boss finale nel **Dreamatorium** (mondo astratto a griglie olografiche,
  generato proceduralmente: qui "fuori dagli schemi" è mandato).
Side-quest opzionali (registro QUESTS, atto=0): Annie's Boobs (riporta 5
oggetti rubati), statua Luis Guzmán (easter egg, sheet `guzman` nel repo),
"Zitto Leonard" (50 hippy), consegne del Dean.

## §MONDI NUOVI (righe WORLDS, in ordine di build)
1. **GREENDALE** — corridoi campus: armadietti, bacheca, mensa. Tileset da
   repo se esiste `greendale*`, altrimenti procedurale + OGA CC0. NPC: Dean,
   Chang (boss), Leonard, Garrett ("GARRETT NEL PANICO" evento casuale).
2. **PAINTBALL** (segreto in Greendale) — ricolorazione runtime del tileset
   via canvas, nemici = studenti coi costumi `paintball` già scaricati.
3. **DREAMATORIUM** — astratto, griglie/ologrammi procedurali, gravità
   variabile a zone. Arena di Abed-Oscuro.
Mini-boss restanti: turkey/"Fabbro fantasma" (villaggio), jumpingacorn
mid-boss (radura) — mettili anche nel pool degli slot generativi.

## §POTERI E SISTEMI (per S7)
- **Super combinati co-op** (entrambi al 100%, insieme): matrice COMBO_SUPERS;
  Troy+Abed="SPARANO LAVA", default="ABBRACCIO DI GRUPPO" (cura+stun).
- **Livelli super** (ogni 5 usi, I→III); **boss rush** + **speedrun timer**;
  **Incubo** con modificatori combinabili stile Hades; **pagina achievement**
  al titolo ("Streets Ahead" no morti, "Sei stagioni e un film" 100%,
  "Cool cool cool" primo combo super, + inventane nel tono giusto).

## §ARTE E AUDIO
- Parallax e meteo: ✅ fatti (v10.5). Mancano: transizioni a cerchio retro
  tra livelli, neve segreta, glitch-meteo del Dreamatorium.
- Musica a layer + stinger: ✅ fatti (v10.6). Sempre WebAudio.
- VFX esterni (Foozle/pimen) SOLO per super e boss, non rumore di fondo.

## §SESSIONI — campagna guidata (una per volta, in ordine)
Ogni sessione: leggi questo file → esegui → criteri accettazione → rituale
di fine (§FINE SESSIONE). Non sforare nello scope della sessione successiva.
- **S1-S4**: ✅ COMPLETATE (v10.1-v10.6, dettagli in CONTESTO): registri +
  quest-engine + Atti I-II; scheletro generativo + endless; perk + juice;
  armi + sinergie + economia + boss delle profondità + audio a layer.
  Pool CHUNKS, PERKS, WEAPONS e SYNERGIES: espandibili in ogni sessione
  (nuove armi/sinergie = righe nei registri, boss nuovi = chiavi MBOSSES).
- **S5 — MONDO VIVO** (priorità utente: uccidere l'"asettico"; §RICERCA.
  Data-driven, glifi PS5, mini-guide in tono. Spezzata in tappe):
  - **tappa 1 ✅ (v10.7)**: MINIMAPPA (drawMinimap, segue il pg, toggle Opz.).
  - **tappa 2 ✅ (v10.8)**: mosse base (doppio salto/scatto/parete) ora GRATIS
    e SUBITO (`BASE_ABIL`, richiesta utente); l'Albero è diventato NEGOZIO in
    Monete (`SAVE.wallet`) con 7 poteri AVANZATI (triplo salto, scatto doppio/
    tagliente, ali di falco, schianto sismico, scatto-specchio, calamita) che
    restano per sempre in `SAVE.meta`; INTERACT open-world: molla 'J', blocco
    segreto 'S' (solido, si sfonda con lo SCATTO → premio); motore `GUIDE`
    hint-on-approach voce-Abed una-tantum (SAVE.flags.seen). +4 armi. VFX
    `firework` da asset esterno CC0 (repo hawkthorne, `playFX`/`fxShots`).
  - **tappa 3 (prossima)**: altri INTERACT (leva→cancello gated dalle abilità,
    torcia, cassa esplosiva, blocco spingibile, corrente, appigli/mantle,
    pogo, combo aeree); AMBIENTE VIVO (bestioline, chiacchiere NPC). Poi
    POTERI = registro `SPELLS[]` elementale (fuoco/ghiaccio/fulmine/vento)
    cast chainabili mentre scatti, colori-firma, 4 slot HUD, chiavi colorate.
    BASE della magia HP (S6). AMPLIA gli asset: scarica+inline altri sheet CC0
    (repo hawkthorne ha fire/firework/sparkle/splatters/steam; OGA/Kenney per
    incantesimi), verifica il layout a griglia prima di cablarli.
- **S6 — GREENDALE + SCUOLA DI MAGIA (Atto III/IV, HP integrato)**: campus
  (Dean+quest, Chang boss EL TIGRE, Leonard, mini-boss villaggio), Atto III;
  Paintball segreto + Atto IV (personaggi malvagi, Dreamatorium + Abed-Oscuro).
  **HARRY POTTER INTEGRATO** (tono Ricky Gervais — comico, assurdo, crudele
  ma mai col cast): la magia elementale della S5 diventa BACCHETTE/incantesimi
  usabili in tutto il gioco + mondo-vetrina "SCUOLA DI MAGIA E STREGONERIA DI
  GREENDALE" (ingresso: armadietto 9¾, muso al muro la prima volta). Cappello
  Parlante = il DEAN che smista insultando ("Casa Tassofrasso-Wipes, sez. B").
  Case: Grifondork, Serpeverde-Chang, Corvo-Nadir, Tassofrasso-Wipes (sponsor.)
  con punti-casa che toccano l'economia della run (stile Terraria happiness).
  Pierce = "Difesa Contro le Arti Noiose" (già wizard, Laser Lotus canonico).
  Boss **LORD CHANGEMORT** (Chang calvo, serpente di feltro, terza persona).
  Boccino d'Oro = ANNIE'S BOOBS che ha rubato la pallina. "Quidditch" =
  raccogli-monete a gravità ridotta su scope del custode. Abed commenta
  quanto sia "legalmente distinguibile da qualsiasi franchise noto".
  **SET HP AMPLIATO (richiesta utente)**: incantesimi-firma come poteri/boon
  — "EXPULSO-CHANG" (respinta), "WINGARDIUM CACIOSA" (solleva blocchi/nemici
  gialli = chiave-colore), "SVEGLIUS TOTALIS", "PATRONO: UN ABED OLOGRAFICO",
  "AVADA KEBABRA" (spell proibito di Star-Burns, ti costa un cuore); pozioni
  di Shirley (Felix Felici-tè), erbologia con la Piantagione di Chang; lezioni
  = mini-stanze a sfida (Trasfigurazione con Troy, Volo con Vaughn); classifica
  Coppa delle Case sul save (punti-casa persistenti); Malandrino's Map =
  la minimappa "sono solennemente un idiota"; sala comune per casa nell'hub;
  Star-Burns = "Severus Piagnataccia". Sprite/effetti CC0 dove servono.
- **S7 — Sistemi e polish**: combo super, livelli super, boss rush, pagina
  achievement, speedrun, transizioni a cerchio, VFX esterni, side-quest,
  slot save + export/import.
- **S8 — Nice-to-have** (solo se tutto sopra è solido): touch iPhone/iPad
  (overlay croce+3 bottoni, pointer events, convivenza con macOS = si attiva
  solo su touch device) + PWA offline; netcode robusto (heartbeat, timeout,
  riconnessione, lerp snapshot, bottone COPIA CODICE); selettore livello dal
  hub post-completamento; endless anche online (serve sync del seed).

## §REGOLE DI LAVORO (compressa V9, sempre valide)
1. Animazioni: test frame-per-frame con `_hawk.step(1)` + screenshot
   consecutivi. Uno screenshot singolo NON rivela sfarfallii.
2. Nemici/boss nuovi: collauda anche in 2P; netcode con `fakeGuest()`.
3. Zero errori console; funziona da file:// E su Pages, prova entrambi.
4. GitHub raw: `sleep 1` tra file, verifica dimensione >5KB.
5. Consegna solo roba TESTATA. Spettacolare sì, rotto no.
6. rAF SOSPESO in headless: niente Promise/rAF negli eval di test, usa
   `_hawk.step`. Diff pixel: soglia >60 (sotto è rumore AA, non un bug).
7. Gli slice python `index()..index()` inghiottono i blocchi inseriti in
   mezzo. Dopo ogni batch: `node -e "new Function(codice)"` sulla sintassi.
8. `_hawk.tp(x, y?)` accetta la Y; quest/flag persistono in localStorage:
   i test riprendono dopo un reload senza rifare la trafila.
9. Eventi periodici su cicli paralleli: moduli coprimi (remix %7, boss %5,
   biomi %4). Overlay full-screen si annullano a coppie (`difference` +
   buio dark): spegnine uno. Nei test di danno azzera `p.inv`.
10. Nei test headless azzera `hitstop` prima di simulare input (li mangia);
   il gamepad NON si simula via eval: pollGamepads sovrascrive GP a ogni
   update — le vie da pad si collaudano a mano.

## §FINE SESSIONE — rituale auto-rigenerativo (obbligatorio)
Al termine di OGNI sessione, in quest'ordine:
1. Verifica criteri di accettazione della sessione (sotto).
2. Commit + push (messaggio: `vX.Y: <sintesi>`).
3. Aggiorna memoria `hawkthorne-assets` se hai introdotto layout/API/asset.
4. Incrementa `GAME_VERSION` in index.html (mostrata nell'angolo del titolo).
5. **Rigenera questo file** come `PROMPT-V10.md` aggiornato (stesso nome,
   sovrascrivi): spunta la sessione completata in §SESSIONI, integra lezioni
   apprese in §REGOLE o §TOKEN (max 3 righe nuove, elimina regole diventate
   ovvie), aggiorna CONTESTO con lo stato reale. Il prompt deve MIGLIORARE
   ad ogni ciclo, non gonfiarsi: budget 260, alzato a 320 finché la §RICERCA
   S4.6 non viene consumata dalla S5 (poi riassorbila e torna a 260).
6. Riporta all'utente: cosa è stato fatto, cosa testare a mano su Safari,
   qual è la prossima sessione.

## §CRITERI DI ACCETTAZIONE (ogni feature)
- Collaudata con `_hawk.step` (inclusi 2P dove rilevante);
- zero errori console; ok da file:// e su Pages;
- contenuto nei registri dati, non hardcoded;
- commit + push; memoria aggiornata se serve.

## §SPIRITO
Non un porting: una lettera d'amore a Community con ambizioni da gioco vero.
Magie spettacolari, humor nero, meta-narrazione, sorprese. Quando hai
un'idea fuori dagli schemi che rispetta i vincoli: falla. Cool cool cool.
