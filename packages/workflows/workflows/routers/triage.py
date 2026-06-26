from workflows.state import IncidentWorkflowState


def route_after_triage(
    state: IncidentWorkflowState,
) -> str:

    if state["triage_result"].confidence >= 0.8:
        return "continue"

    return "human_review"