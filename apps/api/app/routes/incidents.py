from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.incident import (
    IncidentResponse,
    IncidentListResponse,
    UpdateIncidentStatusRequest,
)
from shared.repositories.incident_repository import IncidentRepository


router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
)


@router.get("", response_model=IncidentListResponse)
def list_incidents(
    db: Session = Depends(get_db),
):
    repository = IncidentRepository(db)

    incidents = repository.get_all()

    return IncidentListResponse(
        incidents=[
            IncidentResponse.model_validate(i)
            for i in incidents
        ]
    )


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
):
    repository = IncidentRepository(db)

    incident = repository.get_by_id(incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return IncidentResponse.model_validate(
        incident
    )

@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
)
def update_incident_status(
    incident_id: str,
    payload: UpdateIncidentStatusRequest,
    db: Session = Depends(get_db),
):
    repository = IncidentRepository(db)

    incident = repository.update_status(
        incident_id=incident_id,
        status=payload.status,
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return IncidentResponse.model_validate(
        incident
    )