from typing import Any

from company_ai.contracts.agent import (
    ResultReducerPort,
)


class DeepAgentResultReducer(
    ResultReducerPort
):

    async def reduce(
        self,
        goal: str,
        results: list[dict[str, Any]],
    ) -> Any:

        return {
            "goal": goal,
            "results": results,
            "total_results": len(results),
        }