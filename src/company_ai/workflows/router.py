from typing import Any, Callable


class WorkflowRouter:
    """
    Registry and execution layer for conditional workflow routers.
    """

    def __init__(
        self,
        routes: dict[
            str,
            Callable[[dict[str, Any]], str],
        ] | None = None,
    ) -> None:

        self._routes = routes or {}

    def register(
        self,
        name: str,
        router: Callable[[dict[str, Any]], str],
    ) -> None:

        if name in self._routes:
            raise ValueError(
                f"Router already registered: {name}"
            )

        self._routes[name] = router

    def unregister(
        self,
        name: str,
    ) -> None:

        self._routes.pop(name, None)

    def route(
        self,
        name: str,
        state: dict[str, Any],
    ) -> str:

        try:
            router = self._routes[name]
        except KeyError as exc:
            raise KeyError(
                f"No workflow router registered: {name}"
            ) from exc

        return router(state)

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._routes

    def names(self) -> tuple[str, ...]:
        return tuple(self._routes.keys())