# ChatGPT Usage

Version actuelle : `1.2.1`

ChatGPT Usage est une integration Home Assistant custom compatible HACS pour afficher l'usage OpenAI API officiel et des informations Codex experimentales via un bridge MQTT local.

## Stack technique

- Home Assistant custom integration
- Python async
- `DataUpdateCoordinator`
- `ConfigFlow` et `OptionsFlow`
- `aiohttp` via Home Assistant
- HACS

## Fonctionnalites

- Cout OpenAI API du jour, d'hier, du mois courant et des 7 derniers jours.
- Requetes et tokens input/output du jour si disponibles via les endpoints OpenAI.
- Statut de connectivite API.
- Capteurs Codex experimentaux alimentes par un bridge MQTT local.
- Diagnostics Home Assistant avec masquage des secrets.

## Installation

1. Copier le dossier `custom_components/chatgpt_usage` dans `config/custom_components/chatgpt_usage`.
2. Redemarrer Home Assistant.
3. Ajouter l'integration depuis l'interface : Parametres > Appareils et services > Ajouter une integration > ChatGPT Usage.

## Configuration

Parametres principaux :

- `OpenAI Admin API key` : cle API admin OpenAI pour les endpoints organisationnels.
- `Organization ID` : optionnel.
- `Project ID` : optionnel.
- `Currency` : `USD` par defaut.
- `Scan interval` : `3600` secondes par defaut, minimum `300`.
- `Codex MQTT prefix` : `codex/usage` par defaut.

Le mode Codex est experimental. Il ne demande jamais de mot de passe ChatGPT et ne stocke aucun cookie ou token de session ChatGPT.

## Topics MQTT Codex

Prefixe par defaut : `codex/usage`.

L'integration s'abonne aux topics suivants :

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

Chaque payload peut etre une valeur brute (`42`, `18.5`, `plus`) ou un objet JSON contenant une cle `value`, par exemple :

```json
{"value": 18.5, "updated_at": "2026-07-07T12:00:00Z"}
```

## Variables d'environnement

Voir `.env.example`. Les secrets reels ne sont pas requis dans le depot pour Home Assistant, car la cle API est stockee dans la config entry Home Assistant.

## Entites

OpenAI API :

- `sensor.chatgpt_usage_cost_today`
- `sensor.chatgpt_usage_cost_yesterday`
- `sensor.chatgpt_usage_cost_current_month`
- `sensor.chatgpt_usage_cost_last_7_days`
- `sensor.chatgpt_usage_requests_today`
- `sensor.chatgpt_usage_input_tokens_today`
- `sensor.chatgpt_usage_output_tokens_today`
- `sensor.chatgpt_usage_total_tokens_today`
- `sensor.chatgpt_usage_last_update`
- `binary_sensor.chatgpt_usage_api_status`

Codex experimental :

- `sensor.chatgpt_codex_5h_used`
- `sensor.chatgpt_codex_5h_remaining_percent`
- `sensor.chatgpt_codex_5h_reset`
- `sensor.chatgpt_codex_weekly_used`
- `sensor.chatgpt_codex_weekly_remaining_percent`
- `sensor.chatgpt_codex_weekly_reset`
- `sensor.chatgpt_codex_plan`
- `sensor.chatgpt_codex_credits`
- `sensor.chatgpt_codex_limit_status`
- `sensor.chatgpt_codex_last_update`

## Exemple Lovelace

```yaml
type: vertical-stack
cards:
  - type: entities
    title: ChatGPT Usage
    entities:
      - entity: sensor.chatgpt_usage_cost_today
        name: Cout aujourd'hui
      - entity: sensor.chatgpt_usage_cost_current_month
        name: Cout mois courant
      - entity: sensor.chatgpt_usage_input_tokens_today
      - entity: sensor.chatgpt_usage_output_tokens_today
      - entity: sensor.chatgpt_usage_last_update
  - type: gauge
    entity: sensor.chatgpt_codex_5h_remaining_percent
    name: Codex restant 5h
    min: 0
    max: 100
    severity:
      red: 0
      yellow: 20
      green: 50
  - type: gauge
    entity: sensor.chatgpt_codex_weekly_remaining_percent
    name: Codex restant hebdo
    min: 0
    max: 100
    severity:
      red: 0
      yellow: 20
      green: 50
  - type: entities
    entities:
      - entity: sensor.chatgpt_codex_limit_status
      - entity: sensor.chatgpt_codex_last_update
```

## Automatisations

```yaml
alias: ChatGPT usage - cout quotidien eleve
trigger:
  - platform: numeric_state
    entity_id: sensor.chatgpt_usage_cost_today
    above: 2
action:
  - service: notify.notify
    data:
      message: "Le cout OpenAI du jour depasse 2 USD."
```

```yaml
alias: ChatGPT usage - Codex 5h faible
trigger:
  - platform: numeric_state
    entity_id: sensor.chatgpt_codex_5h_remaining_percent
    below: 20
action:
  - service: notify.notify
    data:
      message: "Le restant Codex 5h est inferieur a 20 %."
```

```yaml
alias: ChatGPT usage - API indisponible
trigger:
  - platform: state
    entity_id: binary_sensor.chatgpt_usage_api_status
    to: "off"
action:
  - service: notify.notify
    data:
      message: "L'API OpenAI ne repond plus ou l'authentification a echoue."
```

```yaml
alias: ChatGPT usage - resume quotidien
trigger:
  - platform: time
    at: "23:30:00"
action:
  - service: notify.notify
    data:
      message: >
        OpenAI aujourd'hui: {{ states('sensor.chatgpt_usage_cost_today') }} USD,
        tokens: {{ states('sensor.chatgpt_usage_total_tokens_today') }},
        Codex 5h restant: {{ states('sensor.chatgpt_codex_5h_remaining_percent') }} %.
```

## Commandes utiles

```bash
pytest
```

## Notes developpement

Les endpoints utilises sont les endpoints officiels d'organisation OpenAI pour les couts et l'usage completions. Le mode Codex est separe car il n'existe pas d'API publique officielle documentee pour l'usage ChatGPT/Codex personnel.
