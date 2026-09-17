import pytest

from company_ai.assistant.intent import IntentAnalyzer
from company_ai.assistant.personal_assistant import (
    PersonalAssistant,
)
from company_ai.context_engine.assembler import (
    ContextAssembler,
)
from company_ai.context_engine.compressor import (
    ContextCompressor,
)
from company_ai.context_engine.engine import (
    ContextEngine,
)
from company_ai.context_engine.filter import (
    ContextFilter,
)
from company_ai.context_engine.providers.enterprise_provider import (
    EnterpriseContextProvider,
)
from company_ai.context_engine.providers.request_provider import (
    RequestContextProvider,
)
from company_ai.context_engine.providers.user_provider import (
    UserContextProvider,
)
from company_ai.context_engine.ranker import (
    ContextRanker,
)
from company_ai.contracts.llm import LLMResponse
from company_ai.models.assistant import AssistantRequest


@pytest.mark.asyncio
async def test_personal_assistant_end_to_end(
    mocker,
):

    # ---------------------------------------------------------
    # External dependency: mocked LLM
    # ---------------------------------------------------------

    llm = mocker.Mock()

    llm.complete = mocker.AsyncMock(
        return_value=LLMResponse(
            content="data_analysis",
            model="test-model",
        )
    )

    # ---------------------------------------------------------
    # Real Day-2 components
    # ---------------------------------------------------------

    intent_analyzer = IntentAnalyzer(
        llm=llm
    )

    context_engine = ContextEngine(
        providers=[
            RequestContextProvider(),
            UserContextProvider(
                user_context=(
                    "User is an enterprise data analyst"
                )
            ),
            EnterpriseContextProvider(
                enterprise_context=(
                    "Company fiscal year uses "
                    "quarterly reporting"
                )
            ),
        ],
        ranker=ContextRanker(),
        context_filter=ContextFilter(),
        compressor=ContextCompressor(),
        assembler=ContextAssembler(),
    )

    assistant = PersonalAssistant(
        intent_analyzer=intent_analyzer,
        context_engine=context_engine,
    )

    # ---------------------------------------------------------
    # User request
    # ---------------------------------------------------------

    request = AssistantRequest(
        message=(
            "Show me sales performance "
            "for APAC in Q2"
        ),
        session_id="session-001",
    )

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    response = await assistant.handle(
        request
    )

    # ---------------------------------------------------------
    # Verify
    # ---------------------------------------------------------

    assert response.intent == "data_analysis"

    assert response.requires_agent is True

    assert "request" in response.context_used

    assert "user" in response.context_used

    assert "enterprise" in response.context_used

    llm.complete.assert_awaited_once()