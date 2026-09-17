import os

import pytest

from company_ai.contracts.llm import (
    LLMRequest,
    Message,
)
from company_ai.llm.litellm_gateway import (
    LiteLLMGateway,
)
from company_ai.llm.model_registry import (
    ModelRegistry,
    ModelRoute,
)


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "ollama/qwen2.5-coder:1.5b",
)


def create_ollama_registry() -> ModelRegistry:
    return ModelRegistry(
        routes=[
            ModelRoute(
                purpose="personal_assistant",
                primary=OLLAMA_MODEL,
                fallbacks=(),
                max_retries=0,
            )
        ]
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_gateway_real_completion():

    gateway = LiteLLMGateway(
        model_registry=create_ollama_registry(),
    )

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[
            Message(
                role="user",
                content="Reply with exactly OLLAMA_OK",
            )
        ],
        temperature=0.0,
        max_tokens=20,
    )

    response = await gateway.complete(request)

    assert response.content
    assert response.model == OLLAMA_MODEL

    print(
        "\nOllama response:",
        response.content,
    )