from langgraph.graph import (
    START,
    END,
    StateGraph,
)

from workflows.state import IncidentWorkflowState
from workflows.nodes.collect_evidence import create_collect_evidence_node
from workflows.nodes.triage import create_triage_node
from workflows.workflow_context import WorkflowContext
from workflows.routers.triage import route_after_triage
from workflows.nodes.retrieve_knowledge import create_retrieve_knowledge_node
from workflows.nodes.rca import create_rca_node


def create_incident_graph(
    workflow_context: WorkflowContext
):

    builder = StateGraph(
        IncidentWorkflowState
    )

    builder.add_node(
        "collect_evidence",
        create_collect_evidence_node(
            workflow_context.context_collector,
        ),
    )

    builder.add_node(
        "triage",
        create_triage_node(
            workflow_context.triage_service,
        ),
    )

    builder.add_node(
        "retrieve_knowledge",
        create_retrieve_knowledge_node(
            workflow_context.knowledge_retriever,
        ),
    )

    builder.add_node(
        "rca",
        create_rca_node(
            workflow_context.rca_service,
        ),
    )

    builder.add_edge(
        START,
        "collect_evidence",
    )

    builder.add_edge(
        "collect_evidence",
        "triage",
    )

    builder.add_conditional_edges(
        "triage",
        route_after_triage,
        {
            "continue": "retrieve_knowledge",
            "human_review": END,
        },
    )

    builder.add_edge(
        "retrieve_knowledge",
        "rca",
    )

    builder.add_edge(
        "rca",
        END,
    )

    graph = builder.compile(
        name="incident_workflow"
    )

    return graph