from typing import Any

from company_ai.contracts.agent import (
    AgentRuntimePort,
)
from company_ai.models.agent import (
    AgentResult,
    AgentStatus,
)


class DeepAgentRuntime(
    AgentRuntimePort
):

    def __init__(
        self,
        graph: Any,
    ) -> None:

        self._graph = graph

    async def run(
        self,
        goal: str,
    ) -> AgentResult:

        if not goal.strip():
            raise ValueError(
                "Agent goal cannot be empty"
            )

        state = await self._graph.ainvoke(
            {
                "goal": goal,
                "iteration": 0,
                "worker_results": [],
            }
        )

        worker_results = state.get(
            "worker_results",
            [],
        )

        return AgentResult(
            success=True,
            result=state.get(
                "final_result"
            ),
            status=AgentStatus.COMPLETED,
            iterations=state.get(
                "iteration",
                0,
            ),
            completed_tasks=len(
                worker_results
            ),
            failed_tasks=0,
        )