from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRoute:
    purpose: str
    primary: str
    fallbacks: tuple[str, ...] = ()
    max_retries: int = 2
    timeout_seconds: int = 60


class ModelRegistry:
    def __init__(self, routes: list[ModelRoute]) -> None:
        self._routes = {
            route.purpose: route
            for route in routes
        }

    def get(self, purpose: str) -> ModelRoute:
        try:
            return self._routes[purpose]
        except KeyError as exc:
            raise KeyError(
                f"No model route configured for: {purpose}"
            ) from exc

    def has(self, purpose: str) -> bool:
        return purpose in self._routes

    def all(self) -> tuple[ModelRoute, ...]:
        return tuple(self._routes.values())