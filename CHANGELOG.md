# CHANGELOG

## Regle de versioning

Le projet utilise toujours une version au format `x.y.z`.

- `x` = version majeure decidee uniquement par l'utilisateur.
- `y` = nouvelle branche ou nouvelle grande etape.
- `z` = modification, correction ou ajustement dans l'etape.
- `y` peut depasser `10`.
- `z` peut depasser `10`.
- Ne jamais transformer automatiquement `1.9.12` en `2.0.0`.
- Seul l'utilisateur peut decider de passer de `1.x.x` a `2.0.0`.

Exemples valides : `1.1.0`, `1.2.0`, `1.2.1`, `1.9.12`, `1.10.0`, `1.14.27`.

Quand la version change, mettre a jour tous les fichiers qui portent la version projet : `package.json` si present, `README.md` si une version y est indiquee, `CHANGELOG.md`, `pyproject.toml`, `custom_components/chatgpt_usage/manifest.json`, `custom_components/chatgpt_usage/const.py`, `package-lock.json` si present, et tout autre fichier de configuration contenant une version projet.

## [1.5.2] - 2026-07-08 Europe/Brussels

### Changements
- Ajout d'une premiere etape de config flow pour lier ChatGPT/Codex avant les reglages.
- Ajout d'un lien vers la page ChatGPT/Codex Usage Dashboard dans l'assistant Home Assistant.
- Ajout d'une confirmation utilisateur avant de continuer vers la configuration `codex_file`.
- Mise a jour des traductions et de la documentation d'installation.

### Limite
- Home Assistant ne peut pas ouvrir automatiquement un navigateur Chromium local ni recuperer les cookies ChatGPT depuis l'integration. La liaison reste une etape guidee : l'utilisateur ouvre la page ChatGPT/Codex et lance le companion web local.

### Tests
- `python3 -m pytest` : OK, 8 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm test` : OK, 7 tests passes.
- Validation JSON des fichiers `strings.json`, traductions, `manifest.json`, `package.json` et `package-lock.json` : OK.

## [1.5.1] - 2026-07-08 Europe/Brussels

### Changements
- Ajout de la regle de versioning projet dans le changelog.
- Rappel que seul l'utilisateur peut decider d'une version majeure.
- Alignement des fichiers de version projet en `1.5.1`.

### Tests
- Changement documentaire et metadata uniquement.

## [1.5.0] - 2026-07-08 Europe/Brussels

### Changements
- Passage du mode initial par defaut a `codex_file` pour permettre une installation sans cle API.
- Clarification de la separation entre abonnement ChatGPT/Codex via companion web et usage OpenAI API via cle admin optionnelle.
- Renforcement du parser du companion web pour detecter les libelles d'abonnement `subscription`, `abonnement`, `forfait` et `ChatGPT Plus/Pro/Go/etc.`.
- Ajout de la prise en charge de libelles francais courants pour l'usage, les credits, les resets et le statut de limite.
- Ajout de `missing_fields` et du statut `partial` pour diagnostiquer les captures incompletes.
- Correction de la conservation des valeurs `0%` dans les progress bars.
- Correction du fallback de reset pour eviter de melanger les fenetres 5h et hebdo.
- Mise a jour des documents README, API, securite, deploiement et TODO.

### Tests
- `python3 -m pytest` : OK, 8 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm test` : OK, 7 tests passes.

## [1.4.0] - 2026-07-07 16:45 Europe/Brussels

### Branche
feature/v1.4.0-codex-web-companion

### Changements
- Ajout d'un companion web local base sur Playwright pour ouvrir ChatGPT et alimenter le fichier Codex JSON.
- Ajout d'un parser Node teste pour extraire au mieux les limites 5h, hebdo, credits et plan depuis la page d'usage Codex.
- Mise a jour de la documentation et des regles de securite pour le profil navigateur local.

### Fichiers modifies
- `package.json`
- `scripts/codex-web-companion.mjs`
- `scripts/codex-page-parser.mjs`
- `scripts/codex-page-parser.test.mjs`
- `.gitignore`
- `README.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `PROJECT_LOG.md`
- `TODO.md`

### Tests
- `python3 -m pytest` : OK, 8 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm test` : OK, 2 tests passes.
- `npx playwright install chromium` : OK.

### Merge
- Branche a merger dans `main` apres validation du commit.

### Notes
- Le companion ouvre un navigateur local et laisse l'authentification a l'utilisateur.

## [1.3.0] - 2026-07-07 15:05 Europe/Brussels

### Branche
feature/v1.3.0-codex-local-file

### Changements
- Ajout d'un mode Codex local sans MQTT via un fichier JSON pollé.
- Ajout d'une source Codex configurable : `file` ou `mqtt`.
- Mise a jour de la configuration et de la documentation pour le mode fichier.

### Fichiers modifies
- `custom_components/chatgpt_usage/const.py`
- `custom_components/chatgpt_usage/config_flow.py`
- `custom_components/chatgpt_usage/coordinator.py`
- `custom_components/chatgpt_usage/sensor.py`
- `custom_components/chatgpt_usage/codex.py`
- `README.md`
- `API.md`
- `CHANGELOG.md`
- `PROJECT_LOG.md`
- `TODO.md`

### Tests
- `python3 -m pytest` : OK, 8 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm run lint` : non disponible, aucun `package.json`.
- `npm run build` : non disponible, aucun `package.json`.

### Merge
- Branche a merger dans `main` apres validation du commit.

### Notes
- Le mode MQTT existant est conserve.

## [1.2.2] - 2026-07-07 14:40 Europe/Brussels

### Branche
docs/v1.2.2-finalize-release-notes

### Changements
- Finalisation des notes de release apres merges reels dans `main`.
- Mise a jour de la version documentaire/projet en `1.2.2`.
- Clarification du statut final des branches, tags et tests.

### Fichiers modifies
- `CHANGELOG.md`
- `PROJECT_LOG.md`
- `TODO.md`
- `README.md`
- `custom_components/chatgpt_usage/manifest.json`
- `custom_components/chatgpt_usage/const.py`
- `pyproject.toml`

### Tests
- `python3 -m pytest` : OK, 7 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm run lint` : non disponible, aucun `package.json`.
- `npm run build` : non disponible, aucun `package.json`.

### Merge
- Branche a merger dans `main` apres validation du commit.

### Notes
- Etape documentaire uniquement.

## [1.2.1] - 2026-07-07 14:40 Europe/Brussels

### Branche
fix/v1.2.1-codex-mqtt-unavailable

### Changements
- Robustesse du mode Codex MQTT quand MQTT est absent ou non configure.
- Conversion des timestamps Codex ISO en `datetime` compatible Home Assistant.
- Passage de la version projet a `1.2.1`.

### Fichiers modifies
- `custom_components/chatgpt_usage/codex.py`
- `custom_components/chatgpt_usage/sensor.py`
- `custom_components/chatgpt_usage/manifest.json`
- `tests/test_codex_parsing.py`
- `README.md`
- `PROJECT_LOG.md`
- `TODO.md`
- `CHANGELOG.md`

### Tests
- `python3 -m pytest` : OK, 7 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm run lint` : non disponible, aucun `package.json`.
- `npm run build` : non disponible, aucun `package.json`.

### Merge
- Branche mergee dans `main` avec succes.
- Tag `v1.2.1` cree et pousse.

### Notes
- Aucun secret reel ajoute.

## [1.2.0] - 2026-07-07 14:40 Europe/Brussels

### Branche
feature/v1.2.0-codex-mqtt-bridge

### Changements
- Ajout de l'abonnement MQTT reel pour les capteurs Codex experimentaux.
- Ajout du parsing de payloads Codex texte, numeriques et JSON avec cle `value`.
- Mise a jour de la documentation des topics MQTT Codex.
- Passage de la version projet a `1.2.0`.

### Fichiers modifies
- `custom_components/chatgpt_usage/codex.py`
- `custom_components/chatgpt_usage/sensor.py`
- `custom_components/chatgpt_usage/manifest.json`
- `tests/test_codex_parsing.py`
- `README.md`
- `API.md`
- `DEPLOYMENT.md`
- `PROJECT_LOG.md`
- `TODO.md`
- `CHANGELOG.md`

### Tests
- `python3 -m pytest` : OK, 6 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `npm run lint` : non disponible, aucun `package.json`.
- `npm run build` : non disponible, aucun `package.json`.

### Merge
- Branche mergee dans `main` avec succes.
- Tag `v1.2.0` cree et pousse.

### Notes
- `git pull origin main` impossible avant branche : `origin/main` n'existe pas encore.
- Aucun secret reel ajoute.

## [1.1.0] - 2026-07-07 14:40 Europe/Brussels

### Branche
chore/v1.1.0-initial-hacs-scaffold

### Changements
- Initialisation de l'integration Home Assistant custom `chatgpt_usage`.
- Ajout du manifeste HACS/Home Assistant, config flow, coordinator, capteurs et diagnostics.
- Ajout du client async OpenAI Usage officiel.
- Ajout des capteurs Codex experimentaux en attente d'un bridge MQTT.
- Ajout de la documentation projet et des tests unitaires de parsing/masquage.

### Fichiers modifies
- `custom_components/chatgpt_usage/*`
- `tests/*`
- `README.md`
- `SECURITY.md`
- `DEPLOYMENT.md`
- `API.md`
- `PROJECT_LOG.md`
- `TODO.md`
- `.env.example`

### Tests
- `python3 -m pytest` : OK, 3 tests passes.
- `python3 -m compileall custom_components tests` : OK.
- `pytest` : commande directe non disponible dans le shell.
- `npm run lint` : non disponible, aucun `package.json`.
- `npm run build` : non disponible, aucun `package.json`.

### Merge
- Branche integree comme premier commit de `main` avec succes.
- Tag `v1.1.0` cree et pousse.

### Notes
- Depot distant sans branche `main` au demarrage.
- Aucun secret reel ajoute.
- `python` direct non disponible ; `python3` utilise.
