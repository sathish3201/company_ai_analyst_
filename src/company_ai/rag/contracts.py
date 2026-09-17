from abc import ABC, abstractmethod
from typing import Any

from company_ai.rag.models import (
    Document,
    DocumentChunk,
    EmbeddedChunk,
    RetrievalRequest,
    RetrievalResult,
)


class DocumentLoaderPort(ABC):

    @abstractmethod
    def load(
        self,
        source: str,
    ) -> list[Document]:
        raise NotImplementedError


class TextChunkerPort(ABC):

    @abstractmethod
    def split(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        raise NotImplementedError


class EmbeddingPort(ABC):

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        raise NotImplementedError


class VectorStorePort(ABC):

    @abstractmethod
    async def add(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        raise NotImplementedError


class RetrieverPort(ABC):

    @abstractmethod
    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        raise NotImplementedError


class ContextCompressorPort(ABC):

    @abstractmethod
    def compress(
        self,
        query: str,
        documents: list[Any],
    ) -> str:
        raise NotImplementedError