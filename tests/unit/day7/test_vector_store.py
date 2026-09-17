import pytest

from company_ai.rag.embeddings.embedding_service import (
    DeterministicEmbeddingService,
)
from company_ai.rag.models import (
    DocumentChunk,
    EmbeddedChunk,
    RetrievalRequest,
)
from company_ai.rag.vectorstore.in_memory import (
    InMemoryVectorStore,
)


@pytest.mark.asyncio
async def test_vector_store_search():

    embeddings = (
        DeterministicEmbeddingService(
            dimensions=16
        )
    )

    values = await embeddings.embed(
        ["finance revenue"]
    )

    store = InMemoryVectorStore()

    await store.add(
        [
            EmbeddedChunk(
                chunk=DocumentChunk(
                    chunk_id="1",
                    document_id="doc1",
                    content="finance revenue",
                ),
                embedding=values[0],
            )
        ]
    )

    result = await store.search(
        RetrievalRequest(
            query="finance revenue",
            filters={
                "_query_embedding": values[0]
            },
        )
    )

    assert len(result.documents) == 1
    assert result.documents[0].score > 0