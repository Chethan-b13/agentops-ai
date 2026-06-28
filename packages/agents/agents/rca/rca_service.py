from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)
from shared.repositories.rca_repository import (
    RCARepository,
)
from shared.schemas.knowledge import (
    KnowledgeDocument,
)

from agents.triage.triage_schema import (
    TriageResultSchema,
)

from .rca_agent import RCAAgent
from .rca_schema import RCAResultSchema


class RCAService:

    def __init__(
        self,
        incident_repo: IncidentRepository,
        evidence_repo: IncidentEvidenceRepository,
        rca_repo: RCARepository,
        rca_agent: RCAAgent,
    ):
        self.incident_repo = incident_repo
        self.evidence_repo = evidence_repo
        self.rca_repo = rca_repo
        self.agent = rca_agent

    def analyze(
        self,
        incident_id: str,
        knowledge_documents: list[KnowledgeDocument],
        triage_result: TriageResultSchema,
    ) -> RCAResultSchema:

        incident = self.incident_repo.get_by_id(
            incident_id
        )

        if incident is None:
            raise ValueError(
                f"Incident {incident_id} not found"
            )

        evidence = (
            self.evidence_repo
            .get_by_incident_id(
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

        triage_context = triage_result.model_dump()

        result = self.agent.analyze(
            incident_context=incident_context,
            evidence_context=evidence_context,
            knowledge_context=knowledge_context,
            triage_context=triage_context,
        )

        self.rca_repo.create(
            incident_id=incident_id,
            root_cause=result.root_cause,
            explanation=result.explanation,
            confidence=result.confidence,
            supporting_evidence=result.supporting_evidence,
        )

        return result