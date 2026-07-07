from custom_components.chatgpt_usage.diagnostics import REDACTED, redact_sensitive_data


def test_redact_sensitive_data_masks_secrets_recursively():
    data = {
        "api_key": "fake-api-key",
        "nested": {
            "token": "abc",
            "safe": "value",
        },
    }

    assert redact_sensitive_data(data) == {
        "api_key": REDACTED,
        "nested": {
            "token": REDACTED,
            "safe": "value",
        },
    }
