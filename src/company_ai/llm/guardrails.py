from abc import ABC, abstractmethod

from company_ai.contracts.llm import LLMRequest, LLMResponse


class GuardrailPort(ABC):

    @abstractmethod
    async def validate_input(
        self,
        request: LLMRequest,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def validate_output(
        self,
        request: LLMRequest,
        response: LLMResponse,
    ) -> None:
        raise NotImplementedError


class NoOpGuardrail(GuardrailPort):
    """
    Development/default guardrail implementation.

    It allows requests and responses without applying
    additional security policies.
    """

    async def validate_input(
        self,
        request: LLMRequest,
    ) -> None:
        return None

    async def validate_output(
        self,
        request: LLMRequest,
        response: LLMResponse,
    ) -> None:
        return None