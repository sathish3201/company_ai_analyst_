import pytest

from company_ai.workflows.models import (
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    WorkflowNodeType,
)

from company_ai.workflows.validators import (
    WorkflowValidator,
)


def make_valid_workflow():

    return WorkflowDefinition(
        name="test_workflow",
        version="1.0",
        entry_node="start",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="finish",
                node_type=WorkflowNodeType.REDUCER,
            ),
        ],
        edges=[
            WorkflowEdge(
                source="start",
                target="finish",
            ),
            WorkflowEdge(
                source="finish",
                target="__end__",
            ),
        ],
    )


def test_valid_workflow():

    validator = WorkflowValidator()

    workflow = make_valid_workflow()

    validator.validate(workflow)


def test_empty_workflow_fails():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="empty",
        version="1.0",
        entry_node="start",
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_missing_entry_node_fails():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="invalid",
        version="1.0",
        entry_node="missing",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            )
        ],
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_duplicate_node_ids_fail():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="duplicate",
        version="1.0",
        entry_node="start",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.WORKER,
            ),
        ],
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_unknown_edge_source_fails():

    validator = WorkflowValidator()

    workflow = make_valid_workflow()

    workflow.edges.append(
        WorkflowEdge(
            source="unknown",
            target="finish",
        )
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_unknown_edge_target_fails():

    validator = WorkflowValidator()

    workflow = make_valid_workflow()

    workflow.edges.append(
        WorkflowEdge(
            source="start",
            target="unknown",
        )
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_end_target_is_allowed():

    validator = WorkflowValidator()

    workflow = make_valid_workflow()

    validator.validate(workflow)


def test_unreachable_node_fails():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="unreachable",
        version="1.0",
        entry_node="start",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="unused",
                node_type=WorkflowNodeType.WORKER,
            ),
        ],
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_cycle_fails():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="cycle",
        version="1.0",
        entry_node="start",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="worker",
                node_type=WorkflowNodeType.WORKER,
            ),
        ],
        edges=[
            WorkflowEdge(
                source="start",
                target="worker",
            ),
            WorkflowEdge(
                source="worker",
                target="start",
            ),
        ],
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)


def test_end_node_cannot_be_declared():

    validator = WorkflowValidator()

    workflow = WorkflowDefinition(
        name="invalid_end",
        version="1.0",
        entry_node="start",
        nodes=[
            WorkflowNode(
                id="start",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="__end__",
                node_type=WorkflowNodeType.REDUCER,
            ),
        ],
    )

    with pytest.raises(ValueError):

        validator.validate(workflow)