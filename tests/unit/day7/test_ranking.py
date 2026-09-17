from company_ai.rag.models import (
    DocumentChunk,
    RetrievedDocument,
)
from company_ai.rag.retrieval.ranking import (
    EvidenceRanker,
)


def test_ranker():

    documents = [
        RetrievedDocument(
            chunk=DocumentChunk(
                chunk_id="1",
                document_id="doc",
                content="low",
            ),
            score=0.2,
        ),
        RetrievedDocument(
            chunk=DocumentChunk(
                chunk_id="2",
                document_id="doc",
                content="high",
            ),
            score=0.9,
        ),
    ]

    result = EvidenceRanker().rank(
        documents,
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].score == 0.9