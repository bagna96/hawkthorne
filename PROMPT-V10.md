# PROMPT V10 — Hawkthorne "Leggendario" (campagna multi-sessione)

> Autosufficiente: contesto, regole, architettura, storia, asset, fasi.
> Leggi PRIMA le memorie `hawkthorne-assets`, `fan-content-fidelity` e
> `game-feel-expectations` (gusti dell'utente: juice + roguelite, PS5).

## CONTESTO (stato v20.0 — S1-S9 + §S-VFX complete, 41 GIOCABILI; prossima:
## residui §S-VFX (HP CC0, extra ninja, più jutsu autentici) o richieste nuove)
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
  ma orfana). PAD (⚠ AGGIORNATO in v20.3, scelta utente): ✕ salto,
  ◯/L2 schivata, ▢ base, △/R2 pesante, L1 POTERE, R1 SUPREMO (grilletti
  studiati: L2 schivata alla Gungeon, R2 pesante alla GoW), croce SU
  cavalcatura / GIÙ interagisci / DESTRA cambia arma (croce SOLO nei menu:
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
- **V14.1 (bug report + feedback "manca contesto, casse inutili, case
  sospese, dov'è Harry Potter?")**: GIN = GALLEGGIAMENTO (la spinta -1.8
  aiuta ma MAI frena una risalita più veloce; GIÙ per immergersi; bracciata
  al pelo = balzo -9.5 con `p.ginLeapT` esente dal taglio del salto
  variabile a -4 di riga ~3014 — quel taglio ammazzava qualsiasi lancio
  verticale esterno: ricordalo per molle/cannoni futuri). ONBOARDING:
  `lvlBanner` in loadLevel (nome mondo + OBIETTIVO dalla quest attiva,
  disegnato in drawHUD per ~4s); GUIDE moneta/cristallo/sigillo/gindown
  alla prima raccolta. Casse: pagano sempre (monete col popup), armi 5%
  anche in campagna, cristalli 18%. HP presto: lettera di ammissione in
  ACTS[1].end, SCOPA gratis alla quest sig_foresta (in questEvent),
  bacchetta nel weaponPool base. Villaggio: facciate procedurali nel
  case 'B' di drawTiles (def.village && ty<14: tetto coppi se sopra è
  aria, porta a ty 13, finestre accese con addLight). Segreti S nuovi in
  M2 (dietro tronco 2) e M5 (sotto la galleria).
- **V14.2 (feedback: flash bianco, "voglio l'autofire", "siamo OP")**:
  flashGrade addolcito (0.12 quadratico; nei verbi storm/freeze/lava il
  lampo fullscreen è SOLO da ult, da pow è flashLight locale — regola:
  mai lampi a schermo intero su azioni frequenti); FUOCO CONTINUO su
  ▢ e △ (pJP→pDown, i cd fanno da rate-limiter) + perk ripetibile
  `rateo` ☕ (+16%/stack ×6, `rateoMul()` su castBase e su tutti i
  `p.hvyCd = w.cd`), riga RATEO nelle stat HUD, perk dalle casse al 10%;
  PRESSIONE: +40% rinforzi walker in campagna, élite dal mondo 2 (55%),
  `raidT`/`updateRaid` = ASSALTI periodici ogni ~35-60s (riusano ambush
  con flag raid, mai in hub/boss). GOTCHA: guardie su `cut` (l'oggetto)
  sono fragili nei test (resta appeso se salti updateCut) — usa `state`.
- **V15.0 (S-OSPITI ✅)**: registro `GUESTS` {anims [y,fw,fh,n] su strip a
  righe, face:-1 = arte GBA guarda a sinistra, scale} + `drawGuestActor`;
  `drawActor` DEVIA in testa se GUESTS[sheetKey] → select/dialoghi/NPC/2P
  gratis; branch guest in drawWalkerInner/drawFlyer/drawMboss (griglia 2
  righe calma/furia + `flip`). GIOCABILI (premi, `needs`+`lockHint` in
  CHARS, flag settato da hitMboss via def.sblocco/sbloccoMsg/ach):
  harry (Changemort→guestHP), naruto/sasuke/rocklee/kakashi (Zabuza→
  guestKonoha). KITS: Expelliarmus/Lumos/EXPECTO PATRONUM (beam+nova),
  kunai/Rasengan/KAGE BUNSHIN (volley 14), shuriken/Chidori(+storm)/KATON
  (lava), Konoha Senpū/Loto/OTTO PORTE (focus), pierce/Raikiri/EVOCAZIONE
  (quake). SCUOLA: spawn gnomo/doxy + lettere-spawn extra `def.spawn[c]`
  (v=tentacula), NPC π=Piton φ=Gazza δ=Silente (groups, ids g_*, NAMES),
  porta '³'→CANE_DEF (corridoio vietato, FUFFI 'Ƒ' hopper 4+4 frame) e
  torii '@'→KONOHA_DEF (bgImg dipinto a parallasse SPECCHIATO anti-cuciture,
  ninja/tigre y/corvo, ZABUZA 'Ƶ' ai-tigre, X bloccata finché vive).
  Luce automatica sul mboss nei livelli dark. Pipeline asset:
  tools_guest_extract.py (scan/preview) + tools_guest_build.py (strip/
  griglie in assets/guest/out/ + guests.json) + tools_guest_inline.py
  (base64→HAWK_ASSETS). Achievement fuffi/hokage.
- **V16.0 (STRANGER THINGS + caos + S-GRAFICA/1)**: crepa 'ψ' nelle
  CAVERNE → gauntlet SOTTOSOPRA in 2 stanze (exitTo accetta anche un DEF:
  stanza2 dichiarata prima della 1) con sfondi dipinti a strati
  (bgImg + bgImg2 alpha, parallasse a specchio): mboss 'Đ' DEMOGORGONE
  (leaper) e 'Ѵ' VECNA (mago, minion demodog) → sblocco guestST =
  UNDICI (bolt pierce/Presa psichica jail/ult nova CHIUDO IO IL CANCELLO)
  e JIM HOPPER (4❤, bolt/quake/ult rain CAFFÈ E CONTEMPLAZIONE). 27
  giocabili. Nemici: demodog/demogrey/demobat (fan-sprite GitHub, vedi
  CREDITS: Sunairaa, Gonzalo6282, elen-c-sales — TSR non ha giochi ST).
  CAOS CRESCENTE: mazzi CAOS_W/CAOS_F pescati da rinforzi+assalti+
  imboscate, p = min(0.85, 0.12+lvlIdx·0.1) — crossover ovunque, misurato
  (demogrey al villaggio, tigri a Greendale, ninja a scuola). S-GRAFICA
  prima consegna: registro TILESETS + texture nel case 'B' di drawTiles
  (esposto=muro, interno=rombi+variante colonna) — Scuola e Corridoio con
  i muri GBA veri di Hogwarts (g_hogtiles da hp_hallways, bordi rattoppati
  via builder). Luce automatica sul mboss nei livelli dark. Strip pesanti:
  quantizzazione FASTOCTREE+alpha binaria nel builder (37KB→4KB).
- **V17.0 (S8 ✅ tutti gli 8 punti)**: COMBO_SUPERS (2 supremi entro 90f
  in co-op = attacco combinato; chiave = id ordinati '+', fallback
  _default; Troy+Abed SPARANO LAVA); LIVELLI supremo I→III ogni 5 usi
  (SAVE.ultUses, castUlt scala dmg/r/t/n, numerale nel banner, ach
  super3); BOSS RUSH dal titolo post-game (RUSH_SEQ 10 mini-boss in
  arena RUSH_DEF def.rush, cuore di cortesia tra i capi, cronometro,
  SAVE.rushBest, rushMode da azzerare anche in 'over'); pagina
  ACHIEVEMENT (state 'ach', contatori progresso); TIMER SPEEDRUN
  (opts().timer, HUD basso-destra, SAVE.speedBest al win); TRANSIZIONE
  A IRIDE (wipeKind 3 al 70%, cerchio (1-k) sul player, kitsch al 30%);
  MODIFICATORI INCUBO alla Hades (registro INCUBI, SAVE.incubi, effetti
  in addWallet/loadLevel/startRun/updateRaid, +15% monete l'uno, menu
  'incubi' dal titolo quando Incubo è ON); SLOT ×3 (hawk_slot, chiave
  storica = slot 1) + ESPORTA/IMPORTA base64 via prompt. GOTCHA: award()
  è muto con cheatDirty; le cut nei test si saltano con _hawk.next().
- **V18.0 (S9 ✅ tutti i punti)**: TOUCH iPhone/iPad (TOUCH_BTNS mappati
  sui tasti P1 → funzionano in gioco E nei menu, slide tra pulsanti,
  compaiono al primo tocco, disegnati sopra il CRT); PWA offline (sw.js
  cache-first — BUMPARE `CACHE='hawkthorne-vN'` a ogni release! —
  manifest + icone 192/512, registrazione SOLO https, file:// intonso);
  netcode: heartbeat 2s/drop 8s via net.lastMsg, onconnectionstatechange,
  COPIA CODICE automatica negli appunti; CARTELLO fast travel nel hub
  (tile 'j', GIÙ → state 'lvlsel', SAVE.maxLvl in loadLevel, fallback
  SAVE.finished→8); ENDLESS ONLINE (snapshot gd:[seed,depth], l'ospite
  rigenera con genLevel in locale — deterministico, verificato). Nei
  test: TouchEvent veri con new Touch({target: cv, ...}).
- Debug: `.goto(n | 'konoha'|'cane'|'paint'|'sotto'|'vecna') .char(id) .step .tp .soul
  (azzera anche i cd) .super(=castUlt) .pow .kill .dmg .beatRival .p2
- **V18.1-18.3 (feedback telefono + co-op)**: STICK virtuale (registro
  STICK, soglie L/R 32% giù 45% SU 60%) + rombo PS generato da TB_C
  (mai coordinate a mano); ✕/Space conferma OVUNQUE (select, updateMenu,
  over, win, netbit ok); grantShards→coinsRun e sblocchi guest* inviati
  all'ospite online (subito alla kill + fine livello) e salvati sul SUO
  profilo. Bump cache sw.js a OGNI release.
- **V19.0 — +14 GIOCABILI Konoha (41 totali)**: gaara hinata neji guy
  tenten temari ino kiba choji shino itachi tsunade sasori kankuro
  (tutti needs:'guestKonoha', kit dedicati — vedi commit e8c3b69).
  Pipeline `nc_char` in tools_guest_build.py: sheet NC etichettati →
  split su barre nere, ordine sezioni FISSO (0 Idle · 2 Running · 5 Jump
  · 7 Throw=cast · 11 Combo1=atk · 15 Hit · 18 OnGround); non etichettati
  → chroma + rimozione globale delle 2 tinte-riquadro; key_trim ITERATO;
  personaggio nuovo = 1 riga in NC_CAST. Deidara = sheet rotto, rimandato.
  SELECT A SCORRIMENTO (finestra 3 file segue selIdx). LIBRERIA: ~180
  sheet in assets/guest/src_tsr/ (tools_tsr_dl.py manifest; catalogo
  visivo: tools_tsr_catalog.py → jpg in scratchpad).
- Debug: `.goto(n | 'konoha'|'cane'|'paint'|'sotto'|'vecna') .char(id)` +
  .give .gems .boon .forge .incubo .next .fakeGuest .reset .info(+mboss/
  nEnemies/nGroups/guests/fail) .quest .mbkill .gen .remix .arma .pom
  .maledici .syn .god .perk .shards .unlock .ui`.
- **V20.0 (§S-VFX ✅)**: FIRME VFX PER-KIT — richiesta "ogni personaggio effetti
  PROPRI, mai la mezzaluna uguale a tutti". Gli slot dei `KITS` accettano ora
  `fx` (sprite jutsu AUTENTICO via `playFX`), `sig` (firma PROCEDURALE a canvas) e
  `proj` (sprite del proiettile). Mappa `KIT_VFX` = overlay data-driven su tutti i
  41 kit (idempotente, `Object.assign` per slot). `kitFX(p,k,tier)` in castPow/
  castUlt usa la firma del kit; le doppie-mezzelune (slash/slash_p) restano SOLO come
  ripiego. `spawnSig`/`drawSigs` = 10 firme procedurali tinte dal colore del kit
  (orb=chakra, chidori=fulmine, sand=sabbia, wind/blade=vento/taglio, petals=fiore,
  swarm=insetti, gates=porte/gioventù, rune=cerchio magico, holy=croce radiante);
  vivono ~20-34f, si spawnano al centro player. `drawProjKind(pr)` = sprite
  proiettile a canvas (kunai/shuriken/senbon/sabbia/foglia/petalo/insetto/scintilla/
  stella) ruotati e tinti da `pr.pcol`; agganciato in execVerb `shoot` (kind/pcol/dir
  sul proiettile) e nel render dei projs (solo `from==='player'`). ASSET AUTENTICI:
  `fx_rasengan` (3f, Naruto pow) e `fx_katon` (3f, Sasuke/Troy ult) ritagliati dagli
  sheet DS vs-Sasuke con `tools_fx_extract.py`. Base autofire tiene il flourish
  leggero (differenziato dai proiettili); pow/ult sono le firme grandi.

## §S-VFX ✅ FATTO (v20.0) — firme per-kit; RESIDUI per la prossima
Consegnato il CUORE: registro VFX per-kit (`fx`/`sig`/`proj` sugli slot dei KITS +
mappa `KIT_VFX`), `kitFX`/`spawnSig`/`drawSigs`/`drawProjKind` — dettagli in CONTESTO
V20.0. Jutsu autentici estratti: `fx_rasengan` (Naruto) e `fx_katon` (Sasuke/Troy) con
`tools_fx_extract.py`. Artifact proposte originali: claude.ai/code/artifact/c0f88173.
RESIDUI (scelte utente già prese, riprendili quando capita):
1. NARUTO — più jutsu AUTENTICI dagli altri fx_* di src_tsr/
   narutoshippudennarutovssasuke (rasenbomb #98915, otto_porte #98911,
   beast_hammer #98917, shadow_bind #98916...): griglie IRREGOLARI a più
   sezioni (bande e frame di dimensioni diverse) → usare `tools_fx_extract.py`
   detect_bands()/detect_cols() e verificare a schermo 1 sheet alla volta;
   assegnarli a `pow.fx`/`ult.fx` dei kit ninja al posto delle firme procedurali.
   Upgrade animazioni ospiti dai loro sheet personaggi (opz.). ❌ NIENTE draghi.
2. HP H2 ✅ FATTO (v20.1): pack CC0 'Pixelart Spells' montato — fx_lumos ('Bolt
   Of Purity' tinto oro, pow) + fx_patronum ('Light Bolt' tinto argento, ult,
   plana avanti con fxv:3.5); beam tinto dal col dell'ult del kit. Tinta =
   moltiplicazione RGB per luminanza (NON hue-shift: gli sprite sono quasi
   bianchi), 3× nearest. Il resto del pack (22 strip: fire/water/ice/darkness/
   wind/arcane/shield...) è in scratchpad e su OGA: riusabile per altri kit.
   RESTA di HP: H1 pose bacchetta da hp_harry (upgrade animazione); bestiario GBC
   (src_tsr/harrypotterthechamberofsecrets) per Scuola/caos: Basilisco, folletti,
   mandragole, Weasley NPC.
3. RON/HERMIONE/VOLDEMORT: ROM GBA/PSP = VICOLO CIECO (regole 28-29). Strade vive:
   (a) fan-sheet DeviantArt (the-super-spriters Naruto; per HP cercare) → PROPORRE
   IMMAGINI prima; (b) l'utente cattura da emulatore e li ricompongo io.
4. GIOCABILI EXTRA gratis: Pain/Sai/Karin/Suigetsu/Jugo da src_tsr/narutoshinrumble
   (layout DIVERSO da NC: mapper da adattare); Deidara con Shinobi Rumble (73406).

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
- **S-OSPITI ✅ COMPLETATA (v15.0)** — Harry/Naruto/Sasuke/Rock Lee/
  Kakashi giocabili, creature HP a scuola, Fuffi, Konoha+Zabuza, NPC
  Piton/Gazza/Silente (dettagli in CONTESTO V15.0). RESIDUI quando
  capita: Gaara/Itachi/Haku/Hinata/Jiraiya (sheet piccoli 152×200,
  layout 4 bande da decifrare — gli altri 28 png grezzi restano in
  assets/guest/); Ron/Hermione/Voldemort via pipeline spriters-resource
  (pagina asset → `/media/assets/<bucket>/<id>.png`, il /download/ è
  dietro Cloudflare; slug: game_boy_advance/harrypotter*, .../narutorpg,
  .../narutoninjacouncil(2), ds_dsi/narutopathoftheninja; curl -A
  Mozilla + sleep 1); ninja del suono nel Dreamatorium; lezioni della
  scuola come mini-stanze; Quidditch a gravità ridotta (residui S7).
- **S-GRAFICA — OLTRE L'8-BIT, AVVIATA in v16** (cast Community resta
  pixel-48 SACRO). FATTO: registro TILESETS + texture 'B' in drawTiles
  (Scuola+Corridoio con muri/rombi Hogwarts); sfondi dipinti a doppio
  strato (Konoha 1 layer, Sottosopra bgImg+bgImg2). RESTA, un mondo alla
  volta: (1) texture per '#' e per i biomi 1-6 (cercare CC0: OGA/Kenney
  zip via curl; oppure altri crop da hp_greathall/library/potions);
  (2) sfondi dipinti sopra le colline dei mondi 1-5 (nrpg_battlebg ha
  altre 8 celle pronte); (3) sprite ambiente hi-res (arredi dai tileset
  Hogwarts, lampioni, alberi); (4) VFX con più frame e glow; (5) sprite
  ambiente a 2× nativo per l'HD interno già attivo.
- **S8 ✅ COMPLETATA (v17.0)** — tutti gli 8 punti consegnati (dettagli
  in CONTESTO V17.0). Residui possibili: più coppie nella matrice
  COMBO_SUPERS (ne esistono 6 + fallback); boss rush con Cornelius
  finale (ora solo i 10 mini-boss); classifica speedrun per personaggio.
- **S9 ✅ COMPLETATA (v18.0)** — tutti i punti (dettagli in CONTESTO
  V18.0). La "riconnessione" vera resta fuori scope con la firma a
  scambio manuale di codici: la linea che cade viene gestita con garbo
  (host continua solo, ospite al titolo). ROADMAP S1-S9 TUTTA CHIUSA:
  le prossime sessioni nascono dai residui (S-GRAFICA biomi 1-6, cast
  Naruto restante, Ron/Hermione/Voldemort, Quidditch, lezioni-stanze,
  Cornelius nel boss rush) o da richieste nuove dell'utente.
- **§S-VFX ✅ COMPLETATA (v20.0)** — firme VFX per-kit (fx autentico / sig
  procedurale / proj sprite) su tutti i 41 kit; jutsu autentici rasengan+katon
  estratti dagli sheet DS. Dettagli in CONTESTO V20.0. RESIDUI in §S-VFX qui sopra:
  più jutsu autentici dagli altri fx_* (griglie irregolari), HP CC0 Pixelart Spells
  (H2) + bestiario GBC, giocabili extra Pain/Sai/Karin/Suigetsu/Jugo.

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
24. Sheet GBA rippati: DUE sfondi da rimuovere — quello esterno (pixel
    0,0) E i RIQUADRI-CELLA dietro ogni frame (colore diverso!). Se la
    segmentazione trova segmenti tutti larghi uguali (es. 40), stai
    segmentando i riquadri, non gli sprite: serve `key_trim` per-frame
    (tools_guest_extract.py). L'arte di battaglia GBA guarda a SINISTRA.
25. Mappe bonus scritte a mano: SEMPRE muri B ai bordi (senza, il
    giocatore esce dal mondo e rinasce allo spawn) e porta X alta 3 tile
    anche lì. Il taglio del salto variabile castra i `vy` iniettati nei
    bot: simulare il salto con justPressed['Space'] + keys tenuto.
    Normalizzare le righe via script (ljust+bordi+X), mai contando spazi.
26. `_hawk.mbkill()` è NO-OP mentre `mboss.hurtT > 0`: se il bot autofira,
    il "kill" può essere un fantasma — chiamarlo in loop finché
    `mboss.dead`, e verificare lo sblocco, non l'intenzione.
27. IP senza rip su TSR (es. Netflix): cercare FAN-REPO su GitHub —
    `gh api search/repositories` + `git/trees/HEAD?recursive=1` filtrato
    su png, poi raw.githubusercontent. Qualità sorprendente (Undici,
    Hopper, Vecna). Accreditare il repo in CREDITS.md.
28. ROM commerciali: GBA/DS di Tomy, Griptonite ed EA usano compressioni
    e archivi CUSTOM (zero LZ77 BIOS, zero NCGR): lo sweep dice subito
    se c'è trippa — se no, NON insistere: TSR/fan-sheet battono il
    reverse engineering 9 volte su 10. MAI `git add -A` con ROM nel
    repo: iso/ è in .gitignore per sempre (incidente 8GB sfiorato).
29. La cartella `iso/` è SOLO locale (copyright + dimensioni): niente
    GitHub. Il backup del gioco è il repo remoto; le ROM se le tiene
    l'utente. Cache PWA (sw.js): bump del nome a ogni release.
30. Sheet fx_* DS (vs-Sasuke): fondo NON fisso (verde 0,136,64 / teal 0,160,160 /
    verde-chiaro 80,152,80) + riquadri-cella ciano (0,255,255). Key robusto che
    toglie tutto MA preserva orb (r≈g<b) e fiamme (r>g): `bg = a<20 OR (r<g-25
    AND b<g+50)`. Griglie IRREGOLARI a più sezioni → `tools_fx_extract.py`
    detect_bands/detect_cols, mai coordinate a mano; verifica a schermo 1 sheet
    alla volta (montaggi con sprite personaggio misti agli fx). Il registro VFX usa
    strip SINGLE-ROW (riga 0): estrai celle uniformi affiancate.
31. Collaudo VFX: le firme (`spawnSig`) si spawnano al CENTRO player → se x è piccolo
    finiscono DIETRO l'HUD (tp al centro). `_hawk.pow` su char col verbo `jail`
    (gaara/ino/abed/eleven/sasori/kankuro) TRASFORMA il player in char casuale
    (jailbreak): `_hawk.char` sembra rotto ma è il jail → RICARICA la pagina prima di
    ogni char per test puliti. rAF del pannello in PAUSA: `_hawk.step(1)` in loop per
    bruciare `wipeT`+animare, poi screenshot (il canvas trattiene l'ultimo frame).
    Base autofire nei test: `dispatchEvent(new KeyboardEvent('keydown',{code:'KeyX'}))`
    + step (il listener setta `keys[]`, che NON è su window).

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
