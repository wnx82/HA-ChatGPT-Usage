"""Binary sensor platform for ChatGPT Usage."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up ChatGPT Usage binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinators"].get("openai")
    if coordinator is not None:
        async_add_entities([ChatGPTUsageApiStatusBinarySensor(coordinator, entry)])


class ChatGPTUsageApiStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """OpenAI API status binary sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "api_status"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: Any, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_api_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "ChatGPT Usage",
            "manufacturer": "OpenAI",
        }

    @property
    def is_on(self) -> bool:
        """Return true when the API is available."""
        return bool(self.coordinator.data.get("api_available", False))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return diagnostic attributes."""
        return {
            "source": "openai_api",
            "recent_error": self.coordinator.data.get("recent_error"),
        }

