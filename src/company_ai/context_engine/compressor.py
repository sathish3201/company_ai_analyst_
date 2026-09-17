from company_ai.models.context import ContextItem


class ContextCompressor:

    def compress(
        self,
        items: list[ContextItem],
    ) -> list[ContextItem]:

        """
        Day-2 baseline implementation.

        Real semantic compression will be added later.
        We keep this as a separate component so the ContextEngine
        does not depend on a particular compression strategy.
        """

        return items