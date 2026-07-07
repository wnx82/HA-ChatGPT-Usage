# CHANGELOG

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
- Branche a merger dans `main` apres validation du commit.

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
- Branche a merger dans `main` apres validation du commit.

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
- Branche a merger dans `main` apres validation du commit.

### Notes
- Depot distant sans branche `main` au demarrage.
- Aucun secret reel ajoute.
- `python` direct non disponible ; `python3` utilise.
