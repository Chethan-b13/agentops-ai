from agents.triage.triage_service import TriageService

from workflows.state import IncidentWorkflowState


def create_triage_node(
    triage_service: TriageService,
):
    def triage_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        triage_service.triage(
            state["incident_id"],
        )

        return state

    return triage_node