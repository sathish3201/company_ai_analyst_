from company_ai.models.context import ContextBundle, ContextItem


class ContextAssembler:

    def assemble(
        self,
        items: list[ContextItem],
    ) -> ContextBundle:

        return ContextBundle(
            items=items
        )