from abc import ABC, abstractmethod

from company_ai.models.assistant import (
    AssistantRequest,
    AssistantResponse,
)


class PersonalAssistantPort(ABC):

    @abstractmethod
    async def handle(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:
        raise NotImplementedError