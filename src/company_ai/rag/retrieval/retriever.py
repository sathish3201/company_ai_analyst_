from company_ai.rag.contracts import (
    EmbeddingPort,
    RetrieverPort,
    VectorStorePort,
)
from company_ai.rag.models import (
    RetrievalRequest,
    RetrievalResult,
)


class SemanticRetriever(
    RetrieverPort
):

    def __init__(
        self,
        embeddings: EmbeddingPort,
        vector_store: VectorStorePort,
    ) -> None:

        self._embeddings = embeddings
        self._vector_store = vector_store

    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:

        query_embedding = (
            await self._embeddings.embed(
                [request.query]
            )
        )

        filters = {
            **request.filters,
            "_query_embedding": (
                query_embedding[0]
            ),
        }

        return await self._vector_store.search(
            RetrievalRequest(
                query=request.query,
                top_k=request.top_k,
                filters=filters,
            )
        )