from workflows.state import IncidentWorkflowState

from shared.services.context_collector import ContextCollector


def create_collect_evidence_node(
    collector: ContextCollector,
):
    def collect_evidence_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        collector.collect(
            state["incident_id"]
        )

        return state

    return collect_evidence_node