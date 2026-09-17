from company_ai.contracts.llm import (
    LLMGatewayPort,
    LLMRequest,
    Message,
)
from company_ai.models.context import IntentType


class IntentAnalyzer:

    def __init__(
        self,
        llm: LLMGatewayPort,
    ) -> None:
        self._llm = llm

    async def analyze(
        self,
        message: str,
    ) -> IntentType:

        request = LLMRequest(
            purpose="personal_assistant",
            messages=[
                Message(
                    role="system",
                    content=(
                        "Classify the user request into exactly "
                        "one category:\n"
                        "general\n"
                        "data_analysis\n"
                        "rag\n"
                        "task_execution\n"
                        "system\n"
                        "unknown\n\n"
                        "Return only the category name."
                    ),
                ),
                Message(
                    role="user",
                    content=message,
                ),
            ],
            temperature=0.0,
        )

        response = await self._llm.complete(
            request
        )

        value = response.content.strip().lower()

        try:
            return IntentType(value)
        except ValueError:
            return IntentType.UNKNOWN