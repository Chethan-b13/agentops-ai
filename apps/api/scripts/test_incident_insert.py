from shared.database.session import SessionLocal
from shared.models.incident import Incident
from shared.repositories.incident_repository import IncidentRepository


def main():
    db = SessionLocal()

    repository = IncidentRepository(db)

    incident = Incident(
        id="INC-000001",
        alarm_name="High CPU Usage",
        service="payments-api",
        region="us-east-1",
        metric_name="CPUUtilization",
        threshold=80,
        current_value=94,
        severity="unknown",
        source="cloudwatch",
        status="new",
    )

    repository.create(incident)

    print("Incident created successfully")


if __name__ == "__main__":
    main()