"""Config flow for ChatGPT Usage."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_CURRENCY, CONF_SCAN_INTERVAL
from homeassistant.core import callback

from .const import (
    CONF_CODEX_REMAINING_ALERT,
    CONF_CODEX_FILE_PATH,
    CONF_CODEX_SOURCE,
    CONF_CHATGPT_ACCOUNT_LINKED,
    CONF_DAILY_COST_ALERT,
    CONF_ENABLE_CODEX,
    CONF_MODE,
    CONF_MQTT_PREFIX,
    CONF_ORG_ID,
    CONF_PROJECT_ID,
    DEFAULT_CODEX_REMAINING_ALERT,
    DEFAULT_CODEX_FILE_PATH,
    DEFAULT_CODEX_SOURCE,
    DEFAULT_CURRENCY,
    DEFAULT_DAILY_COST_ALERT,
    DEFAULT_MQTT_PREFIX,
    DEFAULT_SCAN_INTERVAL,
    CODEX_SOURCE_FILE,
    CODEX_SOURCES,
    CHATGPT_CODEX_USAGE_URL,
    DOMAIN,
    MODE_BOTH,
    MODE_CODEX_FILE,
    MODES,
)


def _link_schema() -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_CHATGPT_ACCOUNT_LINKED, default=False): bool,
        }
    )


def _config_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(CONF_MODE, default=defaults.get(CONF_MODE, MODE_CODEX_FILE)): vol.In(MODES),
            vol.Optional(CONF_API_KEY, default=defaults.get(CONF_API_KEY, "")): str,
            vol.Optional(CONF_ORG_ID, default=defaults.get(CONF_ORG_ID, "")): str,
            vol.Optional(CONF_PROJECT_ID, default=defaults.get(CONF_PROJECT_ID, "")): str,
            vol.Optional(CONF_CURRENCY, default=defaults.get(CONF_CURRENCY, DEFAULT_CURRENCY)): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=300)),
            vol.Optional(CONF_ENABLE_CODEX, default=defaults.get(CONF_ENABLE_CODEX, False)): bool,
            vol.Optional(CONF_CODEX_SOURCE, default=defaults.get(CONF_CODEX_SOURCE, DEFAULT_CODEX_SOURCE)): vol.In(CODEX_SOURCES),
            vol.Optional(CONF_CODEX_FILE_PATH, default=defaults.get(CONF_CODEX_FILE_PATH, DEFAULT_CODEX_FILE_PATH)): str,
            vol.Optional(CONF_MQTT_PREFIX, default=defaults.get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX)): str,
        }
    )


def _options_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_ORG_ID, default=defaults.get(CONF_ORG_ID, "")): str,
            vol.Optional(CONF_PROJECT_ID, default=defaults.get(CONF_PROJECT_ID, "")): str,
            vol.Optional(CONF_CURRENCY, default=defaults.get(CONF_CURRENCY, DEFAULT_CURRENCY)): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=300)),
            vol.Optional(CONF_ENABLE_CODEX, default=defaults.get(CONF_ENABLE_CODEX, False)): bool,
            vol.Optional(CONF_CODEX_SOURCE, default=defaults.get(CONF_CODEX_SOURCE, DEFAULT_CODEX_SOURCE)): vol.In(CODEX_SOURCES),
            vol.Optional(CONF_CODEX_FILE_PATH, default=defaults.get(CONF_CODEX_FILE_PATH, DEFAULT_CODEX_FILE_PATH)): str,
            vol.Optional(CONF_MQTT_PREFIX, default=defaults.get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX)): str,
            vol.Optional(CONF_DAILY_COST_ALERT, default=defaults.get(CONF_DAILY_COST_ALERT, DEFAULT_DAILY_COST_ALERT)): vol.Coerce(float),
            vol.Optional(CONF_CODEX_REMAINING_ALERT, default=defaults.get(CONF_CODEX_REMAINING_ALERT, DEFAULT_CODEX_REMAINING_ALERT)): vol.Coerce(float),
        }
    )


class ChatGPTUsageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChatGPT Usage."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Start with ChatGPT account linking instructions."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if not user_input.get(CONF_CHATGPT_ACCOUNT_LINKED):
                errors[CONF_CHATGPT_ACCOUNT_LINKED] = "chatgpt_link_required"
            if not errors:
                return await self.async_step_settings()

        return self.async_show_form(
            step_id="user",
            data_schema=_link_schema(),
            errors=errors,
            description_placeholders={"chatgpt_url": CHATGPT_CODEX_USAGE_URL},
        )

    async def async_step_settings(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle integration settings after ChatGPT account linking."""
        errors: dict[str, str] = {}
        if user_input is not None:
            mode = user_input[CONF_MODE]
            if mode in ("openai", "both") and not user_input.get(CONF_API_KEY):
                errors[CONF_API_KEY] = "api_key_required"
            if mode == MODE_CODEX_FILE and not user_input.get(CONF_CODEX_FILE_PATH):
                errors[CONF_CODEX_FILE_PATH] = "codex_file_path_required"
            if mode == MODE_BOTH and user_input.get(CONF_CODEX_SOURCE) == CODEX_SOURCE_FILE and not user_input.get(CONF_CODEX_FILE_PATH):
                errors[CONF_CODEX_FILE_PATH] = "codex_file_path_required"
            if not errors:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="ChatGPT Usage", data=user_input)

        return self.async_show_form(step_id="settings", data_schema=_config_schema(user_input), errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Return the options flow."""
        return ChatGPTUsageOptionsFlow(config_entry)


class ChatGPTUsageOptionsFlow(config_entries.OptionsFlow):
    """Handle options for ChatGPT Usage."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Manage integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        defaults = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_options_schema(defaults))
