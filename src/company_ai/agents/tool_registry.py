from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError


class ToolRegistry:

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:

        self._tools.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> Tool:

        try:
            return self._tools[name]

        except KeyError as exc:

            raise KeyError(
                f"Tool not registered: {name}"
            ) from exc

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._tools.keys()
        )

    def all(
        self,
    ) -> tuple[Tool, ...]:

        return tuple(
            self._tools.values()
        )