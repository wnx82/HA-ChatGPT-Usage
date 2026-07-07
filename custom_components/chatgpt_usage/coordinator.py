"""Data coordinators for ChatGPT Usage."""

from __future__ import annotations

from datetime import timedelta
import json
import logging
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    ChatGPTUsageAuthError,
    ChatGPTUsageError,
    ChatGPTUsageRateLimitError,
    OpenAIUsageClient,
    OpenAIUsageSnapshot,
)
from .codex import normalize_codex_snapshot
from .const import CONF_API_KEY, CONF_ORG_ID, CONF_PROJECT_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ChatGPTUsageCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for official OpenAI organization usage."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=update_interval,
        )
        self.entry = entry
        session = async_get_clientsession(hass)
        self.client = OpenAIUsageClient(
            session=session,
            api_key=entry.data[CONF_API_KEY],
            org_id=entry.options.get(CONF_ORG_ID) or entry.data.get(CONF_ORG_ID),
            project_id=entry.options.get(CONF_PROJECT_ID) or entry.data.get(CONF_PROJECT_ID),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return (await self.client.fetch_snapshot()).as_dict()
        except ChatGPTUsageAuthError as err:
            snapshot = OpenAIUsageSnapshot(api_available=False, recent_error=str(err))
            return snapshot.as_dict()
        except ChatGPTUsageRateLimitError as err:
            raise UpdateFailed("OpenAI rate limit reached") from err
        except ChatGPTUsageError as err:
            raise UpdateFailed(str(err)) from err


class LocalCodexUsageCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for local Codex usage snapshots stored as JSON."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        update_interval: timedelta,
        file_path: str,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}_codex_file",
            update_interval=update_interval,
        )
        self.entry = entry
        self.file_path = file_path

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self._load_snapshot)
        except FileNotFoundError:
            return self._placeholder_snapshot("waiting_for_file")
        except json.JSONDecodeError:
            return self._placeholder_snapshot("invalid_json")
        except OSError as err:
            raise UpdateFailed(f"Unable to read Codex file: {self.file_path}") from err

    def _load_snapshot(self) -> dict[str, Any]:
        payload = json.loads(Path(self.file_path).read_text(encoding="utf-8"))
        snapshot = normalize_codex_snapshot(payload)
        snapshot["source"] = "codex_local_file"
        snapshot["path"] = self.file_path
        snapshot["status"] = "loaded"
        return snapshot

    def _placeholder_snapshot(self, status: str) -> dict[str, Any]:
        """Return a non-failing placeholder when the file is not ready yet."""
        return {
            "source": "codex_local_file",
            "path": self.file_path,
            "status": status,
        }
