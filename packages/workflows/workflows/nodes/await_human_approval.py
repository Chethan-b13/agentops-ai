from langgraph.types import interrupt

from workflows.state import (
    IncidentWorkflowState,
)


def await_human_approval_node(
    state: IncidentWorkflowState,
) -> IncidentWorkflowState:

    approval = interrupt(
        {
            "incident_id": state["incident_id"],
            "triage_result": state["triage_result"].model_dump(),
            "rca_result": state["rca_result"].model_dump(),
            "remediation_plan": state["remediation_plan"].model_dump(),
            "validation_result": state["validation_result"].model_dump(),
        }
    )

    return {
        **state,
        "approval": approval,
    }