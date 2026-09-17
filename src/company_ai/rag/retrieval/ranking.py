from company_ai.rag.models import (
    RetrievedDocument,
)


class EvidenceRanker:

    def rank(
        self,
        documents: list[RetrievedDocument],
        top_k: int,
    ) -> list[RetrievedDocument]:

        ranked = sorted(
            documents,
            key=lambda item: item.score,
            reverse=True,
        )

        return ranked[:top_k]