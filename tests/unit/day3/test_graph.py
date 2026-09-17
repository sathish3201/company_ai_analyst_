from company_ai.agents.graph import (
    DeepAgentGraph,
)
from company_ai.models.agent import (
    AgentTask,
)


class MockPlanner:

    async def create_plan(self, goal):

        raise NotImplementedError


class MockWorker:

    async def execute(
        self,
        task,
        context,
    ):

        return {
            "task": task.description
        }


class MockReducer:

    async def reduce(
        self,
        goal,
        results,
    ):

        return results


def create_graph():

    return DeepAgentGraph(
        planner=MockPlanner(),
        worker=MockWorker(),
        reducer=MockReducer(),
    )


def test_fanout_creates_send_objects():

    graph = create_graph()

    tasks = [
        AgentTask(
            task_id="1",
            description="Task one",
        ),
        AgentTask(
            task_id="2",
            description="Task two",
        ),
        AgentTask(
            task_id="3",
            description="Task three",
        ),
    ]

    state = {
        "goal": "Test goal",
        "tasks": tasks,
    }

    sends = graph.fanout(
        state
    )

    assert len(sends) == 3

    assert all(
        send.node == "worker"
        for send in sends
    )

import pytest

from company_ai.agents.graph import (
    DeepAgentGraph,
)
from company_ai.agents.runtime import (
    DeepAgentRuntime,
)
from company_ai.models.agent import (
    AgentPlan,
    AgentTask,
)


class GraphPlanner:

    async def create_plan(
        self,
        goal,
    ):

        return AgentPlan(
            goal=goal,
            tasks=[
                AgentTask(
                    task_id="1",
                    description="Collect sales",
                ),
                AgentTask(
                    task_id="2",
                    description="Analyze sales",
                ),
                AgentTask(
                    task_id="3",
                    description="Summarize sales",
                ),
            ],
        )


class GraphWorker:

    async def execute(
        self,
        task,
        context,
    ):

        return {
            "description": task.description,
            "success": True,
        }


class GraphReducer:

    async def reduce(
        self,
        goal,
        results,
    ):

        return {
            "goal": goal,
            "results": results,
        }


@pytest.mark.asyncio
async def test_graph_executes_parallel_tasks():

    graph_builder = DeepAgentGraph(
        planner=GraphPlanner(),
        worker=GraphWorker(),
        reducer=GraphReducer(),
    )

    graph = graph_builder.compile()

    runtime = DeepAgentRuntime(
        graph
    )

    result = await runtime.run(
        "Analyze company sales"
    )

    assert result.success is True

    assert result.completed_tasks == 3

    assert result.failed_tasks == 0

    assert result.result["goal"] == (
        "Analyze company sales"
    )

    assert len(
        result.result["results"]
    ) == 3