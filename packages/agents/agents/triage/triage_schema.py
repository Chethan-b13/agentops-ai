from pydantic import BaseModel, Field
from enum import Enum

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentCategory(str, Enum):
    DATABASE = "database"
    NETWORK = "network"
    COMPUTE = "compute"
    STORAGE = "storage"
    APPLICATION = "application"


class TriageResultSchema(BaseModel):
    severity: Severity = Field(
        description="Incident severity"
    )

    category: IncidentCategory = Field(
        description="Incident category"
    )

    owner: str = Field(
        description="Owning team"
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score",
    )