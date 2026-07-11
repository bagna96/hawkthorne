# Crediti asset esterni

Tutti gli asset sono incorporati in base64 dentro `index.html` (vincolo single-file).

## Sprite del cast e nemici
- **Project Hawkthorne** (github.com/hawkthorne/hawkthorne-journey) — sprite autentici
  di personaggi, NPC, nemici, boss (acornBoss, cornelius, betafish, icebat...),
  FX firework/sparkle/steam. Licenza del progetto originale (fan-game open source).

## Effetti visivi
- **"Weapon Slash - Effect"** — OpenGameArt.org, licenza **CC0**
  (https://opengameart.org/content/weapon-slash-effect).
  Usati: mezzelune slash (oro/blu/viola), streak, arrow — 6 frame da 126×150,
  strip ricomposte in `fx_slash`, `fx_slash_b`, `fx_slash_p`, `fx_streak`, `fx_arrow`.
  Nel gioco: attacchi corpo a corpo, scatti, incantesimi, super, critici (v12.0).
- **Jutsu autentici (v20.0, §S-VFX)** — ritagliati dagli sheet DS *Naruto Shippuden:
  Naruto vs Sasuke* via The Spriters Resource (fx_double_rasengan #98910 → `fx_rasengan`,
  3 frame 56px; fx_fireball_rasengan #98912 → `fx_katon`, 3 frame 64px). Estrazione con
  chroma-key robusto (fondo verde/teal + riquadri-cella ciano) in `tools_fx_extract.py`.
  Nel gioco: firma del potere di Naruto (rasengan) e del supremo di Sasuke/Troy (Katōn).
  Le altre firme per-kit (chidori, sabbia, vento, rune, insetti, petali, gates, holy) sono
  procedurali (canvas, zero asset), tinte dal colore di ciascun kit.

## Personaggi ospiti e ambientazioni (assets/guest/, INTEGRATI in v15.0)
- **Harry Potter e il Prigioniero di Azkaban (GBA)** e **HP e la Pietra Filosofale (GBA)** —
  sheet rippati via The Spriters Resource (hp_harry, hp_dumbledore, hp_snape, hp_filch,
  creature doxy/gnome/fluffy/tentacula, tileset greathall/hallways/library/potions/commonroom).
- **Naruto RPG: Uketsugareshi Hi no Ishi (GBA)** — sheet battaglia del cast (nrpg_*: naruto,
  sasuke, sakura, kakashi, rocklee, gaara, itachi, orochimaru, zabuza, haku, hinata, jiraiya,
  enemies, battlebg) via The Spriters Resource.
- ⚠ Questi sono **rip da giochi commerciali**: gratuiti da scaricare ma NON liberi di licenza.
  Uso da fan-game personale non commerciale, nello stesso regime del cast Community
  (Project Hawkthorne). Nessuna rivendicazione di proprietà.
- In gioco (v15.0): giocabili Harry/Naruto/Sasuke/Rock Lee/Kakashi (strip g_* ricomposte
  da tools_guest_build.py, chroma-key doppio passaggio), nemici doxy/gnomo/tentacula/
  ninja/tigre/corvo, mini-boss Fuffi e Zabuza, NPC Piton/Gazza/Silente, sfondo dipinto
  di Konoha (nrpg_nar_battlebg, cella singola) per il mondo bonus.

## Stranger Things (v16.0, fan-sprite da repository GitHub pubblici)
- **Sunairaa/StrangerThingsGame** (GitHub) — sprite fan di Undici (posa telecinetica),
  demodog e demogorgone grande. → `st_eleven`, `st_demodog`, `st_demogorgon`.
- **Gonzalo6282/Stranger_Things_Game** (GitHub) — ciclo camminata di Hopper (6 frame,
  con morte "cappello che rotola") e demogorgone grigio animato. → `st_hopper`, `st_demogrey`.
- **elen-c-sales/dino-run-vecna-edition** (GitHub) — corsa di Vecna (4 frame), demobat
  (4 frame) e sfondi a strati del Sottosopra. → `st_vecna`, `st_demobat`, `st_upside_far/near`.
- ⚠ Opere di fan senza licenza esplicita, su IP Netflix: stesso regime fan-game non
  commerciale del resto del progetto. Nessuna rivendicazione; credito agli autori dei repo.

## S-GRAFICA (v16.0)
- Atlante `g_hogtiles` (muro in mattoni + pavimento a rombi ×2) ritagliato da
  `hp_hallways` (rip GBA già accreditato sopra): tile texturizzate di Scuola e Corridoio.

## Musica e suoni
- Interamente procedurali (WebAudio), nessun asset esterno.
