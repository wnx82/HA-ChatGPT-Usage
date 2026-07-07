# API

Ce projet n'expose aucune API HTTP locale.

## APIs externes utilisees

### OpenAI Organization Costs

- Methode : `GET`
- URL : `https://api.openai.com/v1/organization/costs`
- Authentification : `Authorization: Bearer <OPENAI_ADMIN_API_KEY>`
- Parametres : `start_time`, `end_time`, `bucket_width`
- Usage : couts OpenAI API par periode.

### OpenAI Organization Usage Completions

- Methode : `GET`
- URL : `https://api.openai.com/v1/organization/usage/completions`
- Authentification : `Authorization: Bearer <OPENAI_ADMIN_API_KEY>`
- Parametres : `start_time`, `end_time`, `bucket_width`, `group_by`
- Usage : requetes et tokens par periode, modele et projet si disponible.

## Fichier local Codex experimental

Le mode Codex experimental peut lire un fichier JSON local, par defaut :

- `/config/chatgpt_usage_codex.json`

Cles attendues :

- `5h_used`
- `5h_remaining_percent`
- `5h_reset`
- `weekly_used`
- `weekly_remaining_percent`
- `weekly_reset`
- `plan`
- `credits`
- `limit_status`
- `last_update`

Le companion web local `npm run codex:companion` peut alimenter ce fichier automatiquement apres authentification manuelle dans ChatGPT.

## MQTT Codex experimental

Le mode Codex experimental attend un bridge local externe. Prefixe par defaut : `codex/usage`.

Topics cibles recommandes :

- `codex/usage/5h_used`
- `codex/usage/5h_remaining_percent`
- `codex/usage/5h_reset`
- `codex/usage/weekly_used`
- `codex/usage/weekly_remaining_percent`
- `codex/usage/weekly_reset`
- `codex/usage/plan`
- `codex/usage/credits`
- `codex/usage/limit_status`
- `codex/usage/last_update`

Payloads acceptes :

- valeur brute : `42`, `18.5`, `plus`, `limited`
- JSON avec cle `value` : `{"value": 18.5}`
