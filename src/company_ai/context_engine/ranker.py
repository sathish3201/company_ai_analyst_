from company_ai.models.context import ContextItem


class ContextRanker:

    def rank(
        self,
        items: list[ContextItem],
    ) -> list[ContextItem]:

        return sorted(
            items,
            key=lambda item: item.relevance,
            reverse=True,
        )