"""Pure parsing helpers for ChatGPT Usage."""

from __future__ import annotations

from typing import Any


def _amount_value(amount: Any) -> float:
    """Extract a numeric amount from OpenAI cost response variants."""
    if isinstance(amount, dict):
        value = amount.get("value", 0)
    else:
        value = amount or 0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def parse_cost_buckets(payload: dict[str, Any]) -> dict[str, float]:
    """Parse OpenAI organization cost buckets keyed by bucket start time."""
    parsed: dict[str, float] = {}
    for bucket in payload.get("data", []):
        start_time = bucket.get("start_time")
        if start_time is None:
            continue
        total = 0.0
        for result in bucket.get("results", []):
            total += _amount_value(result.get("amount"))
        parsed[str(start_time)] = round(total, 6)
    return parsed


def parse_usage_buckets(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse OpenAI organization usage buckets into token/request totals."""
    totals = {
        "requests": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "models": {},
        "projects": {},
    }
    for bucket in payload.get("data", []):
        for result in bucket.get("results", []):
            requests = int(result.get("num_model_requests") or result.get("requests") or 0)
            input_tokens = int(result.get("input_tokens") or 0)
            output_tokens = int(result.get("output_tokens") or 0)
            total_tokens = int(result.get("total_tokens") or input_tokens + output_tokens)
            totals["requests"] += requests
            totals["input_tokens"] += input_tokens
            totals["output_tokens"] += output_tokens
            totals["total_tokens"] += total_tokens

            for key_name, container_name in (("model", "models"), ("project_id", "projects")):
                key = result.get(key_name)
                if not key:
                    continue
                container = totals[container_name].setdefault(
                    key,
                    {"requests": 0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
                )
                container["requests"] += requests
                container["input_tokens"] += input_tokens
                container["output_tokens"] += output_tokens
                container["total_tokens"] += total_tokens
    return totals

