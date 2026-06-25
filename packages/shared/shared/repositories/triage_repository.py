from uuid import uuid4

from sqlalchemy.orm import Session

from shared.models.triage_result import (
    TriageResult,
)


class TriageRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        incident_id: str,
        severity: str,
        category: str,
        owner: str,
        confidence: float,
    ) -> TriageResult:

        result = TriageResult(
            id=f"TRI-{uuid4().hex[:8]}",
            incident_id=incident_id,
            severity=severity,
            category=category,
            owner=owner,
            confidence=confidence,
        )

        self.db.add(result)

        self.db.commit()

        self.db.refresh(result)

        return result

    def get_by_incident_id(
        self,
        incident_id: str,
    ) -> TriageResult | None:

        return (
            self.db
            .query(TriageResult)
            .filter(
                TriageResult.incident_id
                == incident_id
            )
            .first()
        )