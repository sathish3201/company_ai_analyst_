import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.rag.capabilities.ingest import (
    RAGIngestionCapability,
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
from company_ai.rag.vectorstore.in_memory import (
    InMemoryVectorStore,
)


@pytest.mark.asyncio
async def test_ingestion_capability(
    tmp_path
):

    file = tmp_path / "policy.md"

    file.write_text(
        "Company revenue policy",
        encoding="utf-8",
    )

    capability = RAGIngestionCapability(
        loader=TextDocumentLoader(),
        chunker=SimpleTextChunker(
            chunk_size=100
        ),
        embeddings=(
            DeterministicEmbeddingService()
        ),
        vector_store=InMemoryVectorStore(),
    )

    result = await capability.execute(
        CapabilityRequest(
            capability_id="rag.ingest",
            input={
                "source": str(file)
            },
        )
    )

    assert result.success is True
    assert result.output["documents"] == 1
    assert result.output["chunks"] == 1