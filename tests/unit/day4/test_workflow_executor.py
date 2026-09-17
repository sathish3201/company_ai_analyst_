import pytest

from company_ai.workflows.builder import (
    DynamicWorkflowBuilder,
)

from company_ai.workflows.executor import (
    WorkflowExecutor,
)

from company_ai.workflows.models import (
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    WorkflowNodeType,
)

from company_ai.workflows.registry import (
    WorkflowNodeRegistry,
)

from company_ai.workflows.validators import (
    WorkflowValidator,
)


def agent_handler(
    state,
    config,
):

    return {
        "message": config.get(
            "message",
            "hello",
        )
    }


def make_executor():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        agent_handler,
    )

    builder = DynamicWorkflowBuilder(
        registry=registry,
        validator=WorkflowValidator(),
    )

    return WorkflowExecutor(
        builder=builder
    )


def make_workflow():

    return WorkflowDefinition(
        name="executor_test",
        version="1.0",
        entry_node="agent",
        nodes=[
            WorkflowNode(
                id="agent",
                node_type=WorkflowNodeType.AGENT,
                config={
                    "message": "hello"
                },
            )
        ],
        edges=[
            WorkflowEdge(
                source="agent",
                target="__end__",
            )
        ],
    )


@pytest.mark.asyncio
async def test_executor_runs_workflow():

    executor = make_executor()

    result = await executor.execute(
        make_workflow()
    )

    assert result["workflow_name"] == (
        "executor_test"
    )

    assert result["current_node"] == "agent"

    assert len(
        result["results"]
    ) == 1


@pytest.mark.asyncio
async def test_executor_accepts_initial_state():

    executor = make_executor()

    result = await executor.execute(
        make_workflow(),
        initial_state={
            "input": {
                "customer": "ACME"
            }
        },
    )

    assert result["input"]["customer"] == (
        "ACME"
    )