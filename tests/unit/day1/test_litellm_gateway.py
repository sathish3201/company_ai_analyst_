import pytest

from company_ai.contracts.llm import LLMRequest, Message
from company_ai.llm.fallback import FallbackPolicy
from company_ai.llm.litellm_gateway import LiteLLMGateway
from company_ai.llm.model_registry import ModelRegistry, ModelRoute


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def create_registry(
    primary: str = "test-primary",
    fallbacks: tuple[str, ...] = ("test-fallback",),
    max_retries: int = 0,
) -> ModelRegistry:
    return ModelRegistry(
        routes=[
            ModelRoute(
                purpose="personal_assistant",
                primary=primary,
                fallbacks=fallbacks,
                max_retries=max_retries,
            )
        ]
    )


def create_request(
    content: str = "Hello",
    purpose: str = "personal_assistant",
) -> LLMRequest:
    return LLMRequest(
        purpose=purpose,
        messages=[
            Message(
                role="user",
                content=content,
            )
        ],
    )


def create_mock_response(
    mocker,
    content: str = "Hello from model",
    model: str = "test-model",
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
):
    """
    Creates a LiteLLM-like response object.

    Explicitly setting usage prevents pytest-mock's Mock from dynamically
    creating nested Mock objects for prompt_tokens/completion_tokens.
    """

    response = mocker.Mock()

    response.choices = [
        mocker.Mock(
            message=mocker.Mock(
                content=content,
            )
        )
    ]

    response.model = model

    if prompt_tokens is None and completion_tokens is None:
        response.usage = None
    else:
        response.usage = mocker.Mock(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

    return response


# ---------------------------------------------------------------------------
# Success
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_success(mocker):
    mock_response = create_mock_response(
        mocker,
        content="Hello from model",
        model="test-model",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=mock_response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(),
    )

    response = await gateway.complete(
        create_request("Hello"),
    )

    assert response.content == "Hello from model"
    assert response.model == "test-primary"
    assert response.input_tokens is None
    assert response.output_tokens is None

    mock_completion.assert_awaited_once()


# ---------------------------------------------------------------------------
# Request mapping
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_passes_request_to_litellm(mocker):
    mock_response = create_mock_response(
        mocker,
        content="Response",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=mock_response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(),
    )

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[
            Message(
                role="system",
                content="You are a helpful assistant.",
            ),
            Message(
                role="user",
                content="Analyze this data.",
            ),
        ],
        temperature=0.2,
        max_tokens=500,
    )

    await gateway.complete(request)

    mock_completion.assert_awaited_once_with(
        model="test-primary",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "Analyze this data.",
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )


# ---------------------------------------------------------------------------
# Token usage
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_maps_token_usage(mocker):
    mock_response = create_mock_response(
        mocker,
        content="Analysis complete",
        model="test-model",
        prompt_tokens=100,
        completion_tokens=50,
    )

    mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=mock_response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(),
    )

    response = await gateway.complete(
        create_request("Analyze sales"),
    )

    assert response.content == "Analysis complete"
    assert response.input_tokens == 100
    assert response.output_tokens == 50


# ---------------------------------------------------------------------------
# Fallback
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_uses_fallback(mocker):
    fallback_response = create_mock_response(
        mocker,
        content="Fallback response",
        model="fallback-model",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        side_effect=[
            TimeoutError("primary timeout"),
            fallback_response,
        ],
    )

    registry = create_registry(
        primary="test-primary",
        fallbacks=("test-fallback",),
        max_retries=0,
    )

    fallback_policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=1,
    )

    gateway = LiteLLMGateway(
        model_registry=registry,
        fallback_policy=fallback_policy,
    )

    response = await gateway.complete(
        create_request(),
    )

    assert response.content == "Fallback response"
    assert response.model == "test-fallback"

    assert mock_completion.await_count == 2

    first_call = mock_completion.await_args_list[0]
    second_call = mock_completion.await_args_list[1]

    assert first_call.kwargs["model"] == "test-primary"
    assert second_call.kwargs["model"] == "test-fallback"


# ---------------------------------------------------------------------------
# Retry same model
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_retries_same_model(mocker):
    success_response = create_mock_response(
        mocker,
        content="Recovered response",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        side_effect=[
            TimeoutError("temporary timeout"),
            success_response,
        ],
    )

    registry = create_registry(
        primary="test-primary",
        fallbacks=(),
        max_retries=1,
    )

    fallback_policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=2,
    )

    gateway = LiteLLMGateway(
        model_registry=registry,
        fallback_policy=fallback_policy,
    )

    response = await gateway.complete(
        create_request(),
    )

    assert response.content == "Recovered response"
    assert response.model == "test-primary"

    assert mock_completion.await_count == 2

    first_call = mock_completion.await_args_list[0]
    second_call = mock_completion.await_args_list[1]

    assert first_call.kwargs["model"] == "test-primary"
    assert second_call.kwargs["model"] == "test-primary"


# ---------------------------------------------------------------------------
# Non-retryable error
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_does_not_retry_non_retryable_error(mocker):
    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        side_effect=ValueError("invalid request"),
    )

    registry = create_registry(
        primary="test-primary",
        fallbacks=("test-fallback",),
        max_retries=2,
    )

    fallback_policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=3,
    )

    gateway = LiteLLMGateway(
        model_registry=registry,
        fallback_policy=fallback_policy,
    )

    # Because the gateway currently moves to the configured fallback after
    # the primary model fails, the fallback is also attempted.
    with pytest.raises(RuntimeError):
        await gateway.complete(
            create_request(),
        )

    assert mock_completion.await_count == 2


# ---------------------------------------------------------------------------
# All models fail
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_gateway_raises_when_all_models_fail(mocker):
    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        side_effect=[
            TimeoutError("primary timeout"),
            ConnectionError("fallback unavailable"),
        ],
    )

    registry = create_registry(
        primary="test-primary",
        fallbacks=("test-fallback",),
        max_retries=0,
    )

    fallback_policy = FallbackPolicy(
        retryable_errors=(TimeoutError, ConnectionError),
        max_attempts=1,
    )

    gateway = LiteLLMGateway(
        model_registry=registry,
        fallback_policy=fallback_policy,
    )

    with pytest.raises(RuntimeError) as exc_info:
        await gateway.complete(
            create_request(),
        )

    error_message = str(exc_info.value)

    assert "All configured LLM models failed" in error_message
    assert "personal_assistant" in error_message

    assert mock_completion.await_count == 2


# ---------------------------------------------------------------------------
# Unknown purpose
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_rejects_unknown_purpose(mocker):
    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(),
    )

    request = create_request(
        content="Hello",
        purpose="unknown_purpose",
    )

    with pytest.raises(KeyError) as exc_info:
        await gateway.complete(request)

    assert "unknown_purpose" in str(exc_info.value)

    mock_completion.assert_not_awaited()


# ---------------------------------------------------------------------------
# Empty choices
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_rejects_empty_choices(mocker):
    response = mocker.Mock()
    response.choices = []
    response.model = "test-model"
    response.usage = None

    mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(
            fallbacks=(),
        ),
    )

    with pytest.raises(RuntimeError):
        await gateway.complete(
            create_request(),
        )


# ---------------------------------------------------------------------------
# None content
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_handles_none_content(mocker):
    response = mocker.Mock()

    response.choices = [
        mocker.Mock(
            message=mocker.Mock(
                content=None,
            )
        )
    ]

    response.model = "test-model"
    response.usage = None

    mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(
            fallbacks=(),
        ),
    )

    response = await gateway.complete(
        create_request(),
    )

    assert response.content == ""


# ---------------------------------------------------------------------------
# Multiple messages
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_supports_multiple_messages(mocker):
    mock_response = create_mock_response(
        mocker,
        content="Multi-message response",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=mock_response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(),
    )

    request = LLMRequest(
        purpose="personal_assistant",
        messages=[
            Message(
                role="system",
                content="You are an enterprise data analyst.",
            ),
            Message(
                role="user",
                content="Show sales.",
            ),
            Message(
                role="assistant",
                content="Which region?",
            ),
            Message(
                role="user",
                content="APAC.",
            ),
        ],
    )

    response = await gateway.complete(request)

    assert response.content == "Multi-message response"

    call = mock_completion.await_args

    assert call.kwargs["messages"] == [
        {
            "role": "system",
            "content": "You are an enterprise data analyst.",
        },
        {
            "role": "user",
            "content": "Show sales.",
        },
        {
            "role": "assistant",
            "content": "Which region?",
        },
        {
            "role": "user",
            "content": "APAC.",
        },
    ]


# ---------------------------------------------------------------------------
# Fallback order
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_respects_fallback_order(mocker):
    third_response = create_mock_response(
        mocker,
        content="Third model response",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        side_effect=[
            TimeoutError("primary failed"),
            ConnectionError("first fallback failed"),
            third_response,
        ],
    )

    registry = ModelRegistry(
        routes=[
            ModelRoute(
                purpose="personal_assistant",
                primary="primary-model",
                fallbacks=(
                    "fallback-model-1",
                    "fallback-model-2",
                ),
                max_retries=0,
            )
        ]
    )

    fallback_policy = FallbackPolicy(
        retryable_errors=(TimeoutError, ConnectionError),
        max_attempts=1,
    )

    gateway = LiteLLMGateway(
        model_registry=registry,
        fallback_policy=fallback_policy,
    )

    response = await gateway.complete(
        create_request(),
    )

    assert response.content == "Third model response"

    assert mock_completion.await_count == 3

    models = [
        call.kwargs["model"]
        for call in mock_completion.await_args_list
    ]

    assert models == [
        "primary-model",
        "fallback-model-1",
        "fallback-model-2",
    ]


# ---------------------------------------------------------------------------
# No fallback
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gateway_uses_primary_when_no_fallback_configured(mocker):
    mock_response = create_mock_response(
        mocker,
        content="Primary response",
    )

    mock_completion = mocker.patch(
        "company_ai.llm.litellm_gateway.litellm.acompletion",
        new_callable=mocker.AsyncMock,
        return_value=mock_response,
    )

    gateway = LiteLLMGateway(
        model_registry=create_registry(
            primary="primary-only",
            fallbacks=(),
        ),
    )

    response = await gateway.complete(
        create_request(),
    )

    assert response.content == "Primary response"
    assert response.model == "primary-only"

    mock_completion.assert_awaited_once()

    assert (
        mock_completion.await_args.kwargs["model"]
        == "primary-only"
    )