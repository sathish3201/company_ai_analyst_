import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.rag.capabilities.retrieve import (
    RAGRetrievalCapability,
)
from company_ai.rag.embeddings.embedding_service import (
    DeterministicEmbeddingService,
)
from company_ai.rag.models import (
    DocumentChunk,
    EmbeddedChunk,
)
from company_ai.rag.retrieval.compressor import (
    EvidenceContextCompressor,
)
from company_ai.rag.retrieval.ranking import (
    EvidenceRanker,
)
from company_ai.rag.retrieval.retriever import (
    SemanticRetriever,
)
from company_ai.rag.vectorstore.in_memory import (
    InMemoryVectorStore,
)


@pytest.mark.asyncio
async def test_retrieval_capability():

    embeddings = (
        DeterministicEmbeddingService()
    )

    store = InMemoryVectorStore()

    vector = (
        await embeddings.embed(
            ["finance revenue"]
        )
    )[0]

    await store.add(
        [
            EmbeddedChunk(
                chunk=DocumentChunk(
                    chunk_id="1",
                    document_id="finance",
                    content=(
                        "Finance revenue "
                        "increased."
                    ),
                ),
                embedding=vector,
            )
        ]
    )

    capability = RAGRetrievalCapability(
        retriever=SemanticRetriever(
            embeddings,
            store,
        ),
        ranker=EvidenceRanker(),
        compressor=EvidenceContextCompressor(),
    )

    result = await capability.execute(
        CapabilityRequest(
            capability_id="rag.retrieve",
            input={
                "query": "finance revenue",
                "top_k": 1,
            },
        )
    )

    assert result.success is True
    assert len(
        result.output["evidence"]
    ) == 1

    assert (
        "Finance revenue"
        in result.output["context"]
    )