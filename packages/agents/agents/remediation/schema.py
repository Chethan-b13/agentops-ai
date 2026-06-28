from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RemediationPlanSchema(BaseModel):
    title: str

    summary: str

    reasoning: str

    recommended_actions: list[str]

    rollback_plan: list[str]

    risk: RiskLevel

    requires_downtime: bool

    confidence: float