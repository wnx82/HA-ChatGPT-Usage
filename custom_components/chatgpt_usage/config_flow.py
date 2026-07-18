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
    CODEX_SOURCES,
    CHATGPT_CODEX_USAGE_URL,
    DOMAIN,
    MODES,
    MODE_BOTH,
    MODE_CODEX_FILE,
    MODE_OPENAI,
)


def _link_schema() -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_CHATGPT_ACCOUNT_LINKED, default=False): bool,
        }
    )


def _default_config_data() -> dict[str, Any]:
    """Return the automatic setup defaults used by the first-run flow."""
    return {
        CONF_MODE: MODE_CODEX_FILE,
        CONF_API_KEY: "",
        CONF_ORG_ID: "",
        CONF_PROJECT_ID: "",
        CONF_CURRENCY: DEFAULT_CURRENCY,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        CONF_ENABLE_CODEX: True,
        CONF_CODEX_SOURCE: DEFAULT_CODEX_SOURCE,
        CONF_CODEX_FILE_PATH: DEFAULT_CODEX_FILE_PATH,
        CONF_MQTT_PREFIX: DEFAULT_MQTT_PREFIX,
    }


def _options_schema(defaults: dict[str, Any]) -> vol.Schema:
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
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="ChatGPT Usage", data=_default_config_data())

        return self.async_show_form(
            step_id="user",
            data_schema=_link_schema(),
            errors=errors,
            description_placeholders={"chatgpt_url": CHATGPT_CODEX_USAGE_URL},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Return the options flow."""
        return ChatGPTUsageOptionsFlow(config_entry)


class ChatGPTUsageOptionsFlow(config_entries.OptionsFlow):
    """Handle options for ChatGPT Usage."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Manage integration options."""
        if user_input is not None:
            errors: dict[str, str] = {}
            mode = user_input.get(CONF_MODE, MODE_CODEX_FILE)
            api_key = str(user_input.get(CONF_API_KEY, "")).strip()
            codex_file_path = str(user_input.get(CONF_CODEX_FILE_PATH, "")).strip()

            if mode in (MODE_OPENAI, MODE_BOTH) and not api_key:
                errors[CONF_API_KEY] = "api_key_required"
            if mode == MODE_CODEX_FILE and not codex_file_path:
                errors[CONF_CODEX_FILE_PATH] = "codex_file_path_required"
            if mode == MODE_BOTH and user_input.get(CONF_CODEX_SOURCE) == DEFAULT_CODEX_SOURCE and not codex_file_path:
                errors[CONF_CODEX_FILE_PATH] = "codex_file_path_required"

            if errors:
                defaults = {**self._config_entry.data, **self._config_entry.options, **user_input}
                return self.async_show_form(
                    step_id="init",
                    data_schema=_options_schema(defaults),
                    errors=errors,
                )
            return self.async_create_entry(title="", data=user_input)
        defaults = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_options_schema(defaults))
