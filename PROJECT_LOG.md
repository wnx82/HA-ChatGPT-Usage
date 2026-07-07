# PROJECT_LOG

## 2026-07-07 14:40 Europe/Brussels - v1.1.0

### Audit initial

- Branche locale initiale : `main`, sans commit.
- Branche distante : aucune branche publiee detectee via `git ls-remote --heads origin`.
- Stack detectee avant modification : depot vide.
- Gestionnaire de paquets : aucun `package-lock.json`, `pnpm-lock.yaml` ou `yarn.lock`.
- Docker : absent.
- Base de donnees : absente.
- Uploads/images/fichiers applicatifs : absents.
- `.env` reels : absents.
- Tests existants : absents.

### Decisions techniques

- Integration Home Assistant custom compatible HACS dans `custom_components/chatgpt_usage`.
- Version initiale projet fixee a `1.1.0`, sans changement de version majeure.
- Usage OpenAI API separe du mode Codex experimental.
- Mode OpenAI implemente avec `DataUpdateCoordinator` et requetes async non bloquantes.
- Mode Codex laisse volontairement experimental et non intrusif : entites indisponibles tant qu'un bridge MQTT fiable n'alimente pas les donnees.
- Les secrets sont stockes dans la config entry Home Assistant et masques par `diagnostics.py`.

### Commandes importantes

- `git ls-remote --heads origin`
- `git pull origin main` : impossible car `origin/main` n'existe pas encore.
- `git checkout -b chore/v1.1.0-initial-hacs-scaffold`
- `python3 -m pytest`
- `python3 -m compileall custom_components tests`

### Limitations connues

- Le bridge MQTT Codex n'est pas encore abonne directement aux topics MQTT ; les entites sont preparees mais restent indisponibles sans implementation d'abonnement.
- Les tests Home Assistant complets necessitent l'environnement de test Home Assistant.

### Rollback

- Branche : `chore/v1.1.0-initial-hacs-scaffold`
- Commande apres merge : `git revert <commit>`

## 2026-07-07 14:40 Europe/Brussels - v1.2.0

### Objectif

- Implementer l'abonnement MQTT reel pour les capteurs Codex experimentaux.

### Criteres d'acceptation

- Chaque capteur Codex s'abonne au topic `prefix/value_key`.
- Les payloads texte, numeriques et JSON avec cle `value` sont supportes.
- Les entites restent indisponibles tant qu'aucune donnee n'est recue.
- Les tests de parsing Codex passent.

### Decisions techniques

- Utilisation de l'integration MQTT native de Home Assistant en `after_dependencies` pour garder le mode OpenAI utilisable sans broker MQTT.
- Conservation du mode experimental et local uniquement pour Codex.
- Parsing MQTT isole dans `codex.py` pour etre testable sans Home Assistant.

### Rollback

- Branche : `feature/v1.2.0-codex-mqtt-bridge`
- Commande apres merge : `git revert <commit>`
