from company_ai.config.settings import get_settings
from company_ai.llm.litellm_gateway import LiteLLMGateway
from company_ai.llm.model_registry import ModelRegistry
from company_ai.llm.router import ModelRouter


class ApplicationContainer:

    def __init__(self):
        self.settings = get_settings()

        self.model_registry = ModelRegistry(
            routes=[]
        )

        self.model_router = ModelRouter(
            self.model_registry
        )

        self.llm_gateway = LiteLLMGateway(
            router=self.model_router
        )