"""Async OpenAI usage client and parsing helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
import logging
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import (
    OPENAI_BASE_URL,
    OPENAI_COSTS_ENDPOINT,
    OPENAI_USAGE_COMPLETIONS_ENDPOINT,
)
from .parsers import parse_cost_buckets, parse_usage_buckets

_LOGGER = logging.getLogger(__name__)


class ChatGPTUsageError(Exception):
    """Base error for ChatGPT Usage."""


class ChatGPTUsageAuthError(ChatGPTUsageError):
    """Authentication failed."""


class ChatGPTUsageRateLimitError(ChatGPTUsageError):
    """OpenAI API rate limit was reached."""


@dataclass(slots=True)
class OpenAIUsageSnapshot:
    """Normalized usage data returned by OpenAI organization endpoints."""

    cost_today: float | None = None
    cost_yesterday: float | None = None
    cost_current_month: float | None = None
    cost_last_7_days: float | None = None
    requests_today: int | None = None
    input_tokens_today: int | None = None
    output_tokens_today: int | None = None
    total_tokens_today: int | None = None
    models: dict[str, dict[str, int]] = field(default_factory=dict)
    projects: dict[str, dict[str, int]] = field(default_factory=dict)
    last_update: str | None = None
    api_available: bool = True
    recent_error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return a Home Assistant friendly dict."""
        return {
            "cost_today": self.cost_today,
            "cost_yesterday": self.cost_yesterday,
            "cost_current_month": self.cost_current_month,
            "cost_last_7_days": self.cost_last_7_days,
            "requests_today": self.requests_today,
            "input_tokens_today": self.input_tokens_today,
            "output_tokens_today": self.output_tokens_today,
            "total_tokens_today": self.total_tokens_today,
            "models": self.models,
            "projects": self.projects,
            "last_update": self.last_update,
            "api_available": self.api_available,
            "recent_error": self.recent_error,
        }


def _day_bounds(now: datetime | None = None) -> dict[str, int]:
    """Return Unix second bounds used by OpenAI usage endpoints."""
    current = now or datetime.now(UTC)
    today = current.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    month = today.replace(day=1)
    last_7 = today - timedelta(days=6)
    tomorrow = today + timedelta(days=1)
    return {
        "yesterday": int(yesterday.timestamp()),
        "today": int(today.timestamp()),
        "tomorrow": int(tomorrow.timestamp()),
        "month": int(month.timestamp()),
        "last_7": int(last_7.timestamp()),
    }


class OpenAIUsageClient:
    """Small async client for official OpenAI organization usage endpoints."""

    def __init__(
        self,
        session: ClientSession,
        api_key: str,
        org_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        self._session = session
        self._api_key = api_key
        self._org_id = org_id
        self._project_id = project_id

    @property
    def _headers(self) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        if self._org_id:
            headers["OpenAI-Organization"] = self._org_id
        if self._project_id:
            headers["OpenAI-Project"] = self._project_id
        return headers

    async def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            async with self._session.get(
                f"{OPENAI_BASE_URL}{endpoint}",
                headers=self._headers,
                params=params,
                timeout=30,
            ) as response:
                if response.status in (401, 403):
                    raise ChatGPTUsageAuthError("OpenAI authentication failed")
                if response.status == 429:
                    raise ChatGPTUsageRateLimitError("OpenAI rate limit reached")
                response.raise_for_status()
                return await response.json()
        except (ChatGPTUsageAuthError, ChatGPTUsageRateLimitError):
            raise
        except ClientResponseError as err:
            raise ChatGPTUsageError(f"OpenAI HTTP error {err.status}") from err
        except ClientError as err:
            raise ChatGPTUsageError("OpenAI API request failed") from err

    async def fetch_snapshot(self) -> OpenAIUsageSnapshot:
        """Fetch cost and token usage from official organization endpoints."""
        bounds = _day_bounds()
        snapshot = OpenAIUsageSnapshot(last_update=datetime.now(UTC).isoformat())
        costs_payload = await self._get(
            OPENAI_COSTS_ENDPOINT,
            {
                "start_time": bounds["last_7"],
                "end_time": bounds["tomorrow"],
                "bucket_width": "1d",
            },
        )
        costs = parse_cost_buckets(costs_payload)
        snapshot.cost_today = costs.get(str(bounds["today"]), 0.0)
        snapshot.cost_yesterday = costs.get(str(bounds["yesterday"]), 0.0)
        snapshot.cost_last_7_days = round(sum(costs.values()), 6)

        month_payload = await self._get(
            OPENAI_COSTS_ENDPOINT,
            {
                "start_time": bounds["month"],
                "end_time": bounds["tomorrow"],
                "bucket_width": "1d",
            },
        )
        snapshot.cost_current_month = round(sum(parse_cost_buckets(month_payload).values()), 6)

        usage_payload = await self._get(
            OPENAI_USAGE_COMPLETIONS_ENDPOINT,
            {
                "start_time": bounds["today"],
                "end_time": bounds["tomorrow"],
                "bucket_width": "1d",
                "group_by": ["model", "project_id"],
            },
        )
        usage = parse_usage_buckets(usage_payload)
        snapshot.requests_today = usage["requests"]
        snapshot.input_tokens_today = usage["input_tokens"]
        snapshot.output_tokens_today = usage["output_tokens"]
        snapshot.total_tokens_today = usage["total_tokens"]
        snapshot.models = usage["models"]
        snapshot.projects = usage["projects"]
        _LOGGER.debug("OpenAI usage snapshot updated")
        return snapshot
