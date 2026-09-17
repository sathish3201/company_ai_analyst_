import pytest

from company_ai.rag.embeddings.embedding_service import (
    DeterministicEmbeddingService,
)


@pytest.mark.asyncio
async def test_embedding_dimensions():

    service = DeterministicEmbeddingService(
        dimensions=16
    )

    result = await service.embed(
        ["hello"]
    )

    assert len(result) == 1
    assert len(result[0]) == 16


@pytest.mark.asyncio
async def test_embedding_is_deterministic():

    service = DeterministicEmbeddingService(
        dimensions=16
    )

    first = await service.embed(
        ["hello"]
    )

    second = await service.embed(
        ["hello"]
    )

    assert first == second