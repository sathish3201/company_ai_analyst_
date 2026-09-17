from company_ai.rag.models import (
    RetrievedDocument,
)


class EvidenceContextCompressor:

    def __init__(
        self,
        max_characters: int = 6000,
    ) -> None:

        if max_characters <= 0:
            raise ValueError(
                "max_characters must be positive"
            )

        self._max_characters = max_characters

    def compress(
        self,
        query: str,
        documents: list[RetrievedDocument],
    ) -> str:

        sections = []
        current_size = 0

        for index, document in enumerate(
            documents,
            start=1,
        ):

            section = (
                f"[Evidence {index}]\n"
                f"Source: "
                f"{document.chunk.metadata.get('filename', document.chunk.document_id)}\n"
                f"Score: {document.score:.4f}\n"
                f"{document.chunk.content}\n"
            )

            if (
                current_size
                + len(section)
                > self._max_characters
            ):
                break

            sections.append(section)
            current_size += len(section)

        return "\n".join(sections)