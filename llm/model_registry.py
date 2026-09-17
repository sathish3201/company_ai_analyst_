from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRoute:
    purpose: str
    primary: str
    fallbacks: tuple[str, ...] = ()
    max_retries: int = 2


class ModelRegistry:

    def __init__(self, routes: list[ModelRoute]):
        self._routes = {
            route.purpose: route
            for route in routes
        }

    def get(self, purpose: str) -> ModelRoute:
        if purpose not in self._routes:
            raise KeyError(
                f"No model route configured for: {purpose}"
            )

        return self._routes[purpose]