from company_ai.llm.model_registry import (
    ModelRegistry,
    ModelRoute,
)


class ModelRouter:

    def __init__(self, registry: ModelRegistry):
        self.registry = registry

    def route(self, purpose: str) -> ModelRoute:
        return self.registry.get(purpose)