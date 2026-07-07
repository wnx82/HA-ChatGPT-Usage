from datetime import UTC, datetime

from custom_components.chatgpt_usage.codex import normalize_codex_snapshot


def test_normalize_codex_snapshot_converts_timestamps():
    snapshot = normalize_codex_snapshot(
        {
            "5h_used": 12,
            "5h_reset": "2026-07-07T12:00:00Z",
            "last_update": "2026-07-07T12:30:00Z",
            "plan": "pro",
        }
    )

    assert snapshot["5h_used"] == 12
    assert snapshot["plan"] == "pro"
    assert snapshot["5h_reset"] == datetime(2026, 7, 7, 12, 0, tzinfo=UTC)
    assert snapshot["last_update"] == datetime(2026, 7, 7, 12, 30, tzinfo=UTC)
