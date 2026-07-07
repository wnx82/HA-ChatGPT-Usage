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

