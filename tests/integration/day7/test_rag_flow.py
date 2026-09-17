import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.rag.capabilities.ingest import (
    RAGIngestionCapability,
)
from company_ai.rag.capabilities.retrieve import (
    RAGRetrievalCapability,
)
from company_ai.rag.chunking.text_chunker import (
    SimpleTextChunker,
)
from company_ai.rag.embeddings.embedding_service import (
    DeterministicEmbeddingService,
)
from company_ai.rag.loaders.document_loader import (
    TextDocumentLoader,
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
async def test_end_to_end_rag(
    tmp_path
):

    file = tmp_path / "company.md"

    file.write_text(
        """
        Company revenue increased by 20 percent.

        The finance department owns revenue
        reporting.

        Monthly revenue reports are generated
        by the finance team.
        """,
        encoding="utf-8",
    )

    embeddings = (
        DeterministicEmbeddingService(
            dimensions=32
        )
    )

    store = InMemoryVectorStore()

    ingestion = RAGIngestionCapability(
        loader=TextDocumentLoader(),
        chunker=SimpleTextChunker(
            chunk_size=150,
            overlap=20,
        ),
        embeddings=embeddings,
        vector_store=store,
    )

    ingest_result = (
        await ingestion.execute(
            CapabilityRequest(
                capability_id="rag.ingest",
                input={
                    "source": str(file)
                },
            )
        )
    )

    assert ingest_result.success is True

    retrieval = RAGRetrievalCapability(
        retriever=SemanticRetriever(
            embeddings=embeddings,
            vector_store=store,
        ),
        ranker=EvidenceRanker(),
        compressor=EvidenceContextCompressor(
            max_characters=5000
        ),
    )

    result = await retrieval.execute(
        CapabilityRequest(
            capability_id="rag.retrieve",
            input={
                "query": (
                    "Who owns revenue reporting?"
                ),
                "top_k": 2,
            },
        )
    )

    assert result.success is True
    assert result.output["evidence"]
    assert result.output["context"]