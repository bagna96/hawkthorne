# PROMPT PER LA PROSSIMA SESSIONE — Hawkthorne v9 "Masterpiece"

> Incolla questo prompt (o indicalo) a Claude Code in una nuova sessione.
> Contiene tutto il contesto, le regole di lavoro e la roadmap completa.

## CONTESTO — cosa esiste già

Sei nel progetto `~/hawkthorne`: un platformer 8-bit tributo a **Community S3E20
"Digital Estate Planning"**, giocabile online su **https://bagna96.github.io/hawkthorne/**
(repo `bagna96/hawkthorne`, GitHub Pages, branch main). Leggi la memoria
`hawkthorne-assets` e `fan-content-fidelity` prima di toccare qualsiasi cosa.

Stato v8.1:
- `index.html` = gioco COMPLETO in un file solo (asset base64 inline, ~1.2MB).
  `assets.js` è la copia esterna degli asset; lo script python per rigenerarla
  e re-inlinarla è documentato sotto ("PIPELINE ASSET").
- 20 personaggi giocabili (sprite autentici di Project Hawkthorne), costumi,
  super-poteri a barra Meraviglia, tratti passivi, boons del negozio,
  scivolata/schianto, 7 mondi (hub, radura, foresta+Re Ghianda, villaggio,
  lago di gin, caverne+Gilbert, trono+Cornelius vero), co-op locale 2P,
  co-op ONLINE WebRTC P2P (scambio manuale di 2 codici), gamepad PS5+rumble,
  musica procedurale con batteria, salvataggio localStorage (`hawk_save`).
- Debug console: `_hawk.goto(n) .step(n) .tp(x) .soul() .super() .kill() .dmg(n)
  .beatRival() .p2() .give(n) .gems(n) .boon(id) .forge() .incubo() .next()
  .fakeGuest() .reset() .info()`.

## REGOLE DI LAVORO (dall'esperienza con l'utente — NON violarle)

1. **Testa le ANIMAZIONI frame-per-frame** con `_hawk.step(1)` + screenshot
   consecutivi: uno screenshot singolo NON rivela sfarfallii. Il bug "strobo
   idle/salto" è stato visto dall'utente, non dai test. Se serve, chiedi un
   video breve ma **analizzalo in max 2 tentativi**: se la diagnosi non
   converge subito, dillo e passa a fix robusti per classe di problema.
2. L'utente usa **Safari** e apre il gioco anche con **doppio click**: mai
   reintrodurre dipendenze esterne runtime (font, CDN, fetch). Tutto inline.
3. **Personaggi principali intoccabili** (sprite autentici); su mondi, nemici,
   NPC extra e meccaniche hai libertà totale. All'utente piacciono **magie e
   poteri spettacolari**. Non trattenerti, ma consegna sempre roba TESTATA.
4. Tutto il testo di gioco in **italiano**, con ironia/humor nero/british
   (Duncan). Fedeltà alle battute della serie dove esistono.
5. Commit frequenti con messaggi chiari; push subito (Pages si aggiorna da solo;
   `http.postBuffer` già configurato). Aggiorna la memoria a fine sessione.
6. GitHub API raw ha rate-limit: scarica con `sleep 1` tra i file e verifica
   la dimensione (>5KB) di ogni png scaricato.

## PIPELINE ASSET (già rodata)

1. Scarica png da `https://raw.githubusercontent.com/hawkthorne/hawkthorne-journey/master/src/images/...`
   in `assets/{characters,npc,enemies}/`.
2. Rigenera e re-inline: lo script è in cronologia git (commit v7/v8) — genera
   `assets.js` da tutte le cartelle e sostituisce il blocco
   `<script>window.HAWK_ASSETS=...</script>` dentro `index.html`.
3. Nel codice: `loadImg(chiave, percorso)` + disegno con crop espliciti.
   Layout noti: personaggi 12×16 frame 48×48 (mappa `ANIM`, riga destra,
   sinistra = riga−1); hilda 32×48; babyabed 20×25; acorn 44×40 (5 col);
   hippy 48×48 (6×2); bat 30×22 (5 col); cornelius boss 200×220 (3×5);
   acornBoss 75×75 (8×7); cornelius_lightning 144×192 (3 col).

## ROADMAP v9 — in ordine di priorità

### A. Solidità (fai prima questo)
1. **Verifica del fix strobo** con l'utente sulla URL Pages; se persiste,
   registra p.anim/p.onGround per 120 frame via `_hawk` e correggi alla fonte.
2. **Netcode robusto**: heartbeat + timeout; riconnessione con nuovo scambio
   codici senza ricaricare; interpolazione posizioni sull'ospite (lerp tra
   ultimi 2 snapshot); compressione snapshot (delta o campi abbreviati);
   pulsante "COPIA CODICE" (navigator.clipboard) al posto dei prompt().
3. **Touch controls iPhone/iPad**: overlay croce+3 bottoni su pointer events,
   `manifest.json` PWA + service worker per giocare offline dall'icona home.

### B. Mondi e boss (espansione grande)
4. **Un mini-boss per ogni mondo** (sheet nel repo `src/images/enemies/`):
   - Lago di Gin: **betafish.png** gigante che salta fuori dal gin
   - Caverne: **icebat.png** regina dei pipistrelli (sciami)
   - Villaggio: **turkey.png** o "il Fabbro fantasma" (vendetta di Annie&Shirley)
   - Radura: opzionale, jumpingacorn come mid-boss veloce
5. **Mondo nuovo: GREENDALE** — corridoi del campus (tileset/idee da
   `src/images/greendale*` nel repo se esiste, altrimenti procedurale: armadietti,
   bacheca, mensa). NPC: il Dean con 3 costumi che dà una quest, Chang boss
   ("EL TIGRE") con fulmini propri, Leonard che ruba monete.
6. **Livello segreto PAINTBALL**: ingresso nascosto a Greendale; tutto il
   livello ricolorato a schizzi, nemici = studenti col paintball
   (usa i costumi `paintball` già scaricati), arma temporanea pistola-vernice.
7. **Nuoto nel Lago di Gin**: la mappa ufficiale ha anim `swim`/`swimwalk` —
   trasforma il gin da hazard a zona nuotabile (con "ubriachezza": controlli
   invertiti dopo 5s, molto Community).

### C. Personaggi e poteri
8. **Super combinati co-op** (quando entrambi al 100%: premendo super insieme):
   Troy+Abed = "TROY E ABED SPARANO LAVA" (doppio raggio); qualsiasi coppia =
   "ABBRACCIO DI GRUPPO" (cura totale + stun globale). Fai matrice semplice.
9. **Livelli dei super**: ogni 5 usi il super sale di grado (I→III, più danno/
   durata); persistito in `hawk_save`.
10. **Boss rush** dal titolo (sblocco post-game) + **speedrun timer** con
    migliori tempi salvati; **modalità Incubo** con modificatori a scelta
    (stile Hades: +velocità nemici, -cuori, monete ×3).
11. **Achievement** con toast e pagina dedicata (tasto A al titolo):
    "Streets Ahead" (finisci senza morire), "Sei stagioni e un film"
    (100% sbloccato), "Zitto, Leonard" (sconfiggi 50 hippy), ecc.

### D. Arte e audio
12. **Parallax multilivello** (2-3 piani per mondo) + **meteo**: foglie nella
    foresta, cenere nel villaggio in fiamme, gocce di gin, neve segreta.
13. **Transizioni a cerchio** retro tra livelli; title screen animato con i
    beam di teletrasporto che depositano il cast uno a uno.
14. **Musica per mondo** (ogni mondo il suo brano con 3 voci + batteria) e
    stinger per: super, mini-boss, vittoria. Resta procedurale WebAudio.
15. Pacchetti CC0 esterni ammessi per VFX magici (l'utente li vuole): cerca
    "pixel spell effects CC0" (es. pimen su itch) — MA scarica solo ciò che
    riesci a verificare visivamente e integra nello stile (48px, palette scura).

### E. Extra da valutare col tempo rimasto
16. Slot di salvataggio multipli + export/import del save (stringa base64).
17. Statua di Luis Guzmán easter egg (repo: `guzman`), Annie's Boobs quest
    (riporta 5 oggetti rubati sparsi nei mondi).
18. Selettore livello dal hub (portali multipli invece di progressione lineare)
    dopo il primo completamento.
19. Daily seed: casse e cristalli rimescolati con seed del giorno, condivisibile.

## CRITERI DI ACCETTAZIONE (per ogni feature)
- Collaudata con `_hawk.step` (inclusi 2P e, per il netcode, `fakeGuest()`);
- zero errori console; funziona da file:// e su Pages;
- commit + push; nota in memoria se introduce API/layout nuovi.
