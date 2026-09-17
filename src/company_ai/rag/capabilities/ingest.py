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
    DocumentLoaderPort,
    EmbeddingPort,
    TextChunkerPort,
    VectorStorePort,
)
from company_ai.rag.models import (
    EmbeddedChunk,
)


@capability(
    capability_id="rag.ingest",
    name="RAG Document Ingestion",
    capability_type=CapabilityType.RETRIEVER,
    version="1.0",
    description=(
        "Load, chunk, embed and index "
        "enterprise documents."
    ),
    tags=[
        "rag",
        "ingestion",
        "embedding",
        "indexing",
    ],
)
class RAGIngestionCapability(
    CapabilityPort
):

    def __init__(
        self,
        loader: DocumentLoaderPort,
        chunker: TextChunkerPort,
        embeddings: EmbeddingPort,
        vector_store: VectorStorePort,
    ) -> None:

        self._loader = loader
        self._chunker = chunker
        self._embeddings = embeddings
        self._vector_store = vector_store

    @property
    def metadata(self):
        return self.__capability_metadata__

    async def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:

        try:

            source = request.input["source"]

            documents = self._loader.load(
                source
            )

            chunks = []

            for document in documents:
                chunks.extend(
                    self._chunker.split(
                        document
                    )
                )

            embeddings = (
                await self._embeddings.embed(
                    [
                        chunk.content
                        for chunk in chunks
                    ]
                )
            )

            embedded_chunks = [
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=embedding,
                )
                for chunk, embedding in zip(
                    chunks,
                    embeddings,
                )
            ]

            await self._vector_store.add(
                embedded_chunks
            )

            return CapabilityResult(
                success=True,
                capability_id="rag.ingest",
                output={
                    "documents": len(documents),
                    "chunks": len(chunks),
                },
            )

        except Exception as exc:

            return CapabilityResult(
                success=False,
                capability_id="rag.ingest",
                error=str(exc),
            )