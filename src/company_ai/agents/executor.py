from typing import Any

from company_ai.agents.subagent_registry import SubAgentRegistry
from company_ai.agents.tool_registry import ToolRegistry
from company_ai.contracts.agent import TaskExecutorPort
from company_ai.models.agent import AgentState, AgentTask


class DeepAgentTaskExecutor(TaskExecutorPort):

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
        state: AgentState,
    ) -> Any:

        task_description = task.description.strip()

        # Day 3 keeps execution generic.
        # Explicit tool/sub-agent dispatch is provided through
        # metadata rather than hardcoded business logic.

        execution_type = task.metadata.get(
            "execution_type",
            "llm",
        )

        if execution_type == "tool":
            tool_name = task.metadata.get("tool")

            if not tool_name:
                raise ValueError(
                    "Tool execution requires metadata['tool']"
                )

            tool = self._tool_registry.get(tool_name)

            arguments = task.metadata.get(
                "arguments",
                {},
            )

            return await tool.execute(**arguments)

        if execution_type == "subagent":
            agent_name = task.metadata.get("agent")

            if not agent_name:
                raise ValueError(
                    "Sub-agent execution requires metadata['agent']"
                )

            agent = self._subagent_registry.get(agent_name)

            return await agent.run(
                task=task_description,
                context=state.metadata,
            )

        # Generic execution is intentionally represented
        # as a result for now. LLM-driven execution will be
        # expanded as the project progresses.
        return {
            "task": task_description,
            "status": "executed",
        }