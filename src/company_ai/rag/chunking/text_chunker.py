from company_ai.rag.contracts import (
    TextChunkerPort,
)
from company_ai.rag.exceptions import (
    ChunkingError,
)
from company_ai.rag.models import (
    Document,
    DocumentChunk,
)


class SimpleTextChunker(
    TextChunkerPort
):

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int | None = None,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero"
            )

        # Default overlap is 10% of chunk size.
        if overlap is None:
            overlap = min(
                100,
                max(0, chunk_size // 10),
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative"
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self._chunk_size = chunk_size
        self._overlap = overlap

    def split(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        try:
            chunks = []

            start = 0
            index = 0
            content = document.content

            while start < len(content):

                end = min(
                    start + self._chunk_size,
                    len(content),
                )

                chunk_content = content[
                    start:end
                ]

                chunks.append(
                    DocumentChunk(
                        chunk_id=(
                            f"{document.document_id}"
                            f":chunk:{index}"
                        ),
                        document_id=(
                            document.document_id
                        ),
                        content=chunk_content,
                        metadata={
                            **document.metadata,
                            "chunk_index": index,
                        },
                    )
                )

                if end >= len(content):
                    break

                start = end - self._overlap
                index += 1

            return chunks

        except Exception as exc:
            raise ChunkingError(
                "Failed to split document"
            ) from exc