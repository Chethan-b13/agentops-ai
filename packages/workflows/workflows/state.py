from typing import TypedDict, NotRequired

from agents.triage.triage_schema import (
    TriageResultSchema,
)


class IncidentWorkflowState(TypedDict):
    incident_id: str

    triage_result: NotRequired[TriageResultSchema]