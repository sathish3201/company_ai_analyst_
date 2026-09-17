from pathlib import Path

import pytest

from company_ai.rag.exceptions import (
    DocumentLoadError,
)
from company_ai.rag.loaders.document_loader import (
    TextDocumentLoader,
)


def test_load_markdown(tmp_path: Path):

    file = tmp_path / "policy.md"

    file.write_text(
        "# Policy\nRevenue policy",
        encoding="utf-8",
    )

    documents = TextDocumentLoader().load(
        str(file)
    )

    assert len(documents) == 1
    assert documents[0].content.startswith(
        "# Policy"
    )


def test_missing_file():

    loader = TextDocumentLoader()

    with pytest.raises(DocumentLoadError):
        loader.load(
            "/does/not/exist.md"
        )