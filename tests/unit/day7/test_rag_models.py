from company_ai.rag.models import (
    Document,
    DocumentChunk,
    DocumentType,
    RetrievalRequest,
)


def test_document():

    document = Document(
        document_id="doc1",
        content="Company policy",
        source="policy.md",
        document_type=DocumentType.MARKDOWN,
    )

    assert document.document_id == "doc1"


def test_document_chunk():

    chunk = DocumentChunk(
        chunk_id="doc1:chunk:0",
        document_id="doc1",
        content="Revenue policy",
    )

    assert chunk.document_id == "doc1"


def test_retrieval_request():

    request = RetrievalRequest(
        query="What is revenue?"
    )

    assert request.top_k == 5