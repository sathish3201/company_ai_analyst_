import pytest

from company_ai.assistant.intent import IntentAnalyzer
from company_ai.contracts.llm import LLMResponse
from company_ai.models.context import IntentType


@pytest.mark.asyncio
async def test_intent_data_analysis(mocker):

    llm = mocker.Mock()

    llm.complete = mocker.AsyncMock(
        return_value=LLMResponse(
            content="data_analysis",
            model="test-model",
        )
    )

    analyzer = IntentAnalyzer(llm)

    result = await analyzer.analyze(
        "Show me sales revenue by region"
    )

    assert result == IntentType.DATA_ANALYSIS

    llm.complete.assert_awaited_once()


@pytest.mark.asyncio
async def test_intent_rag(mocker):

    llm = mocker.Mock()

    llm.complete = mocker.AsyncMock(
        return_value=LLMResponse(
            content="rag",
            model="test-model",
        )
    )

    analyzer = IntentAnalyzer(llm)

    result = await analyzer.analyze(
        "What is our company leave policy?"
    )

    assert result == IntentType.RAG


@pytest.mark.asyncio
async def test_intent_general(mocker):

    llm = mocker.Mock()

    llm.complete = mocker.AsyncMock(
        return_value=LLMResponse(
            content="general",
            model="test-model",
        )
    )

    analyzer = IntentAnalyzer(llm)

    result = await analyzer.analyze(
        "Hello"
    )

    assert result == IntentType.GENERAL


@pytest.mark.asyncio
async def test_invalid_intent_returns_unknown(mocker):

    llm = mocker.Mock()

    llm.complete = mocker.AsyncMock(
        return_value=LLMResponse(
            content="something_invalid",
            model="test-model",
        )
    )

    analyzer = IntentAnalyzer(llm)

    result = await analyzer.analyze(
        "Do something"
    )

    assert result == IntentType.UNKNOWN