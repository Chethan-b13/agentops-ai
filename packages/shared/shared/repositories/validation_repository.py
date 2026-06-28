from shared.models.validation_result import (
    ValidationResult,
)


class ValidationRepository:

    def __init__(self, db):
        self.db = db

    def create(
        self,
        *,
        incident_id: str,
        status: str,
        summary: str,
        findings: list[str],
        recommendations: list[str],
        confidence: float,
    ) -> ValidationResult:

        validation = ValidationResult(
            incident_id=incident_id,
            status=status,
            summary=summary,
            findings=findings,
            recommendations=recommendations,
            confidence=confidence,
        )

        self.db.add(validation)
        self.db.commit()
        self.db.refresh(validation)

        return validation