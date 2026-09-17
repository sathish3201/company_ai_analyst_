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


def analysis_handler(
    state,
    config,
):

    customer = state.get(
        "input",
        {},
    ).get(
        "customer",
        "unknown",
    )

    return {
        "customer": customer,
        "analysis": "completed",
    }


def reducer_handler(
    state,
    config,
):

    results = state.get(
        "results",
        [],
    )

    return {
        "result_count": len(results),
        "status": "completed",
    }


@pytest.mark.asyncio
async def test_complete_dynamic_workflow():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        analysis_handler,
    )

    registry.register(
        "reducer",
        reducer_handler,
    )

    validator = WorkflowValidator()

    builder = DynamicWorkflowBuilder(
        registry=registry,
        validator=validator,
    )

    executor = WorkflowExecutor(
        builder=builder
    )

    workflow = WorkflowDefinition(
        name="company_customer_analysis",
        version="1.0",
        entry_node="analysis",
        nodes=[
            WorkflowNode(
                id="analysis",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="reducer",
                node_type=WorkflowNodeType.REDUCER,
            ),
        ],
        edges=[
            WorkflowEdge(
                source="analysis",
                target="reducer",
            ),
            WorkflowEdge(
                source="reducer",
                target="__end__",
            ),
        ],
        metadata={
            "domain": "company_data",
        },
    )

    result = await executor.execute(
        workflow,
        initial_state={
            "input": {
                "customer": "ACME"
            }
        },
    )

    assert result["workflow_name"] == (
        "company_customer_analysis"
    )

    assert result["current_node"] == (
        "reducer"
    )

    assert len(
        result["results"]
    ) == 2

    assert result["results"][0]["result"][
        "customer"
    ] == "ACME"

    assert result["results"][1]["result"][
        "status"
    ] == "completed"