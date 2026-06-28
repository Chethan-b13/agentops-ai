from workflows.state import (
    IncidentWorkflowState,
)


def route_after_rca(state: IncidentWorkflowState) -> str:

    if state["rca_result"].confidence >= 0.8:
        return "continue"

    return "human_review"