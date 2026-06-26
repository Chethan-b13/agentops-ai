from shared.database.session import SessionLocal
from shared.repositories.incident_repository import IncidentRepository
from shared.repositories.incident_evidence_repository import IncidentEvidenceRepository
from shared.repositories.triage_repository import TriageRepository
from agents.triage.triage_agent import TriageAgent
from agents.triage.triage_service import TriageService


db = SessionLocal()

incident_repo = IncidentRepository(db)
evidence_repo = IncidentEvidenceRepository(db)
triage_repo = TriageRepository(db)
agent = TriageAgent()

incident = incident_repo.get_all()[0]

service = TriageService(
    incident_repo,
    evidence_repo,
    triage_repo,
    agent,
)

result = service.triage(incident.id)

print(result)