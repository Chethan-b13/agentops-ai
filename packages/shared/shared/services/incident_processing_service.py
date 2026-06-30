from sqlalchemy.orm import Session

from shared.repositories.incident_repository import IncidentRepository

from workflows.factory import create_workflow


class IncidentProcessingService:

    def __init__(self, db: Session):
        self.db = db
        self.incident_repository = IncidentRepository(db)

    def process(self, incident):
        """
        Orchestrates the production incident workflow.

        This service owns:
        - Persisting incidents
        - Creating the workflow
        - Executing the workflow

        It does NOT:
        - Read from SQS
        - Map CloudWatch events
        """

        incident = self.incident_repository.create(
            incident
        )

        print(
            f"Created incident: {incident.id}"
        )

        return incident