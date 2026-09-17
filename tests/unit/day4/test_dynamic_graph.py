import pytest

from company_ai.workflows.builder import (
    DynamicWorkflowBuilder,
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


def handler(**kwargs):

    state = kwargs["state"]
    config = kwargs["config"]

    return {
        "value": config.get(
            "value",
            state.get("input", {}).get(
                "value"
            ),
        )
    }


def create_builder():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        handler,
    )

    registry.register(
        "worker",
        handler,
    )

    registry.register(
        "reducer",
        handler,
    )

    return DynamicWorkflowBuilder(
        registry=registry,
        validator=WorkflowValidator(),
    )


@pytest.mark.asyncio
async def test_graph_changes_when_workflow_changes():

    builder = create_builder()

    workflow_one = WorkflowDefinition(
        name="workflow_one",
        version="1.0",
        entry_node="first",
        nodes=[
            WorkflowNode(
                id="first",
                node_type=WorkflowNodeType.AGENT,
                config={
                    "value": "first"
                },
            ),
            WorkflowNode(
                id="end",
                node_type=WorkflowNodeType.REDUCER,
                config={
                    "value": "end"
                },
            ),
        ],
        edges=[
            WorkflowEdge(
                source="first",
                target="end",
            ),
            WorkflowEdge(
                source="end",
                target="__end__",
            ),
        ],
    )

    graph_one = builder.build(
        workflow_one
    )

    result_one = await graph_one.ainvoke(
        {
            "workflow_name": workflow_one.name,
            "input": {},
            "results": [],
        }
    )

    assert result_one["current_node"] == "end"

    workflow_two = WorkflowDefinition(
        name="workflow_two",
        version="1.0",
        entry_node="first",
        nodes=[
            WorkflowNode(
                id="first",
                node_type=WorkflowNodeType.AGENT,
                config={
                    "value": "first"
                },
            ),
            WorkflowNode(
                id="middle",
                node_type=WorkflowNodeType.WORKER,
                config={
                    "value": "middle"
                },
            ),
            WorkflowNode(
                id="end",
                node_type=WorkflowNodeType.REDUCER,
                config={
                    "value": "end"
                },
            ),
        ],
        edges=[
            WorkflowEdge(
                source="first",
                target="middle",
            ),
            WorkflowEdge(
                source="middle",
                target="end",
            ),
            WorkflowEdge(
                source="end",
                target="__end__",
            ),
        ],
    )

    graph_two = builder.build(
        workflow_two
    )

    result_two = await graph_two.ainvoke(
        {
            "workflow_name": workflow_two.name,
            "input": {},
            "results": [],
        }
    )

    assert result_two["current_node"] == "end"

    assert len(
        result_two["results"]
    ) == 3