from typing import Any

import litellm

from company_ai.contracts.llm import (
    LLMGatewayPort,
    LLMRequest,
    LLMResponse,
)
from company_ai.llm.fallback import FallbackPolicy
from company_ai.llm.model_registry import ModelRegistry


class LiteLLMGateway(LLMGatewayPort):
    """Application-level gateway around LiteLLM."""

    def __init__(
        self,
        model_registry: ModelRegistry,
        fallback_policy: FallbackPolicy | None = None,
    ) -> None:
        self.model_registry = model_registry

        self.fallback_policy = fallback_policy or FallbackPolicy(
            retryable_errors=(
                TimeoutError,
                ConnectionError,
            ),
            max_attempts=1,
        )

    async def complete(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        route = self.model_registry.get(request.purpose)

        models = (
            route.primary,
            *route.fallbacks,
        )

        last_error: Exception | None = None

        for model in models:

            try:
                return await self._complete_with_model(
                    model=model,
                    request=request,
                    max_attempts=route.max_retries + 1,
                )

            except Exception as exc:
                last_error = exc

                # Move to next model.
                continue

        raise RuntimeError(
            f"All configured LLM models failed "
            f"for purpose='{request.purpose}'"
        ) from last_error

    async def _complete_with_model(
        self,
        model: str,
        request: LLMRequest,
        max_attempts: int,
    ) -> LLMResponse:

        last_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):

            try:

                response = await litellm.acompletion(
                    model=model,
                    messages=[
                        message.model_dump()
                        for message in request.messages
                    ],
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )

                return self._to_llm_response(
                    response=response,
                    model=model,
                )

            except Exception as exc:

                last_error = exc

                if not self.fallback_policy.should_retry(
                    exc,
                    attempt,
                ):
                    raise

        assert last_error is not None
        raise last_error

    @staticmethod
    def _get_value(
        obj: Any,
        key: str,
        default: Any = None,
    ) -> Any:

        if obj is None:
            return default

        if isinstance(obj, dict):
            value = obj.get(key, default)

        else:
            value = getattr(obj, key, default)

        if value is Ellipsis:
            return default

        return value

    @classmethod
    def _to_llm_response(
        cls,
        response: Any,
        model: str,
    ) -> LLMResponse:

        choices = cls._get_value(
            response,
            "choices",
            [],
        )

        if not choices:
            raise ValueError(
                "LLM response contains no choices"
            )

        first_choice = choices[0]

        message = cls._get_value(
            first_choice,
            "message",
            {},
        )

        content = cls._get_value(
            message,
            "content",
            "",
        )

        usage = cls._get_value(
            response,
            "usage",
            None,
        )

        input_tokens = cls._get_value(
            usage,
            "prompt_tokens",
            None,
        )

        output_tokens = cls._get_value(
            usage,
            "completion_tokens",
            None,
        )

        return LLMResponse(
            content=content or "",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            metadata={},
        )