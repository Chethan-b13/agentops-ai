from datetime import datetime
from pydantic import BaseModel

from shared.schemas.incident import IncidentStatus

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

class UpdateIncidentStatusRequest(BaseModel):
    status: IncidentStatus
