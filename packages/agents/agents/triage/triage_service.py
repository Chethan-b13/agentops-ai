from shared.repositories.incident_repository import (
    IncidentRepository,
)

from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)

from shared.repositories.triage_repository import (
    TriageRepository,
)

from shared.schemas.incident import IncidentStatus

from .triage_agent import TriageAgent


class TriageService:

    def __init__(
        self,
        incident_repo: IncidentRepository,
        evidence_repo: IncidentEvidenceRepository,
        triage_repo: TriageRepository,
        triage_agent: TriageAgent
    ):
        self.incident_repo = incident_repo
        self.evidence_repo = evidence_repo
        self.triage_repo = triage_repo
        self.agent = triage_agent

    def triage(self, incident_id: str):
        
        incident = self.incident_repo.get_by_id(
            incident_id
        )

        if incident is None:
            raise ValueError(f"Incident {incident_id} not found")

        self.incident_repo.update_status(
            incident_id,
            IncidentStatus.TRIAGING,
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

        result = self.agent.classify(
            incident_context,
            evidence_context,
        )

        self.triage_repo.create(
            incident_id=incident_id,
            severity=result.severity,
            category=result.category,
            owner=result.owner,
            confidence=result.confidence,
        )

        self.incident_repo.update_status(
            incident_id,
            IncidentStatus.TRIAGED,
        )

        return result