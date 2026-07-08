# TODO

## A faire
- [ ] Ajouter des tests Home Assistant complets du config flow avec `pytest-homeassistant-custom-component`.
- [ ] Valider les schemas exacts des endpoints OpenAI Usage contre des reponses reelles anonymisees.

## En cours
- [ ] Aucune tache en cours apres validation de `1.5.0`.

## Termine
- [x] Initialiser la structure HACS/Home Assistant. Version : `1.1.0`, branche : `chore/v1.1.0-initial-hacs-scaffold`.
- [x] Implementer l'abonnement MQTT Codex reel via l'integration MQTT Home Assistant. Version : `1.2.0`, branche : `feature/v1.2.0-codex-mqtt-bridge`.
- [x] Rendre le mode Codex robuste si MQTT est absent ou non configure. Version : `1.2.1`, branche : `fix/v1.2.1-codex-mqtt-unavailable`.
- [x] Finaliser les notes de release apres merges. Version : `1.2.2`, branche : `docs/v1.2.2-finalize-release-notes`.
- [x] Ajouter un mode Codex local par fichier JSON sans MQTT. Version : `1.3.0`, branche : `feature/v1.3.0-codex-local-file`.
- [x] Ajouter un companion web local pour alimenter le fichier Codex sans MQTT. Version : `1.4.0`, branche : `feature/v1.4.0-codex-web-companion`.
- [x] Passer le mode sans cle API en configuration par defaut et renforcer la recuperation de l'abonnement ChatGPT/Codex. Version : `1.5.0`.

## Bugs connus
- [ ] Aucun bug runtime confirme pour l'instant ; tests Home Assistant complets encore a ajouter.

## Ameliorations possibles
- [ ] Rendre l'extraction du companion web plus robuste face aux changements d'interface ChatGPT.
  - Contexte : le parsing actuel repose sur le texte visible, les libelles d'abonnement et les progress bars.
  - Priorite : haute.
  - Detecte pendant : `feature/v1.4.0-codex-web-companion`, renforce en `1.5.0`.
- [ ] Ajouter des tests d'entites MQTT avec Home Assistant et un broker simule.
  - Contexte : le parsing est teste, mais l'abonnement Home Assistant complet depend de l'environnement HA.
  - Priorite : haute.
  - Detecte pendant : `feature/v1.2.0-codex-mqtt-bridge`.
- [ ] Ajouter une carte dashboard packagee ou un blueprint Lovelace.
  - Contexte : faciliter l'installation pour les utilisateurs Home Assistant.
  - Priorite : moyenne.
  - Detecte pendant : `chore/v1.1.0-initial-hacs-scaffold`.
- [ ] Ajouter un blueprint d'automatisation Home Assistant.
  - Contexte : reutiliser les alertes cout/Codex sans copier du YAML.
  - Priorite : moyenne.
  - Detecte pendant : `chore/v1.1.0-initial-hacs-scaffold`.

## Idees futures
- [ ] Ajouter un companion `codex-ha-bridge` separe pour publier les topics MQTT attendus.

## Dette technique
- [ ] Ajouter des tests Home Assistant du setup complet `codex_file`.
  - Raison : le parsing est couvert, mais le cycle config entry/coordinator/entity depend encore d'un environnement Home Assistant complet.
