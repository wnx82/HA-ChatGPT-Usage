"""Constants for the ChatGPT Usage integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "chatgpt_usage"
NAME = "ChatGPT Usage"
VERSION = "1.5.2"

CONF_MODE = "mode"
CONF_API_KEY = "api_key"
CONF_ORG_ID = "org_id"
CONF_PROJECT_ID = "project_id"
CONF_CURRENCY = "currency"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_ENABLE_CODEX = "enable_codex"
CONF_CODEX_SOURCE = "codex_source"
CONF_CODEX_FILE_PATH = "codex_file_path"
CONF_MQTT_PREFIX = "mqtt_prefix"
CONF_DAILY_COST_ALERT = "daily_cost_alert"
CONF_CODEX_REMAINING_ALERT = "codex_remaining_alert"
CONF_CHATGPT_ACCOUNT_LINKED = "chatgpt_account_linked"

MODE_OPENAI = "openai"
MODE_CODEX_MQTT = "codex_mqtt"
MODE_CODEX_FILE = "codex_file"
MODE_BOTH = "both"
MODES = [MODE_OPENAI, MODE_CODEX_MQTT, MODE_CODEX_FILE, MODE_BOTH]

CODEX_SOURCE_MQTT = "mqtt"
CODEX_SOURCE_FILE = "file"
CODEX_SOURCES = [CODEX_SOURCE_MQTT, CODEX_SOURCE_FILE]

DEFAULT_CURRENCY = "USD"
DEFAULT_SCAN_INTERVAL = 3600
DEFAULT_SCAN_INTERVAL_DELTA = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
DEFAULT_MQTT_PREFIX = "codex/usage"
DEFAULT_CODEX_SOURCE = CODEX_SOURCE_FILE
DEFAULT_CODEX_FILE_PATH = "/config/chatgpt_usage_codex.json"
DEFAULT_DAILY_COST_ALERT = 2.0
DEFAULT_CODEX_REMAINING_ALERT = 20.0
CHATGPT_CODEX_USAGE_URL = "https://chatgpt.com/codex/cloud/settings/analytics"

OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_COSTS_ENDPOINT = "/organization/costs"
OPENAI_USAGE_COMPLETIONS_ENDPOINT = "/organization/usage/completions"

PLATFORMS = ["sensor", "binary_sensor"]
