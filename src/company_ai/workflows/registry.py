from typing import Any, Callable

from company_ai.workflows.contracts import WorkflowRegistryPort


class WorkflowNodeRegistry(WorkflowRegistryPort):
    """
    Runtime registry for workflow node handlers.

    The workflow definition only specifies the logical node type.
    The registry maps that type to executable behavior.
    """

    def __init__(self) -> None:
        self._handlers: dict[
            str,
            Callable[..., Any],
        ] = {}

    def register(
        self,
        node_type: str,
        handler: Callable[..., Any],
    ) -> None:
        if node_type in self._handlers:
            raise ValueError(
                f"Workflow node type already registered: {node_type}"
            )

        self._handlers[node_type] = handler

    def unregister(
        self,
        node_type: str,
    ) -> None:
        self._handlers.pop(node_type, None)

    def get(
        self,
        node_type: str,
    ) -> Callable[..., Any]:
        try:
            return self._handlers[node_type]
        except KeyError as exc:
            raise KeyError(
                f"No workflow handler registered for: {node_type}"
            ) from exc

    def has(
        self,
        node_type: str,
    ) -> bool:
        return node_type in self._handlers

    def names(self) -> tuple[str, ...]:
        return tuple(self._handlers.keys())

    def all(self) -> dict[str, Callable[..., Any]]:
        return dict(self._handlers)