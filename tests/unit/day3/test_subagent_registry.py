import pytest

from company_ai.agents.subagent_registry import (
    SubAgent,
    SubAgentRegistry,
)


class MockSubAgent(SubAgent):

    @property
    def name(self):
        return "mock_agent"

    async def run(
        self,
        task,
        context,
    ):

        return {
            "task": task,
            "context": context,
        }


def test_register_subagent():

    registry = SubAgentRegistry()

    agent = MockSubAgent()

    registry.register(agent)

    assert registry.has(
        "mock_agent"
    )

    assert registry.get(
        "mock_agent"
    ) is agent


def test_duplicate_subagent_rejected():

    registry = SubAgentRegistry()

    registry.register(
        MockSubAgent()
    )

    with pytest.raises(ValueError):
        registry.register(
            MockSubAgent()
        )


def test_missing_subagent_rejected():

    registry = SubAgentRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")