from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from workflows.state import IncidentWorkflowState
from workflows.workflow_context import WorkflowContext

from workflows.graphs.investigation_graph import (
    create_investigation_graph,
)


def create_incident_graph(
    workflow_context: WorkflowContext,
):

    builder = StateGraph(
        IncidentWorkflowState,
    )

    investigation_graph = (
        create_investigation_graph(
            workflow_context
        )
    )

    builder.add_node(
        "investigation",
        investigation_graph,
    )

    builder.add_edge(
        START,
        "investigation",
    )

    builder.add_edge(
        "investigation",
        END,
    )

    return builder.compile()