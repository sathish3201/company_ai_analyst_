from company_ai.assistant.intent import IntentAnalyzer
from company_ai.contracts.assistant import (
    PersonalAssistantPort,
)
from company_ai.contracts.context import (
    ContextEnginePort,
)
from company_ai.models.assistant import (
    AssistantRequest,
    AssistantResponse,
)
from company_ai.models.context import IntentType


class PersonalAssistant(PersonalAssistantPort):

    def __init__(
        self,
        intent_analyzer: IntentAnalyzer,
        context_engine: ContextEnginePort,
    ) -> None:

        self._intent_analyzer = intent_analyzer
        self._context_engine = context_engine

    async def handle(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        # 1. Understand request
        intent = await self._intent_analyzer.analyze(
            request.message
        )

        # 2. Build dynamic context
        context = await self._context_engine.build(
            request.message
        )

        # 3. Decide whether Deep Agent is required
        requires_agent = intent in {
            IntentType.DATA_ANALYSIS,
            IntentType.RAG,
            IntentType.TASK_EXECUTION,
        }

        return AssistantResponse(
            answer="Request understood.",
            intent=intent.value,
            confidence=1.0,
            requires_agent=requires_agent,
            context_used=[
                item.source
                for item in context.items
            ],
        )