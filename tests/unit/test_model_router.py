from company_ai.llm.model_registry import (
    ModelRegistry,
    ModelRoute,
)

from company_ai.llm.router import ModelRouter


def test_router_returns_configured_route():

    registry = ModelRegistry(
        [
            ModelRoute(
                purpose="fast",
                primary="ollama/qwen2.5-coder:1.5b",
            )
        ]
    )

    router = ModelRouter(registry)

    route = router.route("fast")

    assert route.primary == "ollama/qwen2.5-coder:1.5b"