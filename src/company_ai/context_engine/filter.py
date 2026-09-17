from company_ai.models.context import ContextItem


class ContextFilter:

    def filter(
        self,
        items: list[ContextItem],
        max_items: int = 10,
    ) -> list[ContextItem]:

        if max_items <= 0:
            return []

        return items[:max_items]