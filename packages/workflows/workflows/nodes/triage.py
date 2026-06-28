from agents.triage.triage_service import TriageService

from workflows.state import IncidentWorkflowState
from shared.telemetry import trace_span

def create_triage_node(
    triage_service: TriageService,
):
    
    @trace_span("Triage")
    def triage_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        result = triage_service.triage(
            state["incident_id"],
        )

        return {
            **state,
            "triage_result": result,
        }

    return triage_node