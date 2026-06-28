from typing import TypedDict, NotRequired

from agents.triage.triage_schema import TriageResultSchema
from agents.rca.rca_schema import RCAResultSchema
from agents.remediation.schema import RemediationPlanSchema
from agents.validation.validation_schema import ValidationResultSchema

from shared.schemas.knowledge import KnowledgeDocument


class IncidentWorkflowState(TypedDict):
    incident_id: str

    triage_result: NotRequired[TriageResultSchema]

    knowledge_documents: NotRequired[
        list[KnowledgeDocument]
    ]

    rca_result: NotRequired[RCAResultSchema]

    remediation_plan: NotRequired[RemediationPlanSchema]

    validation_result: NotRequired[ValidationResultSchema]