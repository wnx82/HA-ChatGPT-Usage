from custom_components.chatgpt_usage.parsers import parse_cost_buckets, parse_usage_buckets


def test_parse_cost_buckets_handles_amount_objects():
    payload = {
        "data": [
            {
                "start_time": 1719878400,
                "results": [
                    {"amount": {"value": 1.25, "currency": "usd"}},
                    {"amount": {"value": "0.75", "currency": "usd"}},
                ],
            }
        ]
    }

    assert parse_cost_buckets(payload) == {"1719878400": 2.0}


def test_parse_usage_buckets_groups_models_and_projects():
    payload = {
        "data": [
            {
                "results": [
                    {
                        "model": "gpt-5-mini",
                        "project_id": "proj_123",
                        "num_model_requests": 2,
                        "input_tokens": 10,
                        "output_tokens": 5,
                    }
                ]
            }
        ]
    }

    parsed = parse_usage_buckets(payload)

    assert parsed["requests"] == 2
    assert parsed["input_tokens"] == 10
    assert parsed["output_tokens"] == 5
    assert parsed["total_tokens"] == 15
    assert parsed["models"]["gpt-5-mini"]["total_tokens"] == 15
    assert parsed["projects"]["proj_123"]["requests"] == 2
