from company_ai.llm.model_registry import ModelRegistry, ModelRoute


class ModelRouter:
    """
    Resolves a logical model purpose to its configured model route.

    The router does not call the LLM.
    It only performs model-route selection.
    """

    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry

    def route(self, purpose: str) -> ModelRoute:
        """
        Return the configured route for a logical purpose.
        """
        return self._registry.get(purpose)

    def has_route(self, purpose: str) -> bool:
        """
        Check whether a route exists for the given purpose.
        """
        return self._registry.has(purpose)