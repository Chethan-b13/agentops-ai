from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class IncidentResponse(BaseModel):
    id: str

    alarm_name: str

    service: str

    region: str

    metric_name: str

    threshold: float

    current_value: float

    severity: str

    source: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True

class IncidentListResponse(BaseModel):
    incidents: list[IncidentResponse]

class IncidentStatus(str, Enum):
    NEW = "new"
    COLLECTING_EVIDENCE = "collecting_evidence"
    TRIAGING = "triaging"
    INVESTIGATING = "investigating"
    FIX_RECOMMENDED = "fix_recommended"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    RESOLVED = "resolved"
    FAILED = "failed"

class UpdateIncidentStatusRequest(BaseModel):
    status: IncidentStatus
