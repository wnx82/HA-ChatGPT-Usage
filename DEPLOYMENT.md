# DEPLOYMENT

## Environnements

- Local : instance Home Assistant de developpement.
- Staging : instance Home Assistant de test, recommandee avant production.
- Production : instance Home Assistant principale.

## Installation locale

Copier `custom_components/chatgpt_usage` dans le dossier `config/custom_components/chatgpt_usage` de Home Assistant puis redemarrer Home Assistant.

## Variables et secrets

- Mode recommande sans cle API : `codex_file` avec fichier JSON local produit par le companion web.
- Cle API OpenAI admin : configuree via l'interface Home Assistant seulement si le mode `openai` ou `both` est utilise.
- Organisation/projet : optionnels via config flow/options flow.
- MQTT Codex : prefixe `codex/usage` par defaut.
- Broker MQTT Home Assistant requis pour le mode Codex MQTT Bridge.
- Profil navigateur du companion : `.codex-web-companion/profile`, local et ignore par Git.

## Ports

L'integration n'ouvre aucun port. Elle utilise les connexions sortantes Home Assistant vers OpenAI seulement en mode API. En mode `codex_file`, Home Assistant lit un fichier local. Le companion web utilise une connexion sortante vers ChatGPT depuis la machine ou il est lance.

## Docker

Aucun `Dockerfile` ou `docker-compose.yml` n'est fourni par ce projet. Si Home Assistant tourne avec Docker, monter le dossier `custom_components` dans le volume persistant Home Assistant.

## Build et demarrage

Aucun build frontend n'est necessaire.

Pour initialiser le companion web :

```bash
npm install
npx playwright install chromium
```

Pour produire le fichier Codex :

```bash
npm run codex:companion -- --out /config/chatgpt_usage_codex.json
```

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
- En mode `codex_file`, les capteurs `sensor.chatgpt_codex_*` se creent apres lecture du fichier JSON.
- En mode API, les capteurs OpenAI se creent et `binary_sensor.chatgpt_usage_api_status` est disponible.
- Les diagnostics ne contiennent pas de secret.
- Les capteurs Codex restent indisponibles si aucun fichier JSON ou bridge MQTT ne fournit les valeurs attendues.
