from abc import ABC, abstractmethod

from company_ai.models.context import ContextBundle


class ContextProviderPort(ABC):

    @abstractmethod
    async def provide(
        self,
        query: str,
    ) -> ContextBundle:
        raise NotImplementedError


class ContextEnginePort(ABC):

    @abstractmethod
    async def build(
        self,
        query: str,
    ) -> ContextBundle:
        raise NotImplementedError