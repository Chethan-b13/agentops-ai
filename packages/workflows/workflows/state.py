from typing import TypedDict, NotRequired

from agents.triage.triage_schema import TriageResultSchema

from shared.schemas.knowledge import KnowledgeDocument


class IncidentWorkflowState(TypedDict):
    incident_id: str

    triage_result: NotRequired[TriageResultSchema]

    knowledge_documents: NotRequired[
        list[KnowledgeDocument]
    ]