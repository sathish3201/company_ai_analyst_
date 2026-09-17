from typing import Any

from langgraph.graph import (
    END,
    START,
    StateGraph,
)
from langgraph.types import Send

from company_ai.agents.planner import (
    DeepAgentPlanner,
)
from company_ai.agents.reducer import (
    DeepAgentResultReducer,
)
from company_ai.agents.state import (
    DeepAgentState,
)
from company_ai.agents.worker import (
    DeepAgentWorker,
)


class DeepAgentGraph:

    def __init__(
        self,
        planner: DeepAgentPlanner,
        worker: DeepAgentWorker,
        reducer: DeepAgentResultReducer,
    ) -> None:

        self._planner = planner
        self._worker = worker
        self._reducer = reducer

    async def planner_node(
        self,
        state: DeepAgentState,
    ) -> dict[str, Any]:

        plan = await self._planner.create_plan(
            state["goal"]
        )

        return {
            "tasks": plan.tasks,
            "iteration": (
                state.get("iteration", 0) + 1
            ),
        }

    def fanout(
        self,
        state: DeepAgentState,
    ) -> list[Send]:

        tasks = state.get(
            "tasks",
            [],
        )

        return [
            Send(
                "worker",
                {
                    "goal": state["goal"],
                    "task": task,
                },
            )
            for task in tasks
        ]

    async def worker_node(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:

        task = state["task"]

        result = await self._worker.execute(
            task=task,
            context={
                "goal": state.get(
                    "goal",
                    "",
                ),
            },
        )

        return {
            "worker_results": [
                {
                    "task_id": task.task_id,
                    "task": task.description,
                    "result": result,
                }
            ]
        }

    async def reducer_node(
        self,
        state: DeepAgentState,
    ) -> dict[str, Any]:

        final_result = await self._reducer.reduce(
            goal=state["goal"],
            results=state.get(
                "worker_results",
                [],
            ),
        )

        return {
            "final_result": final_result
        }

    def compile(self):

        builder = StateGraph(
            DeepAgentState
        )

        builder.add_node(
            "planner",
            self.planner_node,
        )

        builder.add_node(
            "worker",
            self.worker_node,
        )

        builder.add_node(
            "reducer",
            self.reducer_node,
        )

        builder.add_edge(
            START,
            "planner",
        )

        builder.add_conditional_edges(
            "planner",
            self.fanout,
            ["worker"],
        )

        builder.add_edge(
            "worker",
            "reducer",
        )

        builder.add_edge(
            "reducer",
            END,
        )

        return builder.compile()