import pytest

from company_ai.rag.embeddings.embedding_service import (
    DeterministicEmbeddingService,
)
from company_ai.rag.models import (
    DocumentChunk,
    EmbeddedChunk,
    RetrievalRequest,
)
from company_ai.rag.retrieval.retriever import (
    SemanticRetriever,
)
from company_ai.rag.vectorstore.in_memory import (
    InMemoryVectorStore,
)


@pytest.mark.asyncio
async def test_retriever():

    embeddings = (
        DeterministicEmbeddingService(
            dimensions=16
        )
    )

    store = InMemoryVectorStore()

    texts = [
        "finance revenue",
        "employee benefits",
    ]

    vectors = await embeddings.embed(texts)

    await store.add(
        [
            EmbeddedChunk(
                chunk=DocumentChunk(
                    chunk_id=str(index),
                    document_id="doc1",
                    content=text,
                ),
                embedding=vector,
            )
            for index, (text, vector)
            in enumerate(
                zip(texts, vectors)
            )
        ]
    )

    retriever = SemanticRetriever(
        embeddings=embeddings,
        vector_store=store,
    )

    result = await retriever.retrieve(
        RetrievalRequest(
            query="finance revenue",
            top_k=1,
        )
    )

    assert len(result.documents) == 1