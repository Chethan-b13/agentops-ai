from sqlalchemy.orm import Session

from shared.models.incident import Incident


class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, incident: Incident) -> Incident:
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)

        return incident
    
    def get_all(self) -> list[Incident]:
        return (
            self.db
            .query(Incident)
            .order_by(Incident.created_at.desc())
            .all()
        )


    def get_by_id(self, incident_id: str) -> Incident | None:
        return (
            self.db
            .query(Incident)
            .filter(Incident.id == incident_id)
            .first()
        )
    
    def update_status(
        self,
        incident_id: str,
        status: str,
    ) -> Incident | None:

        incident = self.get_by_id(incident_id)

        if not incident:
            return None

        incident.status = status

        self.db.commit()
        self.db.refresh(incident)
        return incident