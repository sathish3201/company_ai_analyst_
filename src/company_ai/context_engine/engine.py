from company_ai.contracts.context import (
    ContextEnginePort,
    ContextProviderPort,
)
from company_ai.context_engine.assembler import (
    ContextAssembler,
)
from company_ai.context_engine.compressor import (
    ContextCompressor,
)
from company_ai.context_engine.filter import (
    ContextFilter,
)
from company_ai.context_engine.ranker import (
    ContextRanker,
)
from company_ai.models.context import ContextBundle


class ContextEngine(ContextEnginePort):

    def __init__(
        self,
        providers: list[ContextProviderPort],
        ranker: ContextRanker,
        context_filter: ContextFilter,
        compressor: ContextCompressor,
        assembler: ContextAssembler,
    ) -> None:

        self._providers = providers
        self._ranker = ranker
        self._filter = context_filter
        self._compressor = compressor
        self._assembler = assembler

    async def build(
        self,
        query: str,
    ) -> ContextBundle:

        items = []

        # 1. Collect
        for provider in self._providers:
            bundle = await provider.provide(query)
            items.extend(bundle.items)

        # 2. Rank
        ranked = self._ranker.rank(items)

        # 3. Filter
        filtered = self._filter.filter(ranked)

        # 4. Compress
        compressed = self._compressor.compress(
            filtered
        )

        # 5. Assemble
        return self._assembler.assemble(
            compressed
        )