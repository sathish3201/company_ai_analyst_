from operator import add
from typing import Annotated, Any

from typing_extensions import TypedDict


class WorkflowState(TypedDict, total=False):
    """
    Shared state used by the dynamically constructed LangGraph.
    """

    workflow_name: str

    current_node: str

    input: dict[str, Any]

    results: Annotated[
        list[dict[str, Any]],
        add,
    ]

    final_result: Any

    error: str | None