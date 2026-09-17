from company_ai.contracts.context import ContextProviderPort
from company_ai.models.context import (
    ContextBundle,
    ContextItem,
)


class UserContextProvider(ContextProviderPort):

    def __init__(
        self,
        user_context: str = "",
    ) -> None:
        self._user_context = user_context

    async def provide(
        self,
        query: str,
    ) -> ContextBundle:

        if not self._user_context:
            return ContextBundle()

        return ContextBundle(
            items=[
                ContextItem(
                    source="user",
                    content=self._user_context,
                    relevance=0.8,
                )
            ]
        )