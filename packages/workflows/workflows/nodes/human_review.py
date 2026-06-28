from workflows.state import (
    IncidentWorkflowState,
)


def human_review_node(
    state: IncidentWorkflowState,
):

    print(
        "Human review required:",
        state["incident_id"],
    )

    return state