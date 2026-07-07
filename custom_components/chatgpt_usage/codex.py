"""Codex MQTT parsing helpers."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from typing import Any


def parse_codex_payload(payload: str) -> Any:
    """Parse a Codex MQTT payload.

    Bridge payloads may be plain strings/numbers or JSON values. If a JSON object
    contains a `value` key, that value is used as the entity state.
    """
    raw = payload.strip()
    if raw == "":
        return None
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError:
        decoded = raw

    if isinstance(decoded, dict) and "value" in decoded:
        decoded = decoded["value"]

    if isinstance(decoded, bool):
        return decoded
    if isinstance(decoded, (int, float)):
        return decoded
    if isinstance(decoded, str):
        try:
            if "." in decoded:
                return float(decoded)
            return int(decoded)
        except ValueError:
            return decoded
    return decoded


def parse_codex_timestamp(value: Any) -> datetime | Any:
    """Convert ISO timestamp strings to timezone-aware datetimes."""
    if not isinstance(value, str):
        return value
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return value
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed
