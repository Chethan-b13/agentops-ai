from shared.services.execution_service import (
    ExecutionService,
)

from workflows.state import (
    IncidentWorkflowState,
)


def create_execute_remediation_node(
    execution_service: ExecutionService,
):

    def execute_remediation_node(
        state: IncidentWorkflowState,
    ):

        if (
            state["approval"]
            != "approved"
        ):
            return state

        execution_service.execute(
            incident_id=state["incident_id"],
            remediation_plan=state[
                "remediation_plan"
            ],
            validation_result=state[
                "validation_result"
            ],
        )

        return state

    return execute_remediation_node