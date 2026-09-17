from company_ai.capabilities.contracts import (
    CapabilityPort,
)
from company_ai.capabilities.decorators import (
    capability,
)
from company_ai.capabilities.models import (
    CapabilityRequest,
    CapabilityResult,
    CapabilityType,
)
from company_ai.rag.contracts import (
    RetrieverPort,
)
from company_ai.rag.models import (
    RetrievalRequest,
)
from company_ai.rag.retrieval.compressor import (
    EvidenceContextCompressor,
)
from company_ai.rag.retrieval.ranking import (
    EvidenceRanker,
)


@capability(
    capability_id="rag.retrieve",
    name="RAG Retrieval",
    capability_type=CapabilityType.RETRIEVER,
    version="1.0",
    description=(
        "Retrieve and rank relevant "
        "enterprise knowledge."
    ),
    tags=[
        "rag",
        "retrieval",
        "semantic-search",
        "evidence",
    ],
)
class RAGRetrievalCapability(
    CapabilityPort
):

    def __init__(
        self,
        retriever: RetrieverPort,
        ranker: EvidenceRanker,
        compressor: EvidenceContextCompressor,
    ) -> None:

        self._retriever = retriever
        self._ranker = ranker
        self._compressor = compressor

    @property
    def metadata(self):
        return self.__capability_metadata__

    async def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:

        try:

            query = request.input["query"]

            top_k = request.input.get(
                "top_k",
                5,
            )

            retrieval = await self._retriever.retrieve(
                RetrievalRequest(
                    query=query,
                    top_k=top_k,
                    filters=request.input.get(
                        "filters",
                        {},
                    ),
                )
            )

            ranked = self._ranker.rank(
                retrieval.documents,
                top_k=top_k,
            )

            context = self._compressor.compress(
                query=query,
                documents=ranked,
            )

            return CapabilityResult(
                success=True,
                capability_id="rag.retrieve",
                output={
                    "query": query,
                    "evidence": [
                        item.model_dump()
                        for item in ranked
                    ],
                    "context": context,
                },
            )

        except Exception as exc:

            return CapabilityResult(
                success=False,
                capability_id="rag.retrieve",
                error=str(exc),
            )