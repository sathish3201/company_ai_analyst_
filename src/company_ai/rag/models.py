from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"
    CSV = "csv"
    HTML = "html"


class Document(BaseModel):
    document_id: str
    content: str
    source: str
    document_type: DocumentType = DocumentType.TEXT
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EmbeddedChunk(BaseModel):
    chunk: DocumentChunk
    embedding: list[float] = Field(
        default_factory=list
    )


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = Field(
        default=5,
        ge=1,
        le=100,
    )
    filters: dict[str, Any] = Field(
        default_factory=dict
    )


class RetrievedDocument(BaseModel):
    chunk: DocumentChunk
    score: float = 0.0


class RetrievalResult(BaseModel):
    query: str
    documents: list[RetrievedDocument] = Field(
        default_factory=list
    )


class RAGContext(BaseModel):
    query: str
    evidence: list[RetrievedDocument] = Field(
        default_factory=list
    )
    text: str = ""


class RAGResult(BaseModel):
    success: bool
    query: str
    context: RAGContext | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )