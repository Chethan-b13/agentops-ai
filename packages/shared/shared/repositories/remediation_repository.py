from shared.models.remediation_result import (
    RemediationResult,
)


class RemediationRepository:

    def __init__(self, db):
        self.db = db

    def create(
        self,
        *,
        incident_id: str,
        title: str,
        summary: str,
        reasoning: str,
        recommended_actions: list[str],
        rollback_plan: list[str],
        risk: str,
        requires_downtime: bool,
        confidence: float,
    ) -> RemediationResult:

        remediation = RemediationResult(
            incident_id=incident_id,
            title=title,
            summary=summary,
            reasoning=reasoning,
            recommended_actions=recommended_actions,
            rollback_plan=rollback_plan,
            risk=risk,
            requires_downtime=requires_downtime,
            confidence=confidence,
        )

        self.db.add(remediation)
        self.db.commit()
        self.db.refresh(remediation)

        return remediation