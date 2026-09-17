class RAGError(Exception):
    """Base RAG exception."""


class DocumentLoadError(RAGError):
    """Document loading failed."""


class ChunkingError(RAGError):
    """Document chunking failed."""


class EmbeddingError(RAGError):
    """Embedding generation failed."""


class VectorStoreError(RAGError):
    """Vector-store operation failed."""


class RetrievalError(RAGError):
    """Retrieval failed."""