from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class WorkflowNodeType(str, Enum):
    """
    Supported logical node types in a dynamic workflow.
    """

    AGENT = "agent"
    WORKER = "worker"
    TOOL = "tool"
    SUBAGENT = "subagent"
    ROUTER = "router"
    REDUCER = "reducer"


class WorkflowNode(BaseModel):
    """
    Definition of one node in a workflow.
    """

    id: str
    node_type: WorkflowNodeType
    config: dict[str, Any] = Field(default_factory=dict)


class WorkflowEdge(BaseModel):
    """
    Normal directed edge between two workflow nodes.

    '__end__' is supported as the virtual LangGraph END target.
    """

    source: str
    target: str


class ConditionalRoute(BaseModel):
    """
    Describes a conditional routing rule.

    Example:

        source = "router"
        router = "research_router"
        targets = ["research", "direct_answer"]
    """

    source: str
    router: str
    targets: list[str] = Field(default_factory=list)


class WorkflowDefinition(BaseModel):
    """
    Complete dynamically generated workflow definition.
    """

    name: str
    version: str
    entry_node: str

    nodes: list[WorkflowNode] = Field(default_factory=list)

    edges: list[WorkflowEdge] = Field(default_factory=list)

    conditional_routes: list[ConditionalRoute] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(default_factory=dict)