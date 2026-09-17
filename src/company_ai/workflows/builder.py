from typing import Any

from langgraph.graph import END, START, StateGraph

from company_ai.workflows.contracts import (
    WorkflowBuilderPort,
)
from company_ai.workflows.models import (
    WorkflowDefinition,
)
from company_ai.workflows.registry import (
    WorkflowNodeRegistry,
)
from company_ai.workflows.state import WorkflowState
from company_ai.workflows.validators import (
    WorkflowValidator,
)


class DynamicWorkflowBuilder(WorkflowBuilderPort):
    """
    Converts a declarative WorkflowDefinition
    into an executable LangGraph StateGraph.
    """

    END_NODE = "__end__"

    def __init__(
        self,
        registry: WorkflowNodeRegistry,
        validator: WorkflowValidator,
    ) -> None:

        self._registry = registry

        self._validator = validator

    def build(
        self,
        workflow: WorkflowDefinition,
    ) -> Any:

        self._validator.validate(workflow)

        builder = StateGraph(
            WorkflowState
        )

        self._add_nodes(
            builder=builder,
            workflow=workflow,
        )

        self._add_edges(
            builder=builder,
            workflow=workflow,
        )

        return builder.compile()

    def _add_nodes(
        self,
        builder: StateGraph,
        workflow: WorkflowDefinition,
    ) -> None:

        for node in workflow.nodes:

            handler = self._registry.get(
                node.node_type.value
            )

            wrapped_handler = (
                self._wrap_handler(
                    node_id=node.id,
                    handler=handler,
                    config=node.config,
                )
            )

            builder.add_node(
                node.id,
                wrapped_handler,
            )

    @staticmethod
    def _wrap_handler(
        node_id: str,
        handler: Any,
        config: dict[str, Any],
    ):

        async def node_handler(
            state: WorkflowState,
        ) -> dict[str, Any]:

            result = handler(
                state=state,
                config=config,
            )

            if hasattr(result, "__await__"):
                result = await result

            return {
                "current_node": node_id,
                "results": [
                    {
                        "node_id": node_id,
                        "result": result,
                    }
                ],
            }

        return node_handler

    def _add_edges(
        self,
        builder: StateGraph,
        workflow: WorkflowDefinition,
    ) -> None:

        builder.add_edge(
            START,
            workflow.entry_node,
        )

        for edge in workflow.edges:

            target = (
                END
                if edge.target == self.END_NODE
                else edge.target
            )

            builder.add_edge(
                edge.source,
                target,
            )