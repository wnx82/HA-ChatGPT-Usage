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
