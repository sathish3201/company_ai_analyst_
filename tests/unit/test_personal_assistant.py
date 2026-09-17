import pytest

from company_ai.assistant.personal_assistant import (
    PersonalAssistant,
)
from company_ai.models.assistant import (
    AssistantRequest,
)
from company_ai.models.context import (
    ContextBundle,
    ContextItem,
    IntentType,
)


@pytest.mark.asyncio
async def test_personal_assistant_data_analysis(
    mocker,
):

    intent_analyzer = mocker.Mock()

    intent_analyzer.analyze = mocker.AsyncMock(
        return_value=IntentType.DATA_ANALYSIS
    )

    context_engine = mocker.Mock()

    context_engine.build = mocker.AsyncMock(
        return_value=ContextBundle(
            items=[
                ContextItem(
                    source="request",
                    content="Show sales",
                    relevance=1.0,
                ),
                ContextItem(
                    source="enterprise",
                    content="Company context",
                    relevance=0.9,
                ),
            ]
        )
    )

    assistant = PersonalAssistant(
        intent_analyzer=intent_analyzer,
        context_engine=context_engine,
    )

    request = AssistantRequest(
        message="Show sales",
        session_id="session-1",
    )

    response = await assistant.handle(
        request
    )

    assert response.intent == "data_analysis"
    assert response.requires_agent is True

    assert response.context_used == [
        "request",
        "enterprise",
    ]

    intent_analyzer.analyze.assert_awaited_once_with(
        "Show sales"
    )

    context_engine.build.assert_awaited_once_with(
        "Show sales"
    )


@pytest.mark.asyncio
async def test_personal_assistant_general_request(
    mocker,
):

    intent_analyzer = mocker.Mock()

    intent_analyzer.analyze = mocker.AsyncMock(
        return_value=IntentType.GENERAL
    )

    context_engine = mocker.Mock()

    context_engine.build = mocker.AsyncMock(
        return_value=ContextBundle()
    )

    assistant = PersonalAssistant(
        intent_analyzer=intent_analyzer,
        context_engine=context_engine,
    )

    request = AssistantRequest(
        message="Hello",
        session_id="session-1",
    )

    response = await assistant.handle(
        request
    )

    assert response.intent == "general"
    assert response.requires_agent is False
    assert response.context_used == []