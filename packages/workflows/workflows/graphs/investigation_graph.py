from langgraph.graph import (
    START,
    END,
    StateGraph,
)

from workflows.state import IncidentWorkflowState
from workflows.workflow_context import WorkflowContext
from workflows.nodes import (
    create_retrieve_knowledge_node,
    create_rca_node,
    create_collect_evidence_node,
    create_triage_node,
    create_remediation_node,
    create_validation_node,
    await_human_approval_node,
    create_execute_remediation_node
)
from workflows.routers import (
    route_after_triage,
    route_after_rca
)


def create_investigation_graph(
    workflow_context: WorkflowContext,
    checkpointer
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

    builder.add_node(
        "remediation",
        create_remediation_node(
            workflow_context.remediation_service,
        ),
    )

    builder.add_node(
        "validation",
        create_validation_node(
            workflow_context.validation_service,
        ),
    )

    builder.add_node(
        "await_human_approval",
        await_human_approval_node,
    )

    builder.add_node(
        "execute_remediation",
        create_execute_remediation_node(
            workflow_context.execution_service,
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

    builder.add_conditional_edges(
        "rca",
        route_after_rca,
        {
            "continue": "remediation",
            "human_review": END,
        },
    )

    builder.add_edge(
        "remediation",
        "validation",
    )

    builder.add_edge(
        "validation",
        "await_human_approval",
    )

    builder.add_edge(
        "await_human_approval",
        "execute_remediation",
    )

    builder.add_edge(
        "execute_remediation",
        END,
    )

    graph = builder.compile(
        checkpointer=checkpointer,
        name="investigation_workflow",
    )

    return graph