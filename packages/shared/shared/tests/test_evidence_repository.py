from shared.database.session import SessionLocal
from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)


db = SessionLocal()

incident_repo = IncidentRepository(db)
evidence_repo = IncidentEvidenceRepository(db)

incident = incident_repo.get_all()[0]

evidence = evidence_repo.create(
    incident_id=incident.id,
    evidence_type="logs",
    source="mock-cloudwatch",
    raw_data={
        "entries": [
            "Database connection timeout",
            "Database connection timeout",
        ]
    },
    summary_data={
        "error": "Database connection timeout",
        "count": 2,
    },
)

print(evidence.id)

results = evidence_repo.get_by_incident_id(
    incident.id
)

print(results)