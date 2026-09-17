from company_ai.contracts.context import ContextProviderPort
from company_ai.models.context import (
    ContextBundle,
    ContextItem,
)


class MemoryContextProvider(ContextProviderPort):

    def __init__(
        self,
        memories: list[str] | None = None,
    ) -> None:
        self._memories = memories or []

    async def provide(
        self,
        query: str,
    ) -> ContextBundle:

        if not self._memories:
            return ContextBundle()

        return ContextBundle(
            items=[
                ContextItem(
                    source="memory",
                    content=memory,
                    relevance=0.7,
                )
                for memory in self._memories
            ]
        )