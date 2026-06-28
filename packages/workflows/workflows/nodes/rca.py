from agents.rca.rca_service import RCAService

from workflows.state import (
    IncidentWorkflowState,
)
from shared.telemetry import trace_span


def create_rca_node(rca_service: RCAService):

    @trace_span("Root Cause Analysis")
    def rca_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        result = rca_service.analyze(
            incident_id=state["incident_id"],
            knowledge_documents=state[
                "knowledge_documents"
            ],
            triage_result=state[
                "triage_result"
            ],
        )

        return {
            **state,
            "rca_result": result,
        }

    return rca_node