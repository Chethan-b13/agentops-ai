from shared.database.session import SessionLocal

from shared.repositories.incident_repository import (
    IncidentRepository,
)

from shared.repositories.triage_repository import (
    TriageRepository,
)


db = SessionLocal()

incident_repo = IncidentRepository(db)

triage_repo = TriageRepository(db)

incident = incident_repo.get_all()[0]

result = triage_repo.create(
    incident_id=incident.id,
    severity="high",
    category="database",
    owner="platform-team",
    confidence=0.91,
)

print(result.id)

retrieved = (
    triage_repo.get_by_incident_id(
        incident.id
    )
)

print(retrieved)