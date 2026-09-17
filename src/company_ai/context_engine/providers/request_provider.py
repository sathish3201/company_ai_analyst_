from company_ai.contracts.context import ContextProviderPort
from company_ai.models.context import (
    ContextBundle,
    ContextItem,
)


class RequestContextProvider(ContextProviderPort):

    async def provide(
        self,
        query: str,
    ) -> ContextBundle:

        return ContextBundle(
            items=[
                ContextItem(
                    source="request",
                    content=query,
                    relevance=1.0,
                )
            ]
        )