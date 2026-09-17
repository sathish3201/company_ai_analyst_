import pytest

from company_ai.agents.subagent_registry import (
    SubAgent,
    SubAgentRegistry,
)
from company_ai.agents.tool_registry import (
    Tool,
    ToolRegistry,
)
from company_ai.agents.worker import (
    DeepAgentWorker,
)
from company_ai.models.agent import AgentTask


class EchoTool(Tool):

    @property
    def name(self):
        return "echo"

    async def execute(self, **kwargs):
        return kwargs


class EchoAgent(SubAgent):

    @property
    def name(self):
        return "echo_agent"

    async def run(
        self,
        task,
        context,
    ):

        return {
            "task": task
        }


@pytest.mark.asyncio
async def test_generic_worker():

    worker = DeepAgentWorker(
        tool_registry=ToolRegistry(),
        subagent_registry=SubAgentRegistry(),
    )

    task = AgentTask(
        task_id="1",
        description="Analyze data",
    )

    result = await worker.execute(
        task,
        {},
    )

    assert result["status"] == "executed"


@pytest.mark.asyncio
async def test_tool_worker():

    tools = ToolRegistry()

    tools.register(
        EchoTool()
    )

    worker = DeepAgentWorker(
        tool_registry=tools,
        subagent_registry=SubAgentRegistry(),
    )

    task = AgentTask(
        task_id="1",
        description="Echo",
        metadata={
            "execution_type": "tool",
            "tool": "echo",
            "arguments": {
                "value": "hello"
            },
        },
    )

    result = await worker.execute(
        task,
        {},
    )

    assert result == {
        "value": "hello"
    }


@pytest.mark.asyncio
async def test_subagent_worker():

    agents = SubAgentRegistry()

    agents.register(
        EchoAgent()
    )

    worker = DeepAgentWorker(
        tool_registry=ToolRegistry(),
        subagent_registry=agents,
    )

    task = AgentTask(
        task_id="1",
        description="Do work",
        metadata={
            "execution_type": "subagent",
            "agent": "echo_agent",
        },
    )

    result = await worker.execute(
        task,
        {},
    )

    assert result["task"] == "Do work"