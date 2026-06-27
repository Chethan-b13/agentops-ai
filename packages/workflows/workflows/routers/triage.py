from workflows.state import IncidentWorkflowState


def route_after_triage(
    state: IncidentWorkflowState,
) -> str:

    triage_result = state.get("triage_result")
    if triage_result and triage_result.confidence >= 0.8:
        return "continue"

    return "human_review"