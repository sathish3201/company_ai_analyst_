from collections import defaultdict, deque

from company_ai.workflows.contracts import WorkflowValidatorPort
from company_ai.workflows.models import WorkflowDefinition


class WorkflowValidator(WorkflowValidatorPort):
    """
    Validates a dynamic workflow before graph construction.
    """

    END_NODE = "__end__"

    def validate(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        self._validate_nodes(workflow)

        self._validate_entry_node(workflow)

        self._validate_edges(workflow)

        self._validate_reachability(workflow)

        self._validate_cycles(workflow)

    def _validate_nodes(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        if not workflow.nodes:
            raise ValueError(
                "Workflow must contain at least one node"
            )

        node_ids = [
            node.id
            for node in workflow.nodes
        ]

        if len(node_ids) != len(set(node_ids)):
            raise ValueError(
                "Workflow contains duplicate node IDs"
            )

        if self.END_NODE in node_ids:
            raise ValueError(
                f"{self.END_NODE} is reserved and cannot "
                "be used as a workflow node ID"
            )

    def _validate_entry_node(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        node_ids = {
            node.id
            for node in workflow.nodes
        }

        if workflow.entry_node not in node_ids:
            raise ValueError(
                "Entry node does not exist: "
                f"{workflow.entry_node}"
            )

    def _validate_edges(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        node_ids = {
            node.id
            for node in workflow.nodes
        }

        for edge in workflow.edges:

            if edge.source not in node_ids:
                raise ValueError(
                    "Unknown edge source: "
                    f"{edge.source}"
                )

            if edge.target == self.END_NODE:
                continue

            if edge.target not in node_ids:
                raise ValueError(
                    "Unknown edge target: "
                    f"{edge.target}"
                )

    def _build_adjacency(
        self,
        workflow: WorkflowDefinition,
    ) -> dict[str, list[str]]:

        graph: dict[str, list[str]] = defaultdict(list)

        for edge in workflow.edges:

            # END is a virtual LangGraph endpoint.
            # It should not participate in graph algorithms.
            if edge.target == self.END_NODE:
                continue

            graph[edge.source].append(
                edge.target
            )

        for node in workflow.nodes:
            graph.setdefault(node.id, [])

        return graph

    def _validate_reachability(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        graph = self._build_adjacency(workflow)

        visited: set[str] = set()

        queue = deque(
            [workflow.entry_node]
        )

        while queue:

            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            for neighbour in graph[current]:

                if neighbour not in visited:
                    queue.append(neighbour)

        node_ids = {
            node.id
            for node in workflow.nodes
        }

        unreachable = node_ids - visited

        if unreachable:

            raise ValueError(
                "Workflow contains unreachable nodes: "
                f"{sorted(unreachable)}"
            )

    def _validate_cycles(
        self,
        workflow: WorkflowDefinition,
    ) -> None:

        graph = self._build_adjacency(workflow)

        visited: set[str] = set()

        recursion_stack: set[str] = set()

        def dfs(node: str) -> bool:

            visited.add(node)

            recursion_stack.add(node)

            for neighbour in graph[node]:

                if neighbour not in visited:

                    if dfs(neighbour):
                        return True

                elif neighbour in recursion_stack:

                    return True

            recursion_stack.remove(node)

            return False

        for node in graph:

            if node not in visited:

                if dfs(node):
                    raise ValueError(
                        "Workflow contains a cycle"
                    )