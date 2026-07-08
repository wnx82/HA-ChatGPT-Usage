# ChatGPT Usage

Version actuelle : `1.5.2`

ChatGPT Usage est une integration Home Assistant custom compatible HACS pour afficher l'abonnement et l'usage Codex/ChatGPT recuperes depuis une connexion web locale, ainsi que l'usage OpenAI API officiel si tu choisis aussi de renseigner une cle admin API.

## Stack technique

- Home Assistant custom integration
- Python async
- `DataUpdateCoordinator`
- `ConfigFlow` et `OptionsFlow`
- `aiohttp` via Home Assistant
- HACS

## Versioning

Le projet suit le format `x.y.z` decrit dans `CHANGELOG.md` : seul l'utilisateur decide un changement de version majeure `x`, `y` represente une nouvelle branche ou grande etape, et `z` une correction ou un ajustement dans l'etape. Les versions comme `1.10.0` ou `1.14.27` sont valides.

## Fonctionnalites

- Mode recommande sans cle API : capteurs Codex/ChatGPT alimentes par un fichier JSON local.
- Companion web local qui ouvre ChatGPT, te laisse te connecter manuellement, puis ecrit le JSON lu par Home Assistant.
- Recuperation best-effort de l'abonnement ChatGPT/Codex (`plan`), des credits, du statut de limite et des limites 5h/hebdo quand la page les affiche.
- Mode optionnel OpenAI API officiel : couts du jour, d'hier, du mois courant, des 7 derniers jours, requetes et tokens.
- Statut de connectivite API uniquement si le mode OpenAI API est active.
- Diagnostics Home Assistant avec masquage des secrets.

## Installation

1. Copier le dossier `custom_components/chatgpt_usage` dans `config/custom_components/chatgpt_usage`.
2. Redemarrer Home Assistant.
3. Ajouter l'integration depuis l'interface : Parametres > Appareils et services > Ajouter une integration > ChatGPT Usage.

## Configuration recommandee sans cle API

Le mode par defaut est `codex_file`. Il ne demande pas de cle API OpenAI.

1. Dans Home Assistant, ajoute l'integration `ChatGPT Usage`.
2. Le premier ecran te demande de lier ChatGPT/Codex : ouvre le lien affiche et connecte-toi.
3. Sur la machine qui peut ouvrir un navigateur, lance le companion :

```bash
npm install
npx playwright install chromium
npm run codex:companion -- --out /config/chatgpt_usage_codex.json
```

Le navigateur Chromium s'ouvre sur ChatGPT/Codex. Connecte-toi normalement, ouvre la page d'usage Codex si necessaire, puis appuie sur Entree dans le terminal. Le fichier JSON est ecrit pour Home Assistant.

Pour garder les capteurs a jour :

```bash
npm run codex:companion -- --out /config/chatgpt_usage_codex.json --watch-seconds 300
```

4. Coche la confirmation dans Home Assistant, puis laisse `Mode` sur `codex_file`.
5. Garde le chemin JSON par defaut ou choisis le chemin utilise avec `--out`.

Le profil navigateur persistant est stocke dans `.codex-web-companion/profile` pour eviter de te reconnecter a chaque lancement. Ce dossier est ignore par Git.

## Mode OpenAI API optionnel

Parametres principaux :

- `Mode` : `codex_file` par defaut, `codex_mqtt`, `openai` ou `both`.
- `OpenAI Admin API key` : cle API admin OpenAI pour les endpoints organisationnels, requise seulement pour `openai` ou `both`.
- `Organization ID` : optionnel.
- `Project ID` : optionnel.
- `Currency` : `USD` par defaut.
- `Scan interval` : `3600` secondes par defaut, minimum `300`.
- `Codex source` : `file` par defaut, ou `mqtt`.
- `Codex local JSON file path` : `/config/chatgpt_usage_codex.json` par defaut.
- `Codex MQTT prefix` : `codex/usage` par defaut si tu choisis MQTT.

Le mode Codex est experimental. Il ne demande jamais de mot de passe ChatGPT a Home Assistant et ne stocke aucun cookie ou token de session ChatGPT dans l'integration. Le companion conserve seulement un profil navigateur local ignore par Git.

## Mode Codex sans MQTT

Le chemin le plus simple sans MQTT est un fichier JSON local mis a jour par un script compagnon sur la machine qui connait deja ton usage Codex.

Exemple de fichier `/config/chatgpt_usage_codex.json` :

```json
{
  "5h_used": 42,
  "5h_remaining_percent": 18,
  "5h_reset": "2026-07-07T15:00:00Z",
  "weekly_used": 310,
  "weekly_remaining_percent": 44,
  "weekly_reset": "2026-07-13T00:00:00Z",
  "plan": "pro",
  "credits": 12.5,
  "limit_status": "limited",
  "last_update": "2026-07-07T14:30:00Z"
}
```

Home Assistant relit ce fichier selon `scan_interval`.

## Companion web local

Le companion web ouvre un vrai navigateur Chromium, te laisse te connecter toi-meme a ChatGPT, puis capture la page `Codex Settings > Usage Dashboard` pour ecrire le fichier JSON local.

Il essaie d'extraire :

- `plan` : abonnement visible (`free`, `go`, `plus`, `pro`, `team`, `business`, `enterprise`, `edu`).
- `credits` : credits ou solde visible.
- `limit_status` : `available`, `near_limit`, `limit_reached` ou `unknown`.
- `5h_*` et `weekly_*` : valeurs et resets visibles sur la page.
- `extraction_status` et `missing_fields` : aide au diagnostic si la page ne contient qu'une partie des informations.

Installation du companion :

```bash
npm install
npx playwright install chromium
```

Execution manuelle :

```bash
npm run codex:companion -- --out /config/chatgpt_usage_codex.json
```

Mode surveillance continue :

```bash
npm run codex:companion -- --out /config/chatgpt_usage_codex.json --watch-seconds 300
```

Important : il n'existe pas d'API publique officielle documentee pour lire l'abonnement ChatGPT personnel depuis Home Assistant. La recuperation de l'abonnement repose donc sur ce que la page web ChatGPT affiche au moment de la capture. Le parser reconnait des libelles anglais et francais courants, mais reste best-effort.

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

Voir `.env.example`. Les secrets reels ne sont pas requis dans le depot. En mode OpenAI API optionnel, la cle API est stockee dans la config entry Home Assistant.

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
python3 -m pytest
npm test
```

## Notes developpement

Les endpoints utilises en mode OpenAI API sont les endpoints officiels d'organisation OpenAI pour les couts et l'usage completions. Le mode Codex/ChatGPT est separe car l'abonnement ChatGPT et l'usage Codex personnel sont affiches dans ChatGPT web, pas exposes ici via une API publique officielle documentee. Le companion web local repose sur une capture best-effort de la page web ChatGPT, donc il peut necessiter des ajustements si l'interface evolue.
