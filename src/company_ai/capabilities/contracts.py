from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from company_ai.capabilities.models import (
    CapabilityMetadata,
    CapabilityRequest,
    CapabilityResult,
)


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class CapabilityPort(
    ABC,
    Generic[InputT, OutputT],
):
    """
    Base contract for every capability.
    """

    @property
    @abstractmethod
    def metadata(
        self,
    ) -> CapabilityMetadata:
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:
        raise NotImplementedError


class CapabilityRegistryPort(ABC):
    """
    Registry contract.
    """

    @abstractmethod
    def register(
        self,
        capability_class: type[CapabilityPort],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        capability_id: str,
    ) -> type[CapabilityPort]:
        raise NotImplementedError

    @abstractmethod
    def has(
        self,
        capability_id: str,
    ) -> bool:
        raise NotImplementedError


class CapabilityFactoryPort(ABC):
    """
    Factory contract.
    """

    @abstractmethod
    def create(
        self,
        capability_id: str,
        config: dict[str, Any] | None = None,
    ) -> CapabilityPort:
        raise NotImplementedError