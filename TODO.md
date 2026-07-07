# TODO

## A faire
- [ ] Implementer l'abonnement MQTT Codex reel via l'integration MQTT Home Assistant.
- [ ] Ajouter des tests Home Assistant complets du config flow avec `pytest-homeassistant-custom-component`.
- [ ] Valider les schemas exacts des endpoints OpenAI Usage contre des reponses reelles anonymisees.

## En cours
- [ ] Aucune tache en cours apres validation de `1.1.0`.

## Termine
- [x] Initialiser la structure HACS/Home Assistant. Version : `1.1.0`, branche : `chore/v1.1.0-initial-hacs-scaffold`.

## Bugs connus
- [ ] Aucun bug runtime confirme pour l'instant ; tests Home Assistant complets encore a ajouter.

## Ameliorations possibles
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
- [ ] Remplacer les capteurs Codex placeholder par des entites mises a jour depuis MQTT.
  - Raison : eviter de coupler l'integration officielle OpenAI a une source Codex non standardisee.
