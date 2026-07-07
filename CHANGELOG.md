# CHANGELOG

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
