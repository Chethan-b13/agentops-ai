from uuid import uuid4

from sqlalchemy.orm import Session

from shared.models.incident_evidence import IncidentEvidence


class IncidentEvidenceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        incident_id: str,
        evidence_type: str,
        source: str,
        raw_data: dict,
        summary_data: dict,
    ) -> IncidentEvidence:

        evidence = IncidentEvidence(
            id=f"EVD-{uuid4().hex[:8]}",
            incident_id=incident_id,
            evidence_type=evidence_type,
            source=source,
            raw_data=raw_data,
            summary_data=summary_data,
        )

        self.db.add(evidence)
        self.db.commit()
        self.db.refresh(evidence)

        return evidence

    def get_by_incident_id(
        self,
        incident_id: str,
    ) -> list[IncidentEvidence]:

        return (
            self.db.query(IncidentEvidence)
            .filter(
                IncidentEvidence.incident_id == incident_id
            )
            .all()
        )