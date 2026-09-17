from abc import ABC, abstractmethod
from typing import Any, Callable

from company_ai.workflows.models import WorkflowDefinition


class WorkflowValidatorPort(ABC):
    """
    Contract for workflow validation.
    """

    @abstractmethod
    def validate(
        self,
        workflow: WorkflowDefinition,
    ) -> None:
        raise NotImplementedError


class WorkflowRegistryPort(ABC):
    """
    Contract for dynamic node-handler registration.
    """

    @abstractmethod
    def register(
        self,
        node_type: str,
        handler: Callable[..., Any],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        node_type: str,
    ) -> Callable[..., Any]:
        raise NotImplementedError


class WorkflowBuilderPort(ABC):
    """
    Contract for converting workflow definitions
    into executable graphs.
    """

    @abstractmethod
    def build(
        self,
        workflow: WorkflowDefinition,
    ) -> Any:
        raise NotImplementedError


class WorkflowExecutorPort(ABC):
    """
    Contract for workflow execution.
    """

    @abstractmethod
    async def execute(
        self,
        workflow: WorkflowDefinition,
        initial_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError