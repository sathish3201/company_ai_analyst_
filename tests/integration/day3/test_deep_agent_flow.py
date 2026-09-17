import pytest

from company_ai.agents.graph import (
    DeepAgentGraph,
)
from company_ai.agents.planner import (
    DeepAgentPlanner,
)
from company_ai.agents.reducer import (
    DeepAgentResultReducer,
)
from company_ai.agents.runtime import (
    DeepAgentRuntime,
)
from company_ai.agents.subagent_registry import (
    SubAgentRegistry,
)
from company_ai.agents.tool_registry import (
    ToolRegistry,
)
from company_ai.agents.worker import (
    DeepAgentWorker,
)
from company_ai.contracts.llm import (
    LLMResponse,
)


class MockLLM:

    async def complete(
        self,
        request,
    ):

        return LLMResponse(
            content=(
                '{"tasks": ['
                '{"description": "Collect sales data"},'
                '{"description": "Analyze regional sales"},'
                '{"description": "Find anomalies"},'
                '{"description": "Summarize findings"}'
                ']}'
            ),
            model="mock-planner",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_deep_agent_flow():

    llm = MockLLM()

    planner = DeepAgentPlanner(
        llm=llm
    )

    worker = DeepAgentWorker(
        tool_registry=ToolRegistry(),
        subagent_registry=SubAgentRegistry(),
    )

    reducer = DeepAgentResultReducer()

    graph_builder = DeepAgentGraph(
        planner=planner,
        worker=worker,
        reducer=reducer,
    )

    graph = graph_builder.compile()

    runtime = DeepAgentRuntime(
        graph
    )

    result = await runtime.run(
        "Analyze company sales performance"
    )

    assert result.success is True

    assert result.completed_tasks == 4

    assert result.failed_tasks == 0

    assert result.result["goal"] == (
        "Analyze company sales performance"
    )

    assert (
        result.result["total_results"]
        == 4
    )