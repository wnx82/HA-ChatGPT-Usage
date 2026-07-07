"""ChatGPT Usage integration for Home Assistant."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from .const import (
    CONF_CODEX_FILE_PATH,
    CONF_CODEX_SOURCE,
    CONF_ENABLE_CODEX,
    CONF_MODE,
    CONF_SCAN_INTERVAL,
    DEFAULT_CODEX_SOURCE,
    DEFAULT_SCAN_INTERVAL,
    MODE_BOTH,
    MODE_CODEX_FILE,
    DOMAIN,
    MODE_CODEX_MQTT,
    MODE_OPENAI,
    PLATFORMS,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ChatGPT Usage from a config entry."""
    from homeassistant.const import Platform

    from .coordinator import ChatGPTUsageCoordinator, LocalCodexUsageCoordinator

    hass.data.setdefault(DOMAIN, {})
    coordinators = {}
    mode = entry.data.get(CONF_MODE, MODE_OPENAI)
    if mode not in (MODE_CODEX_MQTT, MODE_CODEX_FILE):
        scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))
        coordinator = ChatGPTUsageCoordinator(hass, entry, timedelta(seconds=scan_interval))
        await coordinator.async_config_entry_first_refresh()
        coordinators["openai"] = coordinator

    codex_enabled = mode in (MODE_CODEX_MQTT, MODE_CODEX_FILE, MODE_BOTH) or entry.options.get(
        CONF_ENABLE_CODEX,
        entry.data.get(CONF_ENABLE_CODEX, False),
    )
    codex_source = entry.options.get(CONF_CODEX_SOURCE, entry.data.get(CONF_CODEX_SOURCE, DEFAULT_CODEX_SOURCE))
    if mode == MODE_CODEX_MQTT:
        codex_source = "mqtt"
    elif mode == MODE_CODEX_FILE:
        codex_source = "file"

    if codex_enabled and codex_source == "file":
        scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))
        codex_coordinator = LocalCodexUsageCoordinator(
            hass,
            entry,
            timedelta(seconds=scan_interval),
            entry.options.get(CONF_CODEX_FILE_PATH, entry.data.get(CONF_CODEX_FILE_PATH, "")),
        )
        await codex_coordinator.async_config_entry_first_refresh()
        coordinators["codex"] = codex_coordinator

    hass.data[DOMAIN][entry.entry_id] = {"coordinators": coordinators}
    platforms = [Platform.SENSOR]
    if mode not in (MODE_CODEX_MQTT, MODE_CODEX_FILE):
        platforms.append(Platform.BINARY_SENSOR)
    if codex_enabled:
        platforms = [Platform.SENSOR] + ([Platform.BINARY_SENSOR] if Platform.BINARY_SENSOR in platforms else [])
    await hass.config_entries.async_forward_entry_setups(entry, platforms)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    from homeassistant.const import Platform

    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform(platform) for platform in PLATFORMS])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration when options change."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
