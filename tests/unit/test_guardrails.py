import pytest

from company_ai.contracts.llm import (
    LLMRequest,
    Message,
)

from company_ai.llm.guardrails import (
    NoOpGuardrail,
)


@pytest.mark.asyncio
async def test_noop_guardrail_input():

    guardrail = NoOpGuardrail()

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[
            Message(
                role="user",
                content="Hello",
            )
        ],
    )

    await guardrail.validate_input(request)


@pytest.mark.asyncio
async def test_noop_guardrail_output():

    guardrail = NoOpGuardrail()

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[],
    )

    response = ...

    # Replace with your LLMResponse instance.
    await guardrail.validate_output(
        request,
        response,
    )