from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_config_flow_supports_mode_and_api_key_in_options():
    content = (ROOT / "custom_components" / "chatgpt_usage" / "config_flow.py").read_text(encoding="utf-8")

    assert "vol.Required(CONF_MODE" in content
    assert "vol.Optional(CONF_API_KEY" in content
    assert 'errors[CONF_API_KEY] = "api_key_required"' in content


def test_coordinator_reads_api_key_from_options():
    content = (ROOT / "custom_components" / "chatgpt_usage" / "coordinator.py").read_text(encoding="utf-8")

    assert 'entry.options.get(CONF_API_KEY, entry.data.get(CONF_API_KEY, ""))' in content
