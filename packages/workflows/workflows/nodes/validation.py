from agents.validation.validation_service import (
    ValidationService,
)

from workflows.state import (
    IncidentWorkflowState,
)
from shared.telemetry import trace_span

def create_validation_node(
    validation_service: ValidationService,
):

    @trace_span("Validate Remediation")
    def validation_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        result = validation_service.validate(
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
            remediation_plan=state[
                "remediation_plan"
            ],
        )

        return {
            **state,
            "validation_result": result,
        }

    return validation_node