# API

Ce projet n'expose aucune API HTTP locale.

## APIs externes utilisees

Le mode recommande `codex_file` n'appelle aucune API OpenAI et ne demande aucune cle API. Il lit seulement un fichier JSON local produit par le companion web apres connexion manuelle dans ChatGPT.

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

Le companion web local `npm run codex:companion` peut alimenter ce fichier automatiquement apres authentification manuelle dans ChatGPT. Il ouvre la page ChatGPT/Codex dans Chromium et extrait au mieux l'abonnement visible, les credits et les limites d'usage depuis le texte de la page.

Exemple :

```json
{
  "5h_used": 42,
  "5h_remaining_percent": 18,
  "5h_reset": "2026-07-08T15:00:00Z",
  "weekly_used": 310,
  "weekly_remaining_percent": 44,
  "weekly_reset": "2026-07-13T00:00:00Z",
  "plan": "plus",
  "credits": 12.5,
  "limit_status": "available",
  "last_update": "2026-07-08T10:30:00.000Z",
  "source_url": "https://chatgpt.com/codex/cloud/settings/analytics",
  "page_title": "Codex",
  "extraction_status": "ok",
  "missing_fields": []
}
```

Les champs `source_url`, `page_title`, `extraction_status` et `missing_fields` sont informatifs. `extraction_status` vaut `ok`, `partial` ou `empty_page`. Les capteurs Home Assistant utilisent les cles principales ci-dessus.

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

## Limite volontaire

Ce projet ne contourne pas l'authentification ChatGPT et ne lit pas de cookies exportes. Il n'existe pas ici d'appel API officiel documente pour recuperer directement l'abonnement ChatGPT personnel ; le champ `plan` vient donc de la page web visible via le companion.
