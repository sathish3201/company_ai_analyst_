from typing import Any

import litellm

from company_ai.contracts.llm import (
    LLMGatewayPort,
    LLMRequest,
    LLMResponse,
)
from company_ai.core.exceptions import LLMError
from company_ai.llm.router import ModelRouter


class LiteLLMGateway(LLMGatewayPort):

    def __init__(self, router: ModelRouter):
        self.router = router

    async def complete(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        route = self.router.route(request.purpose)

        models = (
            route.primary,
            *route.fallbacks,
        )

        last_error: Exception | None = None

        for model in models:

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

                usage: Any = getattr(
                    response,
                    "usage",
                    None,
                )

                return LLMResponse(
                    content=response.choices[0].message.content,
                    model=model,
                    input_tokens=getattr(
                        usage,
                        "prompt_tokens",
                        None,
                    ),
                    output_tokens=getattr(
                        usage,
                        "completion_tokens",
                        None,
                    ),
                    metadata=request.metadata,
                )

            except Exception as exc:
                last_error = exc

        raise LLMError(
            f"All configured models failed: {last_error}"
        ) from last_error