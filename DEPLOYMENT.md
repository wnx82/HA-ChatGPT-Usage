# DEPLOYMENT

## Environnements

- Local : instance Home Assistant de developpement.
- Staging : instance Home Assistant de test, recommandee avant production.
- Production : instance Home Assistant principale.

## Installation locale

Copier `custom_components/chatgpt_usage` dans le dossier `config/custom_components/chatgpt_usage` de Home Assistant puis redemarrer Home Assistant.

## Variables et secrets

- Cle API OpenAI admin : configuree via l'interface Home Assistant.
- Organisation/projet : optionnels via config flow/options flow.
- MQTT Codex : prefixe `codex/usage` par defaut.

## Ports

L'integration n'ouvre aucun port. Elle utilise les connexions sortantes Home Assistant vers OpenAI et, a terme, les messages MQTT locaux.

## Docker

Aucun `Dockerfile` ou `docker-compose.yml` n'est fourni par ce projet. Si Home Assistant tourne avec Docker, monter le dossier `custom_components` dans le volume persistant Home Assistant.

## Build et demarrage

Aucun build frontend n'est necessaire.

## Rollback

1. Desactiver l'integration dans Home Assistant.
2. Revenir au commit precedent :

```bash
git revert <commit>
```

3. Recopier le dossier `custom_components/chatgpt_usage`.
4. Redemarrer Home Assistant.

## Verification apres deploiement

- L'integration apparait dans Appareils et services.
- Les capteurs OpenAI se creent.
- `binary_sensor.chatgpt_usage_api_status` est disponible.
- Les diagnostics ne contiennent pas de secret.
- Les capteurs Codex restent indisponibles si aucun bridge MQTT n'est present.

