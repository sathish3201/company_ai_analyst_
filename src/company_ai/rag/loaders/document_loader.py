from pathlib import Path

from company_ai.rag.contracts import (
    DocumentLoaderPort,
)
from company_ai.rag.exceptions import (
    DocumentLoadError,
)
from company_ai.rag.models import (
    Document,
    DocumentType,
)


class TextDocumentLoader(
    DocumentLoaderPort
):

    SUPPORTED_EXTENSIONS = {
        ".txt": DocumentType.TEXT,
        ".md": DocumentType.MARKDOWN,
    }

    def load(
        self,
        source: str,
    ) -> list[Document]:

        path = Path(source)

        if not path.exists():
            raise DocumentLoadError(
                f"Document does not exist: {source}"
            )

        if not path.is_file():
            raise DocumentLoadError(
                f"Source is not a file: {source}"
            )

        document_type = (
            self.SUPPORTED_EXTENSIONS.get(
                path.suffix.lower()
            )
        )

        if document_type is None:
            raise DocumentLoadError(
                "Unsupported document type: "
                f"{path.suffix}"
            )

        try:
            content = path.read_text(
                encoding="utf-8"
            )
        except OSError as exc:
            raise DocumentLoadError(
                f"Failed to read document: {source}"
            ) from exc

        return [
            Document(
                document_id=path.stem,
                content=content,
                source=str(path),
                document_type=document_type,
                metadata={
                    "filename": path.name,
                    "extension": path.suffix,
                },
            )
        ]