import pytest

from company_ai.contracts.llm import (
    LLMRequest,
    Message,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_completion(llm_gateway):

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[
            Message(
                role="user",
                content="Say hello in one sentence.",
            )
        ],
    )

    response = await llm_gateway.complete(request)

    assert response.content
    assert response.model