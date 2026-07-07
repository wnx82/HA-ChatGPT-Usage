# PROJECT_LOG

## 2026-07-07 15:05 Europe/Brussels - v1.3.0

### Objectif

- Ajouter une source Codex locale sans MQTT via un fichier JSON pollé par Home Assistant.

### Criteres d'acceptation

- Un utilisateur peut configurer Codex sans broker MQTT.
- Les capteurs Codex lisent un fichier JSON local selon `scan_interval`.
- Le mode MQTT existant reste fonctionnel.

### Decisions techniques

- Ajout d'une source Codex `file` configurable dans le config flow.
- Lecture du fichier via un `DataUpdateCoordinator` dedie pour rester coherente avec le reste de l'integration.
- Pas d'authentification web automatisee dans Home Assistant ; le fichier local reste une frontiere claire et maintenable.

### Rollback

- Branche : `feature/v1.3.0-codex-local-file`
- Commande apres merge : `git revert <commit>`

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

## 2026-07-07 14:40 Europe/Brussels - v1.2.1

### Objectif

- Eviter qu'un broker MQTT absent ou non configure casse les capteurs Codex experimentaux.

### Decisions techniques

- Attraper les erreurs d'abonnement MQTT au niveau de chaque capteur Codex.
- Exposer un statut `mqtt_unavailable` dans les attributs au lieu d'echouer silencieusement ou de casser le setup.
- Convertir les timestamps ISO en objets `datetime` pour respecter le `SensorDeviceClass.TIMESTAMP`.

### Rollback

- Branche : `fix/v1.2.1-codex-mqtt-unavailable`
- Commande apres merge : `git revert <commit>`

## 2026-07-07 14:40 Europe/Brussels - v1.2.2

### Objectif

- Finaliser les notes de release apres les merges et tags reels.

### Decisions techniques

- Garder une etape documentaire dediee pour ne pas modifier l'historique deja tague.
- Incrementation patch `z` uniquement, sans changement de version majeure ni mineure.

### Rollback

- Branche : `docs/v1.2.2-finalize-release-notes`
- Commande apres merge : `git revert <commit>`
