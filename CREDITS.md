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

## Musica e suoni
- Interamente procedurali (WebAudio), nessun asset esterno.
