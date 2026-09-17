import pytest

from company_ai.agents.planner import (
    DeepAgentPlanner,
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
                '{"description": "Get sales data"},'
                '{"description": "Analyze sales data"},'
                '{"description": "Summarize results"}'
                ']}'
            ),
            model="mock",
        )


@pytest.mark.asyncio
async def test_planner_creates_plan():

    planner = DeepAgentPlanner(
        llm=MockLLM()
    )

    plan = await planner.create_plan(
        "Analyze sales performance"
    )

    assert plan.goal == (
        "Analyze sales performance"
    )

    assert len(plan.tasks) == 3

    assert (
        plan.tasks[0].description
        == "Get sales data"
    )


@pytest.mark.asyncio
async def test_planner_invalid_json():

    class InvalidLLM:

        async def complete(
            self,
            request,
        ):

            return LLMResponse(
                content="invalid",
                model="mock",
            )

    planner = DeepAgentPlanner(
        llm=InvalidLLM()
    )

    plan = await planner.create_plan(
        "Analyze sales"
    )

    assert len(plan.tasks) == 1

    assert (
        plan.tasks[0].description
        == "Analyze sales"
    )