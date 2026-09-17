from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class LLMRequest(BaseModel):
    purpose: str
    messages: list[Message]

    temperature: float = 0.0
    max_tokens: int | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class LLMResponse(BaseModel):
    content: str
    model: str

    input_tokens: int | None = None
    output_tokens: int | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class LLMGatewayPort(ABC):

    @abstractmethod
    async def complete(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        ...