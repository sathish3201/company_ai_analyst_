from abc import ABC, abstractmethod
from typing import Any


class SubAgent(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def run(
        self,
        task: str,
        context: dict[str, Any],
    ) -> Any:
        raise NotImplementedError


class SubAgentRegistry:

    def __init__(self) -> None:
        self._agents: dict[str, SubAgent] = {}

    def register(
        self,
        agent: SubAgent,
    ) -> None:

        if agent.name in self._agents:
            raise ValueError(
                f"Sub-agent already registered: "
                f"{agent.name}"
            )

        self._agents[agent.name] = agent

    def unregister(
        self,
        name: str,
    ) -> None:

        self._agents.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> SubAgent:

        try:
            return self._agents[name]

        except KeyError as exc:

            raise KeyError(
                f"Sub-agent not registered: {name}"
            ) from exc

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._agents

    def names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._agents.keys()
        )