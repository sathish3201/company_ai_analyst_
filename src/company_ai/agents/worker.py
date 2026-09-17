from typing import Any

from company_ai.agents.subagent_registry import (
    SubAgentRegistry,
)
from company_ai.agents.tool_registry import (
    ToolRegistry,
)
from company_ai.contracts.agent import WorkerPort
from company_ai.models.agent import AgentTask


class DeepAgentWorker(WorkerPort):

    def __init__(
        self,
        tool_registry: ToolRegistry,
        subagent_registry: SubAgentRegistry,
    ) -> None:

        self._tool_registry = tool_registry
        self._subagent_registry = subagent_registry

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> Any:

        execution_type = task.metadata.get(
            "execution_type",
            "generic",
        )

        if execution_type == "tool":

            tool_name = task.metadata.get(
                "tool"
            )

            if not tool_name:
                raise ValueError(
                    "Tool execution requires "
                    "'tool' metadata"
                )

            tool = self._tool_registry.get(
                tool_name
            )

            arguments = task.metadata.get(
                "arguments",
                {},
            )

            return await tool.execute(
                **arguments
            )

        if execution_type == "subagent":

            agent_name = task.metadata.get(
                "agent"
            )

            if not agent_name:
                raise ValueError(
                    "Sub-agent execution requires "
                    "'agent' metadata"
                )

            agent = self._subagent_registry.get(
                agent_name
            )

            return await agent.run(
                task=task.description,
                context=context,
            )

        return {
            "task": task.description,
            "status": "executed",
        }