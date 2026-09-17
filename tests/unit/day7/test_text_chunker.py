from company_ai.rag.chunking.text_chunker import (
    SimpleTextChunker,
)
from company_ai.rag.models import (
    Document,
)


def test_chunking():

    document = Document(
        document_id="doc1",
        content="a" * 250,
        source="test.txt",
    )

    chunker = SimpleTextChunker(
        chunk_size=100,
        overlap=20,
    )

    chunks = chunker.split(document)

    assert len(chunks) == 3
    assert chunks[0].content == "a" * 100


def test_chunk_metadata():

    document = Document(
        document_id="doc1",
        content="hello world",
        source="test.txt",
        metadata={
            "department": "finance"
        },
    )

    chunks = SimpleTextChunker(
        chunk_size=100
    ).split(document)

    assert (
        chunks[0].metadata["department"]
        == "finance"
    )