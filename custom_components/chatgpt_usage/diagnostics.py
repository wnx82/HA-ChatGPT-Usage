"""Diagnostics for ChatGPT Usage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

from .const import CONF_API_KEY

REDACTED = "**REDACTED**"


def redact_sensitive_data(data: Any) -> Any:
    """Redact sensitive fields recursively."""
    if isinstance(data, dict):
        return {
            key: REDACTED if key in {CONF_API_KEY, "authorization", "token", "password", "secret"} else redact_sensitive_data(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [redact_sensitive_data(value) for value in data]
    return data


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return diagnostics with secrets masked."""
    return {
        "entry": {
            "data": redact_sensitive_data(entry.data),
            "options": redact_sensitive_data(entry.options),
        }
    }
