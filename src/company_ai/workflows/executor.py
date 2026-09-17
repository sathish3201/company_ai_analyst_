from typing import Any

from company_ai.workflows.builder import (
    DynamicWorkflowBuilder,
)
from company_ai.workflows.contracts import (
    WorkflowExecutorPort,
)
from company_ai.workflows.models import (
    WorkflowDefinition,
)


class WorkflowExecutor(WorkflowExecutorPort):
    """
    Executes dynamically generated workflow definitions.
    """

    def __init__(
        self,
        builder: DynamicWorkflowBuilder,
    ) -> None:

        self._builder = builder

    async def execute(
        self,
        workflow: WorkflowDefinition,
        initial_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        graph = self._builder.build(
            workflow
        )

        state: dict[str, Any] = {
            "workflow_name": workflow.name,
            "input": {},
            "results": [],
        }

        if initial_state:
            state.update(initial_state)

        return await graph.ainvoke(
            state
        )