"""Data coordinators for ChatGPT Usage."""

from __future__ import annotations

from datetime import timedelta
import logging
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

