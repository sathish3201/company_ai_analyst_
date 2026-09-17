import pytest

from company_ai.agents.tool_registry import (
    Tool,
    ToolRegistry,
)


class MockTool(Tool):

    @property
    def name(self):
        return "mock_tool"

    async def execute(self, **kwargs):
        return kwargs


def test_register_tool():

    registry = ToolRegistry()

    tool = MockTool()

    registry.register(tool)

    assert registry.has("mock_tool")
    assert registry.get("mock_tool") is tool


def test_duplicate_tool_rejected():

    registry = ToolRegistry()

    registry.register(MockTool())

    with pytest.raises(ValueError):
        registry.register(MockTool())


def test_missing_tool_rejected():

    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_unregister_tool():

    registry = ToolRegistry()

    registry.register(MockTool())

    registry.unregister(
        "mock_tool"
    )

    assert not registry.has(
        "mock_tool"
    )