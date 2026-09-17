from company_ai.rag.models import (
    DocumentChunk,
    RetrievedDocument,
)
from company_ai.rag.retrieval.compressor import (
    EvidenceContextCompressor,
)


def test_compressor():

    documents = [
        RetrievedDocument(
            chunk=DocumentChunk(
                chunk_id="1",
                document_id="doc1",
                content="Revenue increased.",
                metadata={
                    "filename": "finance.md"
                },
            ),
            score=0.9,
        )
    ]

    result = EvidenceContextCompressor(
        max_characters=1000
    ).compress(
        query="revenue",
        documents=documents,
    )

    assert "Revenue increased." in result
    assert "finance.md" in result