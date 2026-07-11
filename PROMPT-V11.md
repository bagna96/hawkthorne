# PROMPT V11 — Hawkthorne "Leggendario": IL CICLO DEL RECENSORE
> Autosufficiente. Leggi PRIMA le memorie `hawkthorne-assets`, `fan-content-fidelity`,
> `game-feel-expectations` (+ `hawkthorne-vfx-iso` se tocchi asset/VFX).
> Cronaca v10→v20.4 in PROMPT-V10.md (ARCHIVIO) e nel git log: NON rileggerli se non serve.

## CONTESTO (stato v20.4)
Progetto `~/hawkthorne`: action-platformer roguelite tributo a Community S3E20.
Live: https://bagna96.github.io/hawkthorne/ (repo bagna96/hawkthorne, Pages, PWA).
- `index.html` single-file (~7300 righe + 101 asset base64 in HAWK_ASSETS+loadImg).
- 41 giocabili (Community sacro + HP/Naruto/ST), KITS a 16 verbi (base ▢ spam /
  pow L1 cd-secondi / ult R1 max10s), campagna 10 livelli in 4 atti + endless +
  boss rush + incubi + co-op locale/online WebRTC + touch iPhone + pad PS5
  (✕ salto · ◯/L2 schivata · ▢ base · △/R2 pesante · L1 potere · R1 supremo).
- Schivata aerea 8-dir alla Celeste (vettore 10px/f, 11f+3 hitstop, scie ghosts[],
  residuo 0.66/0.45, `inAria = !onGround && airT>1`).
- §S-VFX fatto: KIT_VFX overlay (fx sprite autentico / sig procedurale / proj),
  kitFX in castPow/castUlt, drawSigs (10 firme), drawProjKind, fx_rasengan/katon
  (jutsu DS), fx_lumos/patronum (CC0 tinto). tools_fx_extract.py per altri jutsu.
- SW cache-first + AUTO-RELOAD su controllerchange (fix iOS "gioco vecchio").
  Bump `GAME_VERSION` + `CACHE` in sw.js A OGNI RELEASE.
- Intro: tv → title diretto; cutscene lab al primo GIOCA (SAVE.introSeen).

## §RECENSORE — protocollo permanente (NUOVO, vale in OGNI sessione)
Fingi che un recensore severo controlli ogni consegna. Prima del commit, PASS DEL
RECENSORE obbligatorio, con queste lenti (dalla review v20.4 + ricerca):
1. **Onestà semantica**: ogni testo mostrato al giocatore (nomi poteri, guide,
   tabelle, toast) promette ESATTAMENTE ciò che il codice fa. Un nome che mente
   = bocciatura (caso storico: verbo 'jail' su "bara di sabbia").
2. **Feel**: ogni hit ha i 5 strati (anim, suono, VFX, camera, rumble); niente
   flash fullscreen su azioni frequenti; camera e input prima dei contenuti.
3. **Piattaforma primaria = Safari/iOS**: niente API che lì degradano in silenzio
   (ctx.filter per-frame, window.prompt su PWA, rAF assumptions). In dubbio: verifica.
4. **"Cambia il comportamento del giocatore?"**: ogni contenuto nuovo (kit, perk,
   élite, unlock) deve cambiare le DECISIONI, non i numeri. Se no, ripensalo.
5. **Regressioni**: smoke di traversata + zero errori console + asset N/N.
Il pass produce ALMENO 2 difetti trovati nella propria consegna: fixa i rapidi,
logga gli altri in §ROADMAP. Poi commit. Il Recensore boccia (= non consegnare)
se: un testo mente, c'è un errore console, o un criterio §CRITERI è saltato.

## §ROADMAP-REVIEW — 7 sessioni. Si parte SOLO al segnale dell'utente ("R1"…"R7").
Ogni sessione: implementa → pass del Recensore → commit+push → spunta qui +
integra i finding nuovi. Le sessioni sono INDIPENDENTI (ordine consigliato R1→R7).

### ☑ R1 — ONESTÀ ✅ FATTA (v20.5, commit b757559)
Verbo 'trap' consegnato (gabbia visibile tinta kit, nemico fermo+INNOCUO+
picchiabile, dmg 0 = controllo puro, s.n multipli, fallback mboss restT 120);
jail solo abed.ult; ultLv/ultUses al personaggio BASE quando jailed; tupla
netcode estesa (gabbia anche per l'ospite). Audit 41 kit: nessuna bugia di
classe jail residua. PASS RECENSORE: #1 trap-che-uccide fixato (dmg 0),
#2 gabbia invisibile online fixata, #3 vedi FINDING sotto.
FINDING APERTI (da R1):
- `_hawk.fakeGuest()` è ROTTO ("reading 'id'") anche su v20.4 live: PRE-esistente,
  il collaudo netcode della regola 2 è azzoppato. RIPARARLO (in R2 o appena serve):
  probabilmente drawGuest/drawHUD assume campi che il fake non setta.
- 4 mezze-bugie "volley spacciato per evocazione": naruto.ult KAGE BUNSHIN,
  kakashi.ult OTTO CANI, sasori.pow cento marionette, kankuro.ult TUTTO IL
  TEATRO → risolte in R5(b) col verbo 'clone'/'summon'.

### ☑ R2 — FEEL ✅ FATTA (v20.6, commit d7d8f87)
Camera: camF float + lerp 0.12 + lookahead 52 (lead misurato 38px) + deadzone
±44 con bias in caduta (vy>7) + snap su tp + clamp ai bordi; jitter 0px.
Blur/visibilitychange rilasciano tutto; parts cap 600. BONUS GROSSO: riparato
l'OSPITE ONLINE (rotto dalla v13: drawSoul senza kit nella tupla → crash a ogni
frame) — tupla pl estesa (+cdef/powCd/ultCd), kitOf blindata, fakeGuest DI NUOVO
FUNZIONANTE (regola 2 torna valida), cam esposta in _hawk.info per i test.
FINDING: nit 1px residuo asintotico al clamp del bordo (cosmetico, ignorato).
LEZIONE per i test: dopo blur l'inerzia fa ~12px con attrito 0.72 — non è un
tasto incastrato (quello fa 80px): misurare le soglie sul comportamento reale.

### ☑ R3 — PIATTAFORMA iOS ✅ FATTA (v20.7, commit 7ff6f95)
codeBox (DOM, Promise, COPIA con fallback iOS, guardia modalOpen sui listener):
i 5 prompt/alert sono spariti; export/import e scambio codici co-op vivono anche
su PWA standalone. tinted(img, filterStr) + cache: matrice hue/sat/bri del filter
spec calcolata una volta per sheet — ctx.filter: 0 occorrenze (coperti élite,
evil, mboss def.filter, hippy, ospiti, render online). PASS RECENSORE: fixati
2 difetti iOS del mio stesso modal (textarea <16px = auto-zoom; select() nudo
non copia → setSelectionRange). DA PROVARE SULL'IPHONE UTENTE: export + copia.
LIMITE loggato: il modal non è pad-only (serve tastiera/appunti di sistema:
accettato). LEZIONE: su iOS ogni input DOM va a 16px, e la copia va testata
col fallback — mai fidarsi del solo navigator.clipboard.

### ☑ R4 — COMBATTIMENTO LEGGIBILE ✅ FATTA (v20.8, commit b6ff1e4)
Caos cap 0.35; eliteMod scudo/vendetta/campo con glifi 🛡💀📣 + barriera/alone
visibili, spd 1.4→1.2; tiratori 22% (dado PRIMA dell'élite — il Recensore li ha
trovati introvabili col dado dopo); ghost con wind-up lampeggiante; Re Ghianda
lancia 2 ghiande ad arco a ogni atterraggio (cd 50f: senza, 56 projs misurati —
gotcha 11 colpisce anche i mboss!); El Tigre ventaglio di 3 uscendo dallo stun.
FINDING aperti: (a) ventaglio Tigre e lampeggio ghost verificati a codice, DA
VEDERE giocando (mondo 6 / livelli dark); (b) assalti/imboscate non assegnano
mod élite né tiratori (solo loadLevel+notte) — da estendere quando capita;
(c) debug nuovi: nProjs/nShooters/cam in _hawk.info.
--- testo originale della sessione (per riferimento): ---
### (era) R4 — COMBATTIMENTO LEGGIBILE (espansa col feedback utente 11 lug sera:
### "i boss non sparano, i nemici fanno male solo al tocco — peccato")
- CAOS: grep "0.12 + lvlIdx" → cap 0.35 (oggi 0.82 al mondo 7).
- ÉLITE COMPORTAMENTALI: e.mod ∈ {scudo (immune dal FRONTE, colpiscila da
  dietro/sopra, indicatore visivo), vendetta (alla morte 3 proiettili radiali
  LENTI e schivabili), campo (alone visibile che velocizza i vicini)}.
  Glifo sopra la testa per leggibilità. In cambio spd élite 1.4→1.2.
- MOB A DISTANZA (richiesta utente): walker 'shooter' (~18% dal mondo 1+):
  si ferma, telegraph '!' 30f, UNA lobbata ad arco lenta (grav, vel~4,
  from:'enemy'). Tinta dedicata via tinted(). Nei mazzi CAOS.
- TELEGRAFI MELEE (richiesta utente): il ghost si ferma 20f e lampeggia
  prima dello scatto; leaper idem se veloce.
- PATTERN BOSS (richiesta utente): Re Ghianda (hopper): all'atterraggio 2
  ghiande ad arco telegrafate dal salto; El Tigre: dopo lo stun a muro, 3
  bolt a ventaglio lenti. Changemort ha già il ventaglio. TUTTO leggibile:
  proiettili lenti, colore distinto, mai spam.
- ESAME: ogni minaccia schivabile con la 8-dir A VISTA; mod élite leggibili;
  il mondo 7 è tornato SUO; nessun pattern che spamma.

### ☐ R5 — ROSTER PROFONDO (basta fotocopie) — la più grande, può spezzarsi in 2
- (a) AUDIT: script che stampa la tabella id/base/pow/ult (verb+numeri) dei 41
  kit → individua i ~10 più fotocopia (bolt+nova+volley re-颜色ati).
- (b) 4-6 VERBI/TWIST nuovi che cambiano le decisioni: es. 'clone' (bunshin veri
  che attaccano, per naruto ult), 'wall' (muro temporaneo), 'pull' (magnete
  nemici), 'mark' (bersaglio marcato prende +dmg da tutti), 'orbit' (proiettili
  orbitanti). Distribuirli ai kit fotocopia rispettando il canone dei personaggi.
- (c) FIRME: oggi sig:'rune' ×20 e 'blade' ×13 (contati) — la promessa §S-VFX
  è a metà. Nuove sig dedicate (fan/puppet/mind/insetti-verdi/...) e/o jutsu
  AUTENTICI dagli sheet DS residui: rasenbomb/otto_porte/beast_hammer con
  tools_fx_extract.py (detect_bands/detect_cols, griglie irregolari, 1 sheet
  alla volta con verifica visiva). Target: nessuna sig condivisa da >8 kit.
- (d) +10 COMBO_SUPERS tematiche (oggi 6/820 coppie: harry+naruto, gaara+temari,
  itachi+sasuke, jeff+annie, troy+abed c'è già, eleven+undici-varianti...).
- ESAME: ricontare le duplicazioni post; per ogni kit toccato la domanda-cardine;
  bilancio: nessun verbo nuovo che superi il dps dei vecchi di >30% (test dummy).

### ☐ R6 — LA SELECT È UN ELENCO TELEFONICO (bussola del roster)
- Raggruppa per serie con INTESTAZIONI (Community/Greendale/HP/Konoha/Hawkins);
  PREFERITI (☆ su tasto △, SAVE.favs, gruppo in testa); card con le 3 icone
  del kit (base/pow/ult) visibili senza selezionare; salto rapido di gruppo
  (L1/R1 nella select). Scorrimento a finestra ESISTENTE da mantenere.
- ESAME: da pad e da touch, raggiungere QUALSIASI personaggio in <5 secondi;
  vincolo 6 (tutto navigabile da pad); niente regressioni online ('hello' invariato).

### ☐ R7 — DEBITO & DIETA ASSET (prima di S-GRAFICA, obbligatoria)
- POTATURA: castSpell / activateSuper / ability-'ab' orfane — grep dei call-site
  PRIMA (devono essere zero), poi via. SPELLS registry: assorbito nei kit, via.
- DIETA: script che stampa il peso per chiave di HAWK_ASSETS → quantizza i top-10
  (FASTOCTREE+alpha binaria, pipeline esistente); valuta atlas per le strip
  piccole. TETTO dichiarato: index.html ≤ 3MB (oggi ~2+). Ogni asset futuro
  entra solo se il tetto regge (pena: split con cache SW, decidere allora).
- ESAME: smoke run COMPLETO post-potatura (campagna 2 livelli + endless +
  boss rush + select + touch); file più leggero di prima; zero errori.

### ☐ R8 — LA BUSSOLA DEL MONDO (feedback utente 11 lug sera: "caotico, teletrasporti
### bruttissimi, non capisco dove sono le mappe e i luoghi secondari") — PRIORITÀ ALTA
Tutte e 4 le richieste approvate dall'utente:
- MAPPA DEL MONDO (in pausa + dal cartello fast-travel del hub): schema alla
  Super Mario World — nodi = 10 mondi + luoghi segreti SCOPERTI (Konoha, corridoio,
  Sottosopra, paintball, Dreamatorium), "TU SEI QUI" lampeggiante, linee tra i nodi.
  Registro WORLD_MAP data-driven {id, nome, x,y, needs}. SAVE.found[] per i segreti.
- CARTELLI SULLE PORTE: ogni porta X/crepa ψ/armadietto ¾/torii @/porta '8'
  mostra PRIMA dove porta (etichetta sopra quando sei vicino): "→ SCUOLA DI MAGIA",
  "??? (mai visitato)" per i segreti. Riusa il pattern lockers/interact.
- TRANSIZIONI CINEMATICHE: entrata nei luoghi segreti = wipe A PORTALE (nuovo
  wipeKind) + banner grande "BENVENUTO A …" + stinger dedicato. L'uscita idem
  ("DI NUOVO A …"). Il viaggio si deve SENTIRE.
- MINIMAPPA RICCA: marker porte (X, bonus), segreti S scoperti, boss, uscita.
- ESAME: un giocatore NUOVO capisce dove si trova in ogni istante? Ogni porta
  dichiara la destinazione? Il ritorno dal bonus ti ri-ancora (banner)?

### ☐ R9 — VERTICALITÀ E SAGOME (feedback utente: "il mondo sembra piatto…
### non si può andare sotto o sopra"; "nemici e personaggi tutti grandi uguali")
- SOTTOSUOLO/SOPRA nei mondi 1-5 via tools_build_maps.py: ogni mondo guadagna
  UNO strato extra — caverna sotterranea (ingresso-buco + risalita, tesoro/
  segreto dentro) o torre/cime (scalata opzionale con premio). Il main path
  resta; lo strato è OPZIONALE e ricco. Regole 21/23/25 valgono.
- SAGOME: taglie differenziate — mob 'runt' (piccoli ×0.7, veloci) e 'brute'
  (grossi ×1.4, lenti, 3hp) come varianti di scala in drawWalker (scale param);
  i mini-boss +20% di scala. Il colpo d'occhio deve dire CHI è cosa.
- ATTACCO PESANTE (utente: "bruttissimo perché banale"): differenziarlo
  PER ARMA (spada=fendente ampio, martello=onda d'urto a terra, lancia=
  affondo lungo, pugni=combo 2 colpi) — riusa i verbi/fx esistenti.
- ESAME: silhouette leggibili a colpo d'occhio; lo strato extra si trova
  senza guida?; il pesante di 3 armi diverse SI SENTE diverso.

### ☐ R10 — ONBOARDING (feedback utente: "non c'è un'introduzione, non si
### capisce cosa fanno gli oggetti, quali sono gli attacchi, obiettivi poco chiari")
- PRIMA PARTITA GUIDATA: nel mondo 1, i primi 60 secondi insegnano GIOCANDO:
  pannellini contestuali una-tantum al primo uso possibile (▢ quando appare
  il primo nemico, ◯ alla prima minaccia, L1 quando il cd è pronto, R1 alla
  prima barra piena) — riusa/estendi il registro GUIDE (già una-tantum).
- OGGETTI SPIEGATI: primo perk/arma/boon raccolto → card breve "COSA FA"
  (nome+icona+1 riga); da lì in poi solo il toast attuale.
- OBIETTIVO SEMPRE VISIBILE: il lvlBanner scade — aggiungere la riga obiettivo
  in PAUSA e sulla minimappa (icona bersaglio).
- ESAME: un giocatore che NON ha mai visto il gioco capisce i 4 tasti nei
  primi 2 minuti senza leggere tabelle? (test: utente o amico).

## §RESIDUI-EXTRA (non-review, quando capita o su richiesta)
S-GRAFICA mondi 1-6 (texture/sfondi, DOPO R7); jutsu autentici extra (in R5c);
Pain/Sai/Karin/Suigetsu/Jugo da narutoshinrumble (mapper diverso); Deidara
(sheet 73406); **Ron/Hermione/Voldemort — PRIORITÀ ALZATA dall'utente 11 lug
("mancano tutti gli sbloccabili Harry Potter")**: fan-sheet DeviantArt con
immagini PROPOSTE prima, o cattura emulatore dell'utente; Quidditch gravità
ridotta; lezioni mini-stanze; Cornelius nel boss rush; side-quest atto 0
(Annie's Boobs, statua Guzmán, consegne Dean); preset layout pad in Opzioni.
Ordine consigliato post-R4: R8 (bussola: è il dolore #1 dichiarato) → R9 → R10
→ R5 → R6 → R7 (il debito prima di S-GRAFICA resta obbligatorio).

## §COMICITÀ — playbook permanente (Community + British + Scrubs + nonsense)
Ogni testo nuovo passa per UNA lente: 1. META/Abed (callback, regola-Beetlejuice,
gag ricorrenti); 2. BRITISH/Duncan (understatement, morte=pratica burocratica);
3. SCRUBS (nickname descrittivi, NPC ostile); 4. NONSENSE IT/EN (supercazzola,
nomi burocratici per cose epiche, il "colmo"). REGOLE: max 2 righe; nome
leggibile; crudele mai col cast; la battuta non interrompe l'azione.

## VINCOLI NON NEGOZIABILI
1. **Single-file, zero dipendenze runtime**. Gira da file:// e su Pages. Safari.
2. **Sprite Community intoccabili** (cast hawkthorne-journey autentico). Resto:
   libertà, CC0/free ammessi e registrati in CREDITS.md.
3. Testo **italiano**, ironia british/nera; battute fedeli alla serie.
4. Stile 48px, palette scura. Musica SOLO procedurale WebAudio.
5. Commit frequenti + push. Memoria aggiornata a fine sessione.
6. **PS5-first**: menù navigabili da pad (glifi ✕▢◯△), rumble. Difficoltà alla
   Hades: l'inizio accoglie, la profondità punisce.
7. **(nuovo)** Pass del Recensore prima di ogni commit di consegna (§RECENSORE).

## §TOKEN — anti-spreco (obbligatorio)
- MAI rileggere `index.html` intero: `grep -n` con `cut -c1-140` (righe base64
  da 300KB!) + read mirati. Gli ANCHOR nelle sessioni R* sono già pronti: usali.
- Edit chirurgici; contenuti nuovi = righe nei registri, non funzioni ad-hoc.
- Batch di 3-5 modifiche, poi UN giro di test.
- Asset nuovi: script python png→base64→riga HAWK_ASSETS (MAI base64 nel
  contesto) E riga loadImg (regola 14).
- Le decisioni di design nelle R* sono GIÀ PRESE: non ri-discuterle, eseguile.

## §ARCHITETTURA — data-driven
Registri: ENEMIES(+char/evil) · VFX(+blend) · KIT_VFX(fx/sig/proj) · SIG_LIFE ·
ACHIEVEMENTS · QUESTS+engine · ACTS 1-4 · MBOSSES (hopper/swooper/leaper/tigre/
mago + boss2 fasi) · BIOMES+CHUNKS · PERKS · WEAPONS(16) · SYNERGIES · ABILITIES ·
CASE · GUIDE · BOONS · SONGS · LEVELS(10) + PAINT/KONOHA/CANE/SOTTOSOPRA/RUSH_DEF ·
KITS (16 verbi in execVerb) · COMBO_SUPERS · INCUBI · MOUNTS · GUESTS · TILESETS ·
CAOS_W/CAOS_F · STICK/TOUCH_BTNS/TB_C · NETBITS(+up 4096).
Tile speciali: k x S J : * A ! = 9 i I l ¾ 8 7 W Z j ψ ³ @ ¾. Def-flags: hub/boss/
gin/dark/village/campus/dream/paint/remix/gen/bossDepth/exitTo/noExit/rush/spawn.
Debug `_hawk.*`: goto char step tp soul super pow kill dmg mbkill gen remix next
fakeGuest info(+assets/fail) unlock reset ui give gems boon forge arma pom p2...

## §ASSET — fonti e pipeline
1. hawkthorne-journey (autentico, `sleep 1` anti-429): char 12×16 di 48 (walk
   row1 cols1-3, atk row9), acorn bbox alpha, cornelius, lightning.
2. TSR (~180 sheet in assets/guest/src_tsr/, tools_tsr_dl.py/tsr_catalog.py):
   Naruto DS (vs-Sasuke fx_*, NC3/NC4, potn2 evocazioni, shinrumble, dairansen),
   HP GBC bestiario. Gli sheet DS: DUE fondi (esterno variabile + riquadri ciano)
   → key robusto `a<20 OR (r<g-25 AND b<g+50)` in tools_fx_extract.py.
3. OGA CC0 (curl diretto): Weapon Slash ✅, Pixelart Spells ✅ (~20 strip residue
   fire/water/ice/dark/wind/arcane/shield in zip, tinta = RGB×luminanza MAI
   hue su sprite bianchi), Kenney. itch.io: NON scriptabile, chiedere.
4. Pipeline ospiti: tools_guest_extract/build/inline.py (nc_char per NC etichettati
   e non). PIL rotto su arm64 → venv in scratchpad. ROM iso/ SOLO locali (gitignore).
Regole: verifica visiva prima dell'inline; CREDITS.md sempre; se non convince, scarta.

## §REGOLE DI LAVORO (lezioni cumulative 1-33)
1. Animazioni: test frame-per-frame `_hawk.step(1)`; uno screenshot non basta.
2. Nemici/boss nuovi: collauda in 2P; netcode con `fakeGuest()`.
3. Zero errori console; funziona da file:// E su Pages.
4. GitHub raw: `sleep 1` tra file, verifica >5KB.
5. Consegna solo roba TESTATA.
6. rAF sospeso in headless: `_hawk.step`, mai Promise/rAF negli eval.
7. Dopo ogni batch di edit: `node -e "new Function(...)"` su TUTTI gli <script>.
8. `_hawk.tp(x,y?)`; quest/flag persistono in localStorage tra reload.
9. Cicli periodici paralleli = moduli coprimi; overlay si annullano a coppie.
10. Azzera `hitstop` prima di simulare input; il gamepad NON si simula.
11. `p.onGround` OSCILLA da fermi: check a terra = `(onGround || coyote>0)`;
    per l'ARIA usa `airT>1` (mai coyote: declassa il dash a inizio salto).
12. Effetti che bucano uno strato: SEMPRE canvas separato + drawImage.
13. Harness node/browser: testare SOLO via `_hawk.*`; `_hawk.ui()` disegna tutto.
14. **HAWK_ASSETS non basta**: ogni chiave DEVE avere la riga loadImg (il Re
    Ghianda-cubo docet). Verifica `_hawk.info().assets` N/N e ASSET_FAIL.
15. Pannello browser: rAF PUÒ essere throttlato/in pausa → `_hawk.step(1)` in
    loop per bruciare wipeT e animare; il canvas trattiene l'ultimo frame per
    gli screenshot; one-shot (fxShots ~12f) → spawnali e step subito.
16. Tasti tenuti: `keys['X']=true` via KeyboardEvent su window (il listener li
    setta; keys non è esposto). justPressed = dispatch keydown reale.
17. Marker NPC: lettere in 'pbtaHLDGdsr' + buildGroups; agganciati con groundAt.
18. Anelli `parts` ring: spawnare con t:12 (t maggiori = raggio negativo storico).
19. `wipeT` decrementa nel DRAW: test throttlati → draw() in loop o wipeT=0.
20. Combattimento nuovo = riga in KITS (o verbo in execVerb). activateSuper/
    castSpell/ability-'ab' ORFANE: non costruirci sopra (R7 le pota).
21. MAPPE: mai a mano — tools_build_maps.py; dopo rigenerazione ri-arma gli Edit.
22. Collaudo livelli: bot traversata (3 tentativi, stocastico); successo = perk
    o lvlIdx; azzera `boons` tra i run.
23. Muri-cancello fino al SOFFITTO (il walljump scala tutto); porte 3 tile.
24. Sheet rippati: DUE sfondi (esterno + riquadri-cella); segmenti tutti uguali
    = stai tagliando i riquadri; key_trim per-frame; arte GBA guarda a sinistra.
25. Mappe bonus a mano: bordi B + porta X 3-tall via script; salto nei bot =
    justPressed+keys (il taglio del salto castra i vy iniettati).
26. `_hawk.mbkill()` NO-OP con hurtT>0: loop finché dead, verifica lo sblocco.
27. IP senza rip su TSR: fan-repo GitHub (gh api search + trees) — accreditare.
28. ROM Tomy/Griptonite/EA = compressioni custom: sweep dice subito; non insistere.
29. iso/ SOLO locale; mai `git add -A` con roba pesante; bump cache sw.js a release.
30. Sheet fx_* DS: key robusto (v. §ASSET); griglie irregolari → detect_bands/cols,
    verifica a schermo 1 sheet alla volta; strip single-row per il registro VFX.
31. Collaudo VFX: firme al centro player (tp al centro, non dietro l'HUD);
    pow con verbo jail TRASFORMA il player (ricarica pagina tra i test).
32. Bug "già fixato" che torna su iPhone = cache SW, non codice (auto-reload
    da v20.2 in poi; comunque: prima verifica con TouchEvent reali, poi tocca).
33. Test con timing REALISTICO prima di dichiarare un bug (il dash-su NON
    mangia il doppio salto: smentito con entrambi i timing — testare, non dedurre).

## §FINE SESSIONE — rituale (obbligatorio)
1. PASS DEL RECENSORE (§RECENSORE: ≥2 difetti propri trovati, fix o log);
2. verifica §CRITERI; 3. commit+push (`vX.Y: sintesi`); 4. bump GAME_VERSION
+ CACHE sw.js; 5. memoria `hawkthorne-assets` aggiornata; 6. spunta la R* qui
e integra i finding nuovi (questo file È la roadmap: tienilo denso e vero);
7. report: fatto / da provare a mano su Safari / prossima sessione.

## §CRITERI DI ACCETTAZIONE (ogni feature)
Collaudata con `_hawk.step` (2P dove rilevante); zero errori console; ok
file:// e Pages; contenuto nei registri; testi onesti (lente 1 del Recensore);
commit+push; memoria.

## §SPIRITO
Non un porting: una lettera d'amore a Community con ambizioni da gioco vero.
Magie spettacolari, humor nero, meta-narrazione, sorprese. Il Recensore è
severo perché il gioco se lo merita. Cool cool cool.
