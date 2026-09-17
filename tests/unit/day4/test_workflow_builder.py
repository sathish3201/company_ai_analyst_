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


def agent_handler(
    state,
    config,
):

    return {
        "message": config.get(
            "message",
            "agent",
        )
    }


def reducer_handler(
    state,
    config,
):

    return {
        "count": len(
            state.get(
                "results",
                [],
            )
        )
    }


def make_builder():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        agent_handler,
    )

    registry.register(
        "reducer",
        reducer_handler,
    )

    validator = WorkflowValidator()

    return DynamicWorkflowBuilder(
        registry=registry,
        validator=validator,
    )


def test_builder_creates_graph():

    builder = make_builder()

    workflow = WorkflowDefinition(
        name="simple",
        version="1.0",
        entry_node="agent",
        nodes=[
            WorkflowNode(
                id="agent",
                node_type=WorkflowNodeType.AGENT,
                config={
                    "message": "hello"
                },
            ),
            WorkflowNode(
                id="reducer",
                node_type=WorkflowNodeType.REDUCER,
            ),
        ],
        edges=[
            WorkflowEdge(
                source="agent",
                target="reducer",
            ),
            WorkflowEdge(
                source="reducer",
                target="__end__",
            ),
        ],
    )

    graph = builder.build(workflow)

    assert graph is not None