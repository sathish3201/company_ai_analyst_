from company_ai.contracts.context import ContextProviderPort
from company_ai.models.context import (
    ContextBundle,
    ContextItem,
)


class EnterpriseContextProvider(ContextProviderPort):

    def __init__(
        self,
        enterprise_context: str = "",
    ) -> None:
        self._enterprise_context = enterprise_context

    async def provide(
        self,
        query: str,
    ) -> ContextBundle:

        if not self._enterprise_context:
            return ContextBundle()

        return ContextBundle(
            items=[
                ContextItem(
                    source="enterprise",
                    content=self._enterprise_context,
                    relevance=0.9,
                )
            ]
        )