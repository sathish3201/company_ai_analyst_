from company_ai.workflows.models import (
    ConditionalRoute,
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    WorkflowNodeType,
)


def test_workflow_node_creation():

    node = WorkflowNode(
        id="analysis",
        node_type=WorkflowNodeType.AGENT,
    )

    assert node.id == "analysis"
    assert node.node_type == WorkflowNodeType.AGENT
    assert node.config == {}


def test_workflow_edge_creation():

    edge = WorkflowEdge(
        source="analysis",
        target="result",
    )

    assert edge.source == "analysis"
    assert edge.target == "result"


def test_conditional_route_creation():

    route = ConditionalRoute(
        source="router",
        router="research_router",
        targets=[
            "research",
            "direct_answer",
        ],
    )

    assert route.source == "router"
    assert route.router == "research_router"
    assert route.targets == [
        "research",
        "direct_answer",
    ]


def test_workflow_definition_creation():

    workflow = WorkflowDefinition(
        name="company_analysis",
        version="1.0",
        entry_node="analysis",
        nodes=[
            WorkflowNode(
                id="analysis",
                node_type=WorkflowNodeType.AGENT,
            ),
            WorkflowNode(
                id="result",
                node_type=WorkflowNodeType.REDUCER,
            ),
        ],
        edges=[
            WorkflowEdge(
                source="analysis",
                target="result",
            ),
            WorkflowEdge(
                source="result",
                target="__end__",
            ),
        ],
    )

    assert workflow.name == "company_analysis"
    assert workflow.version == "1.0"
    assert workflow.entry_node == "analysis"
    assert len(workflow.nodes) == 2
    assert len(workflow.edges) == 2