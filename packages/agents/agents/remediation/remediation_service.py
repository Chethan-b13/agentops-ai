from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)
from shared.repositories.remediation_repository import (
    RemediationRepository,
)
from shared.schemas.knowledge import (
    KnowledgeDocument,
)

from agents.triage.triage_schema import (
    TriageResultSchema,
)
from agents.rca.rca_schema import (
    RCAResultSchema,
)

from agents.remediation.remediation_agent import RemediationAgent
from agents.remediation.schema import (
    RemediationPlanSchema,
)


class RemediationService:

    def __init__(
        self,
        incident_repo: IncidentRepository,
        evidence_repo: IncidentEvidenceRepository,
        remediation_repo: RemediationRepository,
        remediation_agent: RemediationAgent,
    ):
        self.incident_repo = incident_repo
        self.evidence_repo = evidence_repo
        self.remediation_repo = remediation_repo
        self.agent = remediation_agent

    def generate(
        self,
        incident_id: str,
        knowledge_documents: list[KnowledgeDocument],
        triage_result: TriageResultSchema,
        rca_result: RCAResultSchema,
    ) -> RemediationPlanSchema:

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

        result = self.agent.generate(
            incident_context=incident_context,
            evidence_context=evidence_context,
            knowledge_context=knowledge_context,
            triage_context=triage_context,
            rca_context=rca_context,
        )

        self.remediation_repo.create(
            incident_id=incident_id,
            title=result.title,
            summary=result.summary,
            reasoning=result.reasoning,
            recommended_actions=result.recommended_actions,
            rollback_plan=result.rollback_plan,
            risk=result.risk.value,
            requires_downtime=result.requires_downtime,
            confidence=result.confidence,
        )

        return result