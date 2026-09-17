import pytest

from company_ai.llm.model_registry import (
    ModelRegistry,
    ModelRoute,
)


def test_get_model_route():

    route = ModelRoute(
        purpose="personal_assistant",
        primary="ollama/qwen2.5:32b",
        fallbacks=(
            "openai/gpt-5-mini",
        ),
    )

    registry = ModelRegistry([route])

    result = registry.get("personal_assistant")

    assert result.primary == "ollama/qwen2.5:32b"
    assert result.fallbacks == (
        "openai/gpt-5-mini",
    )


def test_unknown_model_purpose():

    registry = ModelRegistry([])

    with pytest.raises(KeyError):

        registry.get("unknown")