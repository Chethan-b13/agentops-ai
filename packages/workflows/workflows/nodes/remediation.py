from agents.remediation.remediation_service import (
    RemediationService,
)

from workflows.state import (
    IncidentWorkflowState,
)
from shared.telemetry import trace_span

def create_remediation_node(
    remediation_service: RemediationService,
):

    @trace_span("Generate Remediation")
    def remediation_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        result = remediation_service.generate(
            incident_id=state["incident_id"],
            knowledge_documents=state[
                "knowledge_documents"
            ],
            triage_result=state[
                "triage_result"
            ],
            rca_result=state[
                "rca_result"
            ],
        )

        return {
            **state,
            "remediation_plan": result,
        }

    return remediation_node