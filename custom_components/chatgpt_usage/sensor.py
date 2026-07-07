"""Sensor platform for ChatGPT Usage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CURRENCY, PERCENTAGE, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .codex import parse_codex_payload
from .const import (
    CONF_ENABLE_CODEX,
    CONF_MODE,
    CONF_MQTT_PREFIX,
    DEFAULT_MQTT_PREFIX,
    DEFAULT_CURRENCY,
    DOMAIN,
    MODE_CODEX_MQTT,
)


@dataclass(frozen=True, kw_only=True)
class ChatGPTUsageSensorDescription(SensorEntityDescription):
    """Description for OpenAI usage sensors."""

    value_key: str
    source: str = "openai"


OPENAI_SENSORS: tuple[ChatGPTUsageSensorDescription, ...] = (
    ChatGPTUsageSensorDescription(
        key="cost_today",
        translation_key="cost_today",
        value_key="cost_today",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.TOTAL,
    ),
    ChatGPTUsageSensorDescription(key="cost_yesterday", translation_key="cost_yesterday", value_key="cost_yesterday"),
    ChatGPTUsageSensorDescription(key="cost_current_month", translation_key="cost_current_month", value_key="cost_current_month"),
    ChatGPTUsageSensorDescription(key="cost_last_7_days", translation_key="cost_last_7_days", value_key="cost_last_7_days"),
    ChatGPTUsageSensorDescription(key="requests_today", translation_key="requests_today", value_key="requests_today", state_class=SensorStateClass.TOTAL),
    ChatGPTUsageSensorDescription(key="input_tokens_today", translation_key="input_tokens_today", value_key="input_tokens_today", state_class=SensorStateClass.TOTAL),
    ChatGPTUsageSensorDescription(key="output_tokens_today", translation_key="output_tokens_today", value_key="output_tokens_today", state_class=SensorStateClass.TOTAL),
    ChatGPTUsageSensorDescription(key="total_tokens_today", translation_key="total_tokens_today", value_key="total_tokens_today", state_class=SensorStateClass.TOTAL),
    ChatGPTUsageSensorDescription(
        key="last_update",
        translation_key="last_update",
        value_key="last_update",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)

CODEX_SENSORS: tuple[ChatGPTUsageSensorDescription, ...] = (
    ChatGPTUsageSensorDescription(key="codex_5h_used", translation_key="codex_5h_used", value_key="5h_used", source="codex"),
    ChatGPTUsageSensorDescription(key="codex_5h_remaining_percent", translation_key="codex_5h_remaining_percent", value_key="5h_remaining_percent", native_unit_of_measurement=PERCENTAGE, source="codex"),
    ChatGPTUsageSensorDescription(key="codex_5h_reset", translation_key="codex_5h_reset", value_key="5h_reset", device_class=SensorDeviceClass.TIMESTAMP, source="codex"),
    ChatGPTUsageSensorDescription(key="codex_weekly_used", translation_key="codex_weekly_used", value_key="weekly_used", source="codex"),
    ChatGPTUsageSensorDescription(key="codex_weekly_remaining_percent", translation_key="codex_weekly_remaining_percent", value_key="weekly_remaining_percent", native_unit_of_measurement=PERCENTAGE, source="codex"),
    ChatGPTUsageSensorDescription(key="codex_weekly_reset", translation_key="codex_weekly_reset", value_key="weekly_reset", device_class=SensorDeviceClass.TIMESTAMP, source="codex"),
    ChatGPTUsageSensorDescription(key="codex_plan", translation_key="codex_plan", value_key="plan", source="codex"),
    ChatGPTUsageSensorDescription(key="codex_credits", translation_key="codex_credits", value_key="credits", source="codex"),
    ChatGPTUsageSensorDescription(key="codex_limit_status", translation_key="codex_limit_status", value_key="limit_status", source="codex"),
    ChatGPTUsageSensorDescription(key="codex_last_update", translation_key="codex_last_update", value_key="last_update", device_class=SensorDeviceClass.TIMESTAMP, source="codex"),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up ChatGPT Usage sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []
    coordinator = data["coordinators"].get("openai")
    if coordinator is not None:
        entities.extend(ChatGPTUsageSensor(coordinator, entry, description) for description in OPENAI_SENSORS)

    mode = entry.data.get(CONF_MODE)
    enable_codex = entry.options.get(CONF_ENABLE_CODEX, entry.data.get(CONF_ENABLE_CODEX, False))
    if mode == MODE_CODEX_MQTT or enable_codex:
        entities.extend(ChatGPTCodexMqttSensor(entry, description) for description in CODEX_SENSORS)

    async_add_entities(entities)


class ChatGPTUsageSensor(CoordinatorEntity, SensorEntity):
    """OpenAI usage sensor."""

    entity_description: ChatGPTUsageSensorDescription
    _attr_has_entity_name = True

    def __init__(self, coordinator: Any, entry: ConfigEntry, description: ChatGPTUsageSensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "ChatGPT Usage",
            "manufacturer": "OpenAI",
        }
        if description.key.startswith("cost_"):
            currency = entry.options.get(CONF_CURRENCY, entry.data.get(CONF_CURRENCY, DEFAULT_CURRENCY))
            self._attr_native_unit_of_measurement = currency

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self.coordinator.data.get(self.entity_description.value_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return common OpenAI attributes."""
        return {
            "source": "openai_api",
            "models": self.coordinator.data.get("models"),
            "projects": self.coordinator.data.get("projects"),
            "last_update": self.coordinator.data.get("last_update"),
            "recent_error": self.coordinator.data.get("recent_error"),
        }


class ChatGPTCodexMqttSensor(SensorEntity):
    """Experimental Codex MQTT sensor."""

    entity_description: ChatGPTUsageSensorDescription
    _attr_has_entity_name = True
    _attr_available = False

    def __init__(self, entry: ConfigEntry, description: ChatGPTUsageSensorDescription) -> None:
        self.entity_description = description
        self._entry = entry
        self._native_value: Any = None
        self._topic = f"{entry.options.get(CONF_MQTT_PREFIX, entry.data.get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX)).rstrip('/')}/{description.value_key}"
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "ChatGPT Codex Usage",
            "manufacturer": "OpenAI",
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to the configured MQTT topic."""
        from homeassistant.components import mqtt

        @callback
        def message_received(message: Any) -> None:
            self._native_value = parse_codex_payload(str(message.payload))
            self._attr_available = self._native_value is not None
            self.async_write_ha_state()

        remove_subscribe = await mqtt.async_subscribe(self.hass, self._topic, message_received, 0, "utf-8")
        self.async_on_remove(remove_subscribe)

    @property
    def native_value(self) -> Any:
        """Return the Codex value when a bridge provides it."""
        return self._native_value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return Codex source metadata."""
        return {
            "source": "codex_mqtt_bridge",
            "experimental": True,
            "topic": self._topic,
            "status": "connected" if self.available else "waiting_for_bridge",
        }

    @callback
    def _handle_mqtt_update(self, value: Any) -> None:
        """Update the sensor from a parsed MQTT value."""
        self._native_value = value
        self._attr_available = True
        self.async_write_ha_state()
