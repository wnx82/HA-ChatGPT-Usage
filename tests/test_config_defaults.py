from types import SimpleNamespace

from custom_components.chatgpt_usage.const import CONF_MODE, MODE_CODEX_FILE, MODE_OPENAI


def resolve_mode(entry: SimpleNamespace) -> str:
    return entry.options.get(CONF_MODE, entry.data.get(CONF_MODE, MODE_OPENAI))


def test_mode_defaults_to_config_entry_data():
    entry = SimpleNamespace(data={CONF_MODE: MODE_CODEX_FILE}, options={})

    assert resolve_mode(entry) == MODE_CODEX_FILE


def test_mode_options_override_config_entry_data():
    entry = SimpleNamespace(
        data={CONF_MODE: MODE_CODEX_FILE},
        options={CONF_MODE: MODE_OPENAI},
    )

    assert resolve_mode(entry) == MODE_OPENAI
