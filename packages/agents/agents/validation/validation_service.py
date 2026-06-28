from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)
from shared.repositories.validation_repository import ValidationRepository
from shared.schemas.knowledge import (
    KnowledgeDocument,
)

from agents.triage.triage_schema import (
    TriageResultSchema,
)
from agents.rca.rca_schema import (
    RCAResultSchema,
)

from agents.remediation.schema import RemediationPlanSchema

from agents.validation.validation_agent import ValidationAgent
from agents.validation.validation_schema import ValidationResultSchema


class ValidationService:

    def __init__(
        self,
        incident_repo: IncidentRepository,
        evidence_repo: IncidentEvidenceRepository,
        validation_repo: ValidationRepository,
        validation_agent: ValidationAgent,
    ):
        self.incident_repo = incident_repo
        self.evidence_repo = evidence_repo
        self.validation_repo = validation_repo
        self.agent = validation_agent

    def validate(
        self,
        incident_id: str,
        knowledge_documents: list[KnowledgeDocument],
        triage_result: TriageResultSchema,
        rca_result: RCAResultSchema,
        remediation_plan: RemediationPlanSchema,
    ) -> ValidationResultSchema:

        incident = self.incident_repo.get_by_id(
            incident_id
        )

        if incident is None:
            raise ValueError(
                f"Incident {incident_id} not found"
            )

        evidence = (
            self.evidence_repo.get_by_incident_id(
                incident_id
            )
        )

        incident_context = {
            "service": incident.service,
            "region": incident.region,
            "metric_name": incident.metric_name,
            "current_value": incident.current_value,
            "severity": incident.severity,
        }

        evidence_context = [
            {
                "type": e.evidence_type,
                "summary": e.summary_data,
            }
            for e in evidence
        ]

        knowledge_context = [
            doc.model_dump()
            for doc in knowledge_documents
        ]

        triage_context = (
            triage_result.model_dump()
        )

        rca_context = (
            rca_result.model_dump()
        )

        remediation_context = remediation_plan.model_dump()

        result = self.agent.validate(
            incident_context=incident_context,
            evidence_context=evidence_context,
            knowledge_context=knowledge_context,
            triage_context=triage_context,
            rca_context=rca_context,
            remediation_context=remediation_context,
        )

        self.validation_repo.create(
            incident_id=incident_id,
            status=result.status.value,
            summary=result.summary,
            findings=result.findings,
            recommendations=result.recommendations,
            confidence=result.confidence,
        )

        return result