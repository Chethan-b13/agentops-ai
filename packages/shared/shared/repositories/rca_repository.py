from sqlalchemy.orm import Session

from shared.models.rca_result import RCAResult


class RCARepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        incident_id: str,
        root_cause: str,
        explanation: str,
        confidence: float,
        supporting_evidence: list[str],
    ) -> RCAResult:

        result = RCAResult(
            incident_id=incident_id,
            root_cause=root_cause,
            explanation=explanation,
            confidence=confidence,
            supporting_evidence=supporting_evidence,
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_by_incident_id(
        self,
        incident_id: str,
    ) -> RCAResult | None:

        return (
            self.db.query(RCAResult)
            .filter(
                RCAResult.incident_id == incident_id
            )
            .first()
        )