import json
import boto3

from mappers.incident_mapper import map_event_to_incident
from shared.services.context_collector import ContextCollector

from shared.database.session import SessionLocal
from shared.repositories.incident_repository import IncidentRepository
from shared.settings import settings

from shared.repositories.incident_evidence_repository import IncidentEvidenceRepository
from shared.repositories.triage_repository import TriageRepository

from agents.triage.triage_agent import TriageAgent
from agents.triage.triage_service import TriageService

from workflows.incident_graph import create_incident_graph


def main():
    sqs = boto3.client(
        "sqs",
        endpoint_url=settings.aws_endpoint_url,
        region_name=settings.aws_region,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

    response = sqs.receive_message(
        QueueUrl=settings.sqs_queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1,
    )

    messages = response.get("Messages", [])

    if not messages:
        print("No messages found")
        return

    message = messages[0]

    body = json.loads(message["Body"])

    db = SessionLocal()

    repository = IncidentRepository(db)

    evidence_repository = IncidentEvidenceRepository(db)

    context_collector = ContextCollector(
        repository,
        evidence_repository,
    )

    triage_repository = TriageRepository(db)
    triage_agent = TriageAgent()

    triage_service = TriageService(
        incident_repo=repository,
        evidence_repo=evidence_repository,
        triage_repo=triage_repository,
        triage_agent=triage_agent
    )

    graph = create_incident_graph(
        context_collector=context_collector,
        triage_service=triage_service,
    )

    try:
        incident = map_event_to_incident(body)

        incident = repository.create(incident)

        print(f"Created incident: {incident.id}")

        state = graph.invoke(
            {
                "incident_id": incident.id,
            }
        )

        print(state)

        print(
            f"Graph invoked for {incident.id}"
        )

        sqs.delete_message(
            QueueUrl=settings.sqs_queue_url,
            ReceiptHandle=message["ReceiptHandle"],
        )

        print("Message deleted")
    except Exception as e:
        if "incident" in locals():
            repository.update_status(
                incident.id,
                "failed",
            )

        print(
            f"Failed processing message: {e}"
        )

        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()