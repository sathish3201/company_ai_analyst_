from abc import ABC, abstractmethod
from typing import Any

from company_ai.models.agent import (
    AgentPlan,
    AgentResult,
    AgentTask,
)


class PlannerPort(ABC):

    @abstractmethod
    async def create_plan(
        self,
        goal: str,
    ) -> AgentPlan:
        raise NotImplementedError


class WorkerPort(ABC):

    @abstractmethod
    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> Any:
        raise NotImplementedError


class ResultReducerPort(ABC):

    @abstractmethod
    async def reduce(
        self,
        goal: str,
        results: list[dict[str, Any]],
    ) -> Any:
        raise NotImplementedError


class AgentRuntimePort(ABC):

    @abstractmethod
    async def run(
        self,
        goal: str,
    ) -> AgentResult:
        raise NotImplementedError