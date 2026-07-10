# PROMPT V10 — Hawkthorne "Leggendario" (campagna multi-sessione)

> Autosufficiente: contesto, regole, architettura, storia, asset, fasi.
> Leggi PRIMA le memorie `hawkthorne-assets`, `fan-content-fidelity` e
> `game-feel-expectations` (gusti dell'utente: juice + roguelite, PS5).

## CONTESTO (stato v12.0 — Sessioni 1-7 completate)
Progetto `~/hawkthorne`: platformer 8-bit tributo a Community S3E20
"Digital Estate Planning". Live: https://bagna96.github.io/hawkthorne/
(repo `bagna96/hawkthorne`, branch main, GitHub Pages).
- `index.html` = gioco COMPLETO single-file (~1.8MB, asset base64 inline in
  HAWK_ASSETS; ogni chiave DEVE anche essere registrata con `loadImg` — v. regola 14).
- 20 personaggi giocabili (sprite autentici Project Hawkthorne), costumi,
  super a barra Meraviglia, tratti passivi, boons, scivolata/schianto,
  co-op locale 2P + online WebRTC, gamepad PS5+rumble, musica procedurale
  WebAudio, save localStorage `hawk_save`.
- **CAMPAGNA 10 livelli**: 0 hub · 1 radura · 2 foresta (Re Ghianda) ·
  3 villaggio · 4 lago di gin · 5 caverne (Gilbert) · 6 GREENDALE (Chang) ·
  7 SCUOLA DI MAGIA (Changemort) · 8 trono (Cornelius) · 9 DREAMATORIUM
  (Abed-Oscuro, post-game via porta '7' nel hub) + `PAINT_DEF` livello
  segreto paintball (porta '8' a Greendale, `exitTo` per uscirne).
- V10.1-10.11 (S1-S5): registri ENEMIES/VFX/ACHIEVEMENTS/QUESTS+engine/
  MBOSSES/ACTS/BIOMES/CHUNKS + genLevel seeded + remix Linea Oscura +
  endless + sfida del giorno; PERKS 1-di-3 + juice (hitstop, squash,
  coyote, popup, meteo, parallasse); WEAPONS (16) + SYNERGIES + pom +
  cassa maledetta + boss profondità (boss2 a fasi); minimappa; meta-
  progressione SAVE.meta + NEGOZIO abilità in Monete; INTERACT (molla J,
  segreto S, barile !, leva =+cancello 9, torce i/I che illuminano,
  corrente :, barriera *, altare A, turno di notte); SPELLS elementali a
  combo (Q/L2); GUIDE voce-Abed una-tantum; suolo vivo; critters; glitch
  comici; menu leggibili.
- V11.0 (S6, HD-2D): risoluzione interna 2× (`HD`/`applyHD`, toggle in
  Opzioni), luce dinamica con bloom su `lightCv` (`addLight`/`flashLight`),
  `drawGrading` (tinta bioma+vignette+flash), sfondi organici (colline
  quadraticCurve, sole con god rays, nebbia, silhouette), `softShadow`,
  riflesso nel gin, pannelli `rrect`/`panel`, `_hawk.ui()` smoke-hook.
- **V12.0 (S7 + 4 fix utente)**:
  · FIX cubo: `mb_acorn` e `fx_bolt` NON erano mai stati inline-ati (il
    Re Ghianda era il fallback fillRect marrone!) → iniettati; hopper ora
    con telegraph '!' (20f, suono `hop` soffice), atterraggio `thud`
    gentile, ogni 3 salti `restT`=70 vulnerabile ×2 (`hitMboss`), guida.
  · PAUSA interattiva: `pauseItems`/`updatePause`/`drawPause` (riprendi/
    comandi=stato 'help'/opzioni/trucchi/torna al menu con conferma);
    `menuFrom` = i sottomenu options/cheats tornano a chi li ha aperti;
    trucchi con "SPEGNI TUTTO"; navigabile da pad (start=pausa).
  · VFX ANIME (richiesta Naruto/DBZ): 5 strip CC0 da OGA "Weapon Slash"
    inline (fx_slash oro / _b blu / _p viola / fx_streak / fx_arrow,
    126×150×6, vedi CREDITS.md); `playFX(id,x,y,s,{rot,flip,vx,vy})` +
    blend 'lighter' in drawFXShots; agganci: attacco melee (grande con
    arma), scivolata+scatto (streak), castSpell (colore-elemento, ×1.5 se
    combo), super (doppia mezzaluna incrociata), critici e fulmine
    (slash_p), hitMboss; aura DBZ (particelle dorate) a Meraviglia 100.
  · MUSICA ripulita: `initAudio` crea MASTER gain + lowpass 6200Hz; blip
    con micro-attacco 8ms (niente click); `musicLayers` CONTESTUALE
    (0=hub, 1=base, 2=+armonia/charleston, 3=boss/notte/combo≥5 — prima
    la campagna era sempre 3); mix ridotto, UNA cassa, melodia triangle
    ai layer bassi.
  · GREENDALE (lvl 6, `campus:true`, spawn studente=garrett char-sheet):
    Dean marker 'd' (3 moduli 7-bis = quest `scartoffie` collect Z con
    contatore `q.n`+SAVE.qcnt), Leonard 'L' variante campus, Garrett 'r'
    evento 'panic' (3 pipistrelli), Hilda, lockers 'l' (decor), porta
    segreta '8'→PAINT_DEF, boss `E` CHANG EL TIGRE (ai 'tigre': pace→tel
    26f→carica orizzontale→muro=stun `restT` 60 vulnerabile; enraged
    fulmini a pioggia grav). Arena delimitata da 'B' singoli a riga 13.
  · SCUOLA DI MAGIA (lvl 7, dark+torce, song 'school' valzer minore):
    ingresso SOLO da armadietto '¾' (GIÙ) → prima volta smistamento del
    Dean-Cappello (`enterScuola`/`assegnaCasa`); registro `CASE` (4 case,
    bonus economici VERI: grifondork +10% monete in addWallet, serpechang
    +monete da kill, corvonadir +cristalli da casse, tassowipes -10%
    menuCost); punti-casa da kill nei lvl 6-7 (`addHousePts`) + COPPA a
    fine Atto III (`assegnaCoppa`, +60 se vinci); corrente ':' col 67 →
    Boccino Z + scimmia M in alto; boss `K` LORD CHANGEMORT (ai 'mago':
    lévita, teletrasporto telegrafato vicino al player + ventaglio mirato,
    enraged evoca minion). Arma nuova `bacchetta` "AVADA KEBABRA (REPLICA)".
  · ATTO III (ACTS[3], intro lvl 6) = scartoffie+el_tigre+boccino+
    changemort; ATTO IV (ACTS[4], intro lvl 9) post-game: porta '7' nel
    hub (richiede SAVE.finished) → DREAMATORIUM (`dream:true` = tile
    olografici ciano disegnati al posto di #/B), nemici `evil_*`
    (char-sheet + hue-rotate 180° + pizzetto di feltro disegnato), boss
    `N` ABED-OSCURO (ai 'mago', minion evil_troy, goatee:true).
  · ENEMIES ora supportano `char:true` (sheet-personaggio 12×16: walk row
    1 cols 1-3, flip via scale) + `evil:true`; MBOSSES idem (`char`,
    `filter`, `goatee`, walk/attack rows 1/9). mkEnemy: y = y+(32-h).
- **V13.0 (feedback utente: "combattimento statico, troppo Mario, armi
  corte, potenziamenti invisibili")**: COMBATTIMENTO ALLA LoL — registro
  `KITS` (20 campioni: base/pow/ult con nome+icona+col comici) + motore
  `execVerb` a 16 verbi (bolt cone wave nova beam rain volley storm freeze
  heal slow focus jail dashstrike quake lava, `extra` concatenabile);
  ▢ = `castBase` POTERE BASE a distanza senza cd (rateo 8-14f, livelli:
  `baseLvl` = 1 + pbase2/pbase3 shop + boons.baseUp perk; lv2 pierce,
  lv3 doppio); △ = ATTACCO PESANTE con arma (`p.hvyCd`, gittata aw ×1.4);
  L1/L2/Q = `castPow` (cd k.cd×60 frame); R2/R = `castUlt` (cd max 600f,
  banner testo gigante + flashGrade + doppia mezzaluna + firework);
  god/infSoul azzerano powCd/ultCd; barra Meraviglia SOSTITUITA da 2
  barre cooldown con icone kit (drawSoul riscritta); aura DBZ quando
  l'ult è pronta. SPELLS elementali assorbite nei kit (castSpell resta
  ma orfana). PAD rimappato (scelta utente): ◯/R1 schivata, ✕ salto,
  ▢ base, △ pesante, L1/L2 potere, R2 supremo, croce SU cavalcatura /
  GIÙ interagisci / DESTRA cambia arma (la croce muove SOLO nei menu:
  `state !== 'play'` nel pad-mapping); tastiera X/C/Q/R/E/Shift/Tab, P2
  F/G/H/J/T/Y/U; NETBITS estesi (heavy/pow/roll/wswap/mount). CAVALCATURE:
  registro `MOUNTS` (scopa glide ×1.5 / unicorno ram ×1.75 / drago fly
  200f ×1.4), righe mount_* in ABILITIES, `cycleMount` su pJP('mount'),
  `drawMount` procedurale (×1.6 sotto il player), assorbono un colpo
  (hurtPlayer smonta). HUD ISAAC: colonna icone boons/perks a destra
  (con livello pom), pannellino stat vive ATK/GIT/VEL/❤ sotto i cuori.
  PERK IN CAMPAGNA: porta X (lvlIdx>0) → `openPerks(next)` con `perkNext`
  callback (fallback endlessNext), pom/banco solo endless; 8% perk
  diretto da breakCrate. HOMING: steering nei projs (rot max 0.22/f,
  raggio 270), perk 'homing' (Mirino di Annie), Annie base homing di
  default, trucco TUTTO-HOMING. Trucchi nuovi: VOLO LIBERO (flyMode),
  MONETE A PIOGGIA (coinRainT 600), COOLDOWN AZZERATI (ex infSoul).
  Tutorial e stato 'help' = TABELLA Azione|Pad|Tastiera. Kit mostrato
  nella schermata select al posto della vecchia SUPER.
- **V14.0 (feedback: "i livelli si assomigliano, la campagna non aggancia")**:
  RIDISEGNO MONDI 1-5 con identità meccanica per mondo, generati da
  `tools_build_maps.py` (griglia+primitive ground/pit/solid/plat/door,
  riproducibile: modifica lo script, rilancialo). MECCANICHE NUOVE:
  piattaforme MOBILI tile 'm'/'n' (orizz/vert → entità `movers[]`,
  `mkMover/updateMovers/rideMovers` trasporta il player, `drawMovers`
  con ingranaggio), assi SBRICIOLANTI 'q' (one-way come '-', `crumbleAt`
  22f di tremolio → via, rinascita 300f via `crumbBack`), IMBOSCATA '&'
  (sacco d'oro-esca → `ambush` ondata 4-8 spawn scaglionati → +25 monete
  e arma 50%). Mondi: M1 apertura-aggancio (monete→molla→cassa in 10s,
  alto ricco/basso coi nemici, torre Sigillo, segreto S), M2 verticale
  (tronchi con archi, chiome, corrente, arena RE Ghianda con sponde),
  M3 tetti vs strada (campanile+corrente, barili a domino, leva+cripta,
  imboscata in piazza), M4 zattere mobili + isole A PELO di gin (montarle
  nuotando dev'essere gratis) + tesoro sommerso, M5 ponti 'q' sulla lava,
  leva+muro A SOFFITTO (walljump scala qualsiasi muro più basso!),
  ascensore 'n', imboscata al buio. QoL: leve tirabili da PROIETTILI
  (tolleranza 2 righe sotto: il ▢ spara ad altezza petto/salto) e con
  GIÙ (croce=interagisci); porte X alte 3 tile A FILO del bordo destro
  (i giocatori le mancavano saltando).
- Debug: `.goto .step .tp .soul(azzera anche i cd) .super(=castUlt) .pow
  .kill .dmg .beatRival .p2 .give .gems .boon .forge .incubo .next
  .fakeGuest .reset .info .quest .mbkill .gen .remix .arma .pom .maledici
  .syn .god .perk .shards .unlock .ui`.

## §RICERCA-GIOCHI — residuo utile
- **Isaac**: pool drop che si espande ✅; restano stanze segrete nei chunk
  e "cosa hai scoperto stavolta" al game over (parziale: bilancio run ✅).
- **Hollow Knight**: rovine narranti nei biomi, scorciatoie che si aprono.
- Risorse: OGA "Pixel Art Spells" CC0 B/N da ricolorare (per SPELLS),
  Kenney CC0 (zip via curl), repo hawkthorne-journey (fire.png resta).
- Vincolo: scaricare→inline base64, MAI runtime-fetch, MAI librerie.

## §COMICITÀ — playbook permanente (Community + British + Scrubs + nonsense)
Ogni testo nuovo passa per UNA lente: 1. META/Abed (callback, regola-
Beetlejuice, gag ricorrenti); 2. BRITISH/Duncan (understatement, morte=
pratica burocratica); 3. SCRUBS (nickname descrittivi, NPC ostile);
4. NONSENSE IT/EN (supercazzola, nomi burocratici per cose epiche, il
"colmo"). REGOLE: max 2 righe; nome leggibile; crudele mai col cast; la
battuta non interrompe l'azione.

## VINCOLI NON NEGOZIABILI
1. **Single-file, zero dipendenze runtime**. Deve girare da file:// e su
   Pages. Browser utente: Safari.
2. **Sprite Community intoccabili** (cast = hawkthorne-journey autentici).
   Resto: libertà totale, CC0/free ammessi (registrati in CREDITS.md).
3. Testo in **italiano**, ironia british/nera; battute fedeli alla serie.
4. Stile 48px, palette scura. Musica SOLO procedurale WebAudio.
5. Commit frequenti + push. Memoria aggiornata a fine sessione.
6. **PS5-first**: ogni menù navigabile da pad (glifi ✕▢◯△), rumble.
   Difficoltà alla Hades: l'inizio accoglie, la profondità punisce.

## §TOKEN — anti-spreco (obbligatorio)
- MAI rileggere `index.html` intero (~5100 righe + base64): `grep -n`
  con `cut -c1-140` (le righe base64 sono da 300KB!) + read mirati.
- Edit chirurgici; nuovi contenuti = righe nei registri, non funzioni
  ad-hoc (>30 righe per UN nemico = stai sbagliando).
- Batch di 3-5 modifiche, poi UN giro di test.
- Asset nuovi: script python che legge png → base64 → inserisce la riga
  `window.HAWK_ASSETS.chiave = "..."` (MAI far passare base64 nel contesto)
  E la riga `loadImg('chiave', 'fallback')` (regola 14).

## §ARCHITETTURA — data-driven
Registri in index.html: `ENEMIES` (+`char`/`evil`), `VFX` (+`blend`),
`ACHIEVEMENTS`, `QUESTS` (+`n` contatore) + quest-engine, `ACTS` (1-4),
`MBOSSES` (ai: hopper/swooper/leaper/tigre/mago + boss2 a fasi),
`BIOMES`+`CHUNKS`, `PERKS`, `WEAPONS`, `SYNERGIES`, `ABILITIES`,
`SPELLS`, `CASE` (punti-casa), `GUIDE`, `BOONS`, `SONGS`, `LEVELS` (10)
+ `PAINT_DEF`. Tile speciali: k x S J : * A ! = 9 i I l ¾ 8 7 W Z.
Def-flags: hub/boss/gin/dark/village/campus/dream/paint/remix/gen/
bossDepth/exitTo/noExit/givewpn/fall/taunt.

## §ASSET — fonti e pipeline
1. repo hawkthorne-journey (autentico, scriptabile, `sleep 1` anti-429):
   personaggi 12×16 di 48×48 (walk row1 cols1-3 right, left=riga-1, atk
   row9 cols0/4); acorn 220×40 bbox alpha; acornBoss 600×525=8×7 di 75;
   cornelius 200×220 3×5; lightning 432×192 3col; betafish/icebat/hippy/bat.
2. OpenGameArt CC0 (curl diretto su /sites/default/files/...): "Weapon
   Slash - Effect" ✅ usato; "Pixel Art Spells"; Kenney.
3. itch.io free (Foozle/pimen): NON scriptabile, chiedere all'utente.
Regole: verifica visiva prima dell'inline; PIL di sistema è ROTTO su
arm64 → venv in scratchpad (`python3 -m venv venv && pip install pillow`);
registra in CREDITS.md; se non convince, scarta.

## §STORIA — 4 atti ✅ TUTTI GIOCABILI (v12.0)
- Atto I "L'Eredità" (3 Sigilli) ✅ · Atto II "Il Fratellastro" (campioni
  di Gilbert → alleato) ✅ · Atto III "Greendale è infetta" (Dean, EL
  TIGRE, Scuola di Magia, Changemort) ✅ · Atto IV "Linea Oscura"
  (post-game, Dreamatorium, Abed-Oscuro) ✅.
Side-quest ancora aperte (registro QUESTS, atto 0): Annie's Boobs riporta
5 oggetti, statua Guzmán, consegne del Dean.

## §SESSIONI
- **S1-S7 ✅ COMPLETATE** (v10.1→v12.0, dettagli in CONTESTO).
  Residui S7 (non bloccanti, riprendili quando capita): turkey/"Fabbro
  fantasma" mini-boss nel pool; Quidditch vero a gravità ridotta; lezioni
  = mini-stanze a sfida (Trasfigurazione con Troy); pozioni di Shirley;
  sale comuni nell'hub; chunk campus/scuola per l'endless; minimappa
  "Malandrino" (rinominarla quando sei a scuola); daydream-cutaway Scrubs.
- **S8 — Sistemi e polish**: combo super co-op (matrice COMBO_SUPERS,
  Troy+Abed="SPARANO LAVA"), livelli super (I→III ogni 5 usi), boss rush,
  pagina achievement al titolo, speedrun timer, transizioni a cerchio
  retro, Incubo con modificatori alla Hades, slot save + export/import.
- **S9 — Nice-to-have**: touch iPhone/iPad + PWA offline; netcode robusto
  (heartbeat, riconnessione, COPIA CODICE); selettore livello dal hub;
  endless online (sync seed).

## §REGOLE DI LAVORO (lezioni cumulative)
1. Animazioni: test frame-per-frame `_hawk.step(1)`; uno screenshot solo
   non rivela sfarfallii.
2. Nemici/boss nuovi: collauda in 2P; netcode con `fakeGuest()`.
3. Zero errori console; funziona da file:// E su Pages.
4. GitHub raw: `sleep 1` tra file, verifica >5KB.
5. Consegna solo roba TESTATA.
6. rAF sospeso in headless: usa `_hawk.step`, mai Promise/rAF negli eval.
7. Slice python `index()..index()` inghiottono blocchi: `node -e "new
   Function(...)"` su TUTTI gli <script> dopo ogni batch.
8. `_hawk.tp(x,y?)`; quest/flag persistono in localStorage tra reload.
9. Cicli periodici paralleli = moduli coprimi; overlay full-screen si
   annullano a coppie.
10. Azzera `hitstop` prima di simulare input; gamepad non simulabile.
11. `p.onGround` OSCILLA da fermi: ogni check a terra = `(p.onGround ||
    p.coyote > 0)`.
12. Effetti che bucano uno strato: SEMPRE canvas separato + drawImage.
13. Harness node con canvas-stub: testare SOLO via `_hawk.*` (i let/const
    top-level dell'eval non sono raggiungibili); `_hawk.ui()` disegna
    tutte le schermate. File in scratchpad/smoke.js (ricrealo se sparito).
14. **HAWK_ASSETS non basta**: `loadImg(key, path)` è una LISTA ESPLICITA.
    Una chiave aggiunta al blocco base64 senza la sua riga loadImg NON
    viene caricata (è così che il Re Ghianda è rimasto un cubo per 4
    versioni). Dopo ogni asset nuovo verifica `_hawk.info().assets` N/N
    e `ASSET_FAIL`.
15. Il pannello browser (localhost, non file://) fa girare il rAF ma PUÒ
    throttlarlo: per test deterministici congela con pattern
    `justPressed['X']=true; update(); delete justPressed[...]; draw()` e
    ricorda che i one-shot (fxShots) muoiono in ~12 frame → per lo
    screenshot spawnali con setInterval o disegna subito dopo.
16. I tasti tenuti si simulano con `keys['ArrowDown']=true` (property di
    const, ok) — mai riassegnare `keys`.
17. Marker NPC: lettere in `'pbtaHLDGdsr'` in loadLevel + ramo in
    buildGroups; vengono AGGANCIATI al suolo con groundAt (solo tile
    isSolid, le piattaforme '-' non contano).
18. Il renderer degli anelli (`parts` con ring) assume `t` che parte da
    12: t maggiori = raggio NEGATIVO = crash `arc`. Il raggio ora è
    clampato ≥1, ma spawna comunque anelli con t:12.
19. `wipeT` (transizione PowerPoint) decrementa nel DRAW: nei test col
    pannello (rAF throttlato) resta a mezz'aria — chiama draw() in loop
    o azzera `wipeT = 0` dopo goto.
20. Contenuto nuovo di combattimento = riga in KITS (o verbo in execVerb
    se proprio serve un comportamento nuovo). Le vecchie vie activateSuper/
    castSpell/ability-'ab' sono ORFANE: non aggiungerci sopra.
21. MAPPE: mai a mano — usa `tools_build_maps.py` (primitive su griglia,
    assert sulle tile obbligatorie, iniezione idempotente). Dopo ogni
    rigenerazione l'Edit su index.html va ri-armato (il file è cambiato).
22. COLLAUDO livelli: bot di traversata in eval (destra + salti con
    doppio-salto concatenato + spari + GIÙ periodico + fasi di sola
    camminata quando è bloccato; nel gin: bracciate a spam ogni 7 frame).
    Successo = state 'perk' O lvlIdx cambia. È STOCASTICO: 3 tentativi.
    Il bot NON dimostra i percorsi opzionali (Z su torri): verificali a
    mano con tp. `boons` NON si resetta con loadLevel: azzerala tra i run
    o i perk-pool si svuotano e la porta salta il perk (nextLevel diretto).
23. Muri-cancello: se non arrivano al SOFFITTO, il walljump (mossa base)
    li scala e il puzzle sparisce. Aperture minime 2 tile. Le porte e le
    leve devono essere generose (porte 3 tile, leve con tolleranza).

## §FINE SESSIONE — rituale (obbligatorio)
1. Verifica criteri accettazione; 2. commit+push (`vX.Y: sintesi`);
3. memoria `hawkthorne-assets` aggiornata; 4. `GAME_VERSION` bump;
5. rigenera QUESTO file (spunta sessione, integra lezioni, pota il
consumato, denso ma completo — §COMICITÀ è permanente); 6. report:
fatto / da testare a mano su Safari / prossima sessione.

## §CRITERI DI ACCETTAZIONE (ogni feature)
Collaudata con `_hawk.step` (2P dove rilevante); zero errori console;
ok file:// e Pages; contenuto nei registri; commit+push; memoria.

## §SPIRITO
Non un porting: una lettera d'amore a Community con ambizioni da gioco
vero. Magie spettacolari, humor nero, meta-narrazione, sorprese. Quando
hai un'idea fuori dagli schemi che rispetta i vincoli: falla. Cool cool cool.
