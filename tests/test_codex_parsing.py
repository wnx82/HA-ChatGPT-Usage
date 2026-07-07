from datetime import UTC, datetime

from custom_components.chatgpt_usage.codex import parse_codex_payload, parse_codex_timestamp


def test_parse_codex_payload_accepts_plain_numbers():
    assert parse_codex_payload("42") == 42
    assert parse_codex_payload("18.5") == 18.5


def test_parse_codex_payload_accepts_json_value():
    assert parse_codex_payload('{"value": 19.5, "updated_at": "2026-07-07T12:00:00Z"}') == 19.5


def test_parse_codex_payload_accepts_plain_text():
    assert parse_codex_payload("limited") == "limited"


def test_parse_codex_timestamp_accepts_zulu_time():
    assert parse_codex_timestamp("2026-07-07T12:00:00Z") == datetime(2026, 7, 7, 12, 0, tzinfo=UTC)
