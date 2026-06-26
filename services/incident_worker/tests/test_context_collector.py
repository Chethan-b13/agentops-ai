from shared.database.session import SessionLocal

from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)

from shared.services.context_collector import ContextCollector


db = SessionLocal()

incident_repo = IncidentRepository(db)
evidence_repo = IncidentEvidenceRepository(db)

incident = incident_repo.get_all()[0]

collector = ContextCollector(
    incident_repo,
    evidence_repo,
)

collector.collect(
    incident.id
)

print("done")