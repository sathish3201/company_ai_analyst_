import json
from uuid import uuid4

from company_ai.contracts.agent import PlannerPort
from company_ai.contracts.llm import (
    LLMGatewayPort,
    LLMRequest,
    Message,
)
from company_ai.models.agent import (
    AgentPlan,
    AgentTask,
)


class DeepAgentPlanner(PlannerPort):

    def __init__(
        self,
        llm: LLMGatewayPort,
    ) -> None:
        self._llm = llm

    async def create_plan(
        self,
        goal: str,
    ) -> AgentPlan:

        request = LLMRequest(
            purpose="planner",
            temperature=0.0,
            messages=[
                Message(
                    role="system",
                    content=(
                        "You are an enterprise task planner.\n\n"
                        "Break the user's goal into independent "
                        "executable tasks whenever possible.\n\n"
                        "Return JSON only.\n\n"
                        "Format:\n"
                        "{\n"
                        '  "tasks": [\n'
                        '    {"description": "task 1"},\n'
                        '    {"description": "task 2"}\n'
                        "  ]\n"
                        "}\n\n"
                        "Do not execute any task."
                    ),
                ),
                Message(
                    role="user",
                    content=goal,
                ),
            ],
        )

        response = await self._llm.complete(
            request
        )

        return self._parse_plan(
            goal=goal,
            content=response.content,
        )

    @staticmethod
    def _parse_plan(
        goal: str,
        content: str,
    ) -> AgentPlan:

        try:
            data = json.loads(content)

        except json.JSONDecodeError:

            return AgentPlan(
                goal=goal,
                tasks=[
                    AgentTask(
                        task_id=str(uuid4()),
                        description=goal,
                    )
                ],
                reasoning=(
                    "Planner returned invalid JSON. "
                    "Fallback task created."
                ),
            )

        raw_tasks = data.get(
            "tasks",
            [],
        )

        tasks: list[AgentTask] = []

        for raw_task in raw_tasks:

            if isinstance(
                raw_task,
                str,
            ):
                description = raw_task

            elif isinstance(
                raw_task,
                dict,
            ):
                description = raw_task.get(
                    "description",
                    "",
                )

            else:
                continue

            description = description.strip()

            if not description:
                continue

            tasks.append(
                AgentTask(
                    task_id=str(uuid4()),
                    description=description,
                )
            )

        if not tasks:

            tasks.append(
                AgentTask(
                    task_id=str(uuid4()),
                    description=goal,
                )
            )

        return AgentPlan(
            goal=goal,
            tasks=tasks,
        )