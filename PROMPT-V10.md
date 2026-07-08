# PROMPT V10 — Hawkthorne "Leggendario" (campagna multi-sessione)

> Autosufficiente: contesto, regole, architettura, storia, asset, fasi.
> Leggi PRIMA le memorie `hawkthorne-assets`, `fan-content-fidelity` e
> `game-feel-expectations` (gusti dell'utente: juice + roguelite, PS5).

## CONTESTO (stato v10.5 — Sessioni 1-3 + S3.5 feedback-pass completate)
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
- Debug: `_hawk.goto(n) .step(n) .tp(x) .soul() .super() .kill() .dmg(n)
  .beatRival() .p2() .give(n) .gems(n) .boon(id) .forge() .incubo() .next()
  .fakeGuest() .reset() .info() .quest() .mbkill() .gen(seed,prof) .remix(n)`.

## §RICERCA (S3.6, luglio 2026) — principi per la S4, distillati online
- **ARMI (Dead Cells, "50 weapons")**: ogni arma deve CAMBIARE lo stile di
  gioco, non le statistiche ("a drastic change from what the player had
  before"); se due armi si somigliano, una va rifatta. Feel = suono
  DISTINTO + knockback/recoil proprio + hitstop custom + effetto visibile.
- **SINERGIE (Gungeon)**: coppie NOMINATE (arma+perk, perk+perk) con toast
  di scoperta; offerte pesate verso ciò che completa una sinergia col
  posseduto (Gungeon usa un "synergy factor" ×6 che cala con l'esperienza).
  Le sinergie rendono buoni anche i drop deboli → meno frustrazione.
- **ECONOMIA (Hades)**: upgrade dei perk posseduti con rendimenti
  DECRESCENTI (pom of power); rarità (comune/rara/epica) che scala i
  numeri; scelta della porta con ANTEPRIMA della ricompensa (simboli).
- **RISCHIO (Dead Cells/Gungeon)**: casse maledette = ricompensa forte
  subito + maledizione temporanea (es. "1 colpo = morte per 20 uccisioni");
  il rischio è sempre una SCELTA del giocatore, mai imposto.
- **BOSS 2D**: telegraphing SEMPRE (wind-up visivo+sonoro ≥30 frame prima
  di ogni mossa); 2-3 fasi con pattern nuovi; interfase (boss invulnerabile
  + ondata/piattaforme) per cambiare ritmo; curva di tensione che sale e
  scende. Nel platformer il boss testa abilità GIÀ apprese con timing più
  severo, non meccaniche nuove.
- **GENERAZIONE (Spelunky)**: percorso-soluzione garantito prima, stanze
  template attorno (già nostro approccio). Da aggiungere: stanze FUORI
  percorso col bottino (rischio), stanza-negozio, stanze segrete.
  Riferimento interattivo in JS: tinysubversions.com/spelunkyGen
- **AUDIO (dynamic layering)**: la musica aggiunge/toglie STRATI in base
  allo stato (profondità, combo, boss vicino); bassline propulsiva come
  seconda melodia; stinger per perk/sinergia/boss/clear; nel WebAudio
  routing con pan+compressore e voci come layer separati attivabili.
Fonti: gamedeveloper.com (Dead Cells 50 weapons; Boss Battle Design), wiki
Gungeon (Synergies) e Hades (Duo/Pom), gameasart.com (Spelunky gen),
babyaud.io (chiptune), splice.com (weapon sound), gamedesignskills.com.

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
- MAI rileggere `index.html` intero: usa `grep -n` per localizzare, poi
  `read_file` con offset/length mirati. Il file è ~2600 righe e crescerà.
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

## §POTERI E SISTEMI (per S6)
- **Super combinati co-op** (entrambi al 100%, insieme): matrice COMBO_SUPERS;
  Troy+Abed="SPARANO LAVA", default="ABBRACCIO DI GRUPPO" (cura+stun).
- **Livelli super** (ogni 5 usi, I→III); **boss rush** + **speedrun timer**;
  **Incubo** con modificatori combinabili stile Hades; **pagina achievement**
  al titolo ("Streets Ahead" no morti, "Sei stagioni e un film" 100%,
  "Cool cool cool" primo combo super, + inventane nel tono giusto).

## §ARTE E AUDIO
- Parallax e meteo: ✅ fatti (v10.5). Mancano: transizioni a cerchio retro
  tra livelli, neve segreta, glitch-meteo del Dreamatorium.
- Musica: vedi §RICERCA (layer dinamici, stinger). Sempre WebAudio.
- VFX esterni (Foozle/pimen) SOLO per super e boss, non rumore di fondo.

## §SESSIONI — campagna guidata (una per volta, in ordine)
Ogni sessione: leggi questo file → esegui → criteri accettazione → rituale
di fine (§FINE SESSIONE). Non sforare nello scope della sessione successiva.
- **S1-S3**: ✅ COMPLETATE (v10.1-v10.5, dettagli in CONTESTO): registri +
  quest-engine + Atti I-II; scheletro generativo, Linea Oscura, endless +
  perk. Pool CHUNKS e registro PERKS espandibili in ogni sessione futura.
- **S4 — ROGUELITE LEGGENDARIO** (priorità utente: endless profondo, armi
  vere, audio; applica TUTTA la §RICERCA):
  a) registro `WEAPONS[]` — 6-8 armi a tema Community, una riga l'una:
     {id, nome, tipo:(arco|proiettile|rimbalzo|raggio|smash), vel, danno,
     kb, hitstop, suonoSeed, icona}. Idee: Penna di Annie (rapidissima,
     crit alle spalle), Mazza del Bidello (lenta, lancia i nemici in aria),
     Dodgeball (rimbalza sui muri), Pistola Paintball (precisa, schizzi),
     Keytar di Troy (onda sonora ad arco), Lancia-lava (migra qui).
     2 slot, swap con L1/TAB. Drop: casse (raro), negozio, boss garantito.
  b) registro `SYNERGIES[]`: {coppia:[id,id], nome, effetto} — toast
     "★ SINERGIA: <nome> ★" alla scoperta; `openPerks` pesa ×3 le carte
     che completano una sinergia con l'equipaggiamento attuale.
  c) economia in-run: ogni 2 profondità la scelta include una carta POM
     (potenzia un perk posseduto, rendimenti decrescenti) o il NEGOZIO di
     Hilda; CASSE MALEDETTE viola (perk subito + "1 colpo = morte" per 20
     uccisioni); nel cap end 2 porte con anteprima-icona della ricompensa
     della prossima profondità (perk / monete / arma, stile Hades).
  d) BOSS DELLE PROFONDITÀ ogni 5, in arena-chunk dedicata: riusa MBOSSES
     con 2 fasi + telegraphing (lampeggio+suono 30f prima di ogni mossa) +
     interfase con ondata; dalla 10ª versioni remix. Pietà accessibile:
     se entri con 1 cuore, un cuore garantito nell'arena.
  e) AUDIO: musica a LAYER per bioma (base→batteria→arpeggio, si sommano
     con profondità/combo); stinger perk/sinergia/boss/clear; suono e
     rumble DISTINTI per arma; glifi PS5 in ogni menù nuovo.
  f) pad al 100%: costumi e Incubo selezionabili anche da controller.
- **S5 — Greendale + Atto III e IV** (autoriale; i chunk alimentano S3):
  campus, Dean+quest, Chang boss EL TIGRE, Leonard, Atto III completo,
  mini-boss villaggio; poi Paintball segreto + Atto IV: personaggi malvagi,
  Dreamatorium + Abed-Oscuro (arena generata: procedurale come mandato
  narrativo).
- **S6 — Sistemi, polish e HOGWARTS DI GREENDALE**: combo super, livelli
  super, boss rush, incubo, pagina achievement, speedrun, parallax/meteo/
  transizioni/stinger, VFX esterni, side-quest, slot save + export/import.
  **TEMA HARRY POTTER (richiesto dall'utente, tono Ricky Gervais — comico,
  assurdo, un filo crudele ma mai col cast)**: mondo segreto "SCUOLA DI MAGIA
  E STREGONERIA DI GREENDALE" (ingresso: armadietto 9¾ a Greendale che ti
  fa sbattere il muso al primo tentativo). Il Cappello Parlante è il DEAN
  con un cappello che smista insultando ("Grifondoro? Tu? Sii serio. Casa
  Tassofrasso-Wipes, sezione B."). Le 4 case: Grifondork, Serpeverde-Chang,
  Corvo-Nadir e Tassofrasso-Wipes (sponsorizzata). Pierce = insegnante di
  "Difesa Contro le Arti Noiose" (già in costume wizard, livello 6 Laser
  Lotus = canonico). Boss: **LORD CHANGEMORT** (Chang calvo con serpente
  di feltro, fulmini propri, parla di sé in terza persona). Il Boccino
  d'Oro è ANNIE'S BOOBS che ha rubato la pallina e giudica tutti. Bacchette
  = boons magici temporanei; "quidditch" = minigioco raccogli-monete a
  gravità ridotta su scope che sono chiaramente scope del custode. Quest
  con dialoghi alla Gervais: il narratore Abed commenta quanto sia legalmente
  distinguibile da qualsiasi franchise noto ("per motivi che i nostri
  avvocati definiscono 'importantissimi'").
- **S7 — Nice-to-have** (solo se tutto sopra è solido): touch iPhone/iPad
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
9. Eventi periodici su cicli paralleli: moduli coprimi (remix %5 vs biomi
   %4), o coincidono sempre. Overlay full-screen si annullano a coppie
   (`difference` + buio dark): spegnine uno. Nei test di danno azzera `p.inv`.

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
   ad ogni ciclo, non gonfiarsi: budget massimo 300 righe totali (alzato
   da 260 in S3.6 per integrare la §RICERCA — quando S4 la consuma,
   riassorbila e torna a 260).
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
