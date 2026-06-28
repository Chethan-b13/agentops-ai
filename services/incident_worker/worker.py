import json
import boto3

from mappers.incident_mapper import map_event_to_incident

from shared.services.context_collector import ContextCollector
from shared.database.session import SessionLocal
from shared.repositories.incident_repository import IncidentRepository
from shared.settings import settings
from shared.repositories.incident_evidence_repository import IncidentEvidenceRepository
from shared.repositories.triage_repository import TriageRepository
from shared.repositories.rca_repository import RCARepository
from shared.services.knowledge_retriever import KnowledgeRetriever

from agents.triage.triage_agent import TriageAgent
from agents.triage.triage_service import TriageService

from agents.rca.rca_agent import RCAAgent
from agents.rca.rca_service import RCAService

from workflows.graphs.investigation_graph import create_investigation_graph
from workflows.workflow_context import WorkflowContext

from shared.repositories.remediation_repository import RemediationRepository
from agents.remediation.remediation_agent import RemediationAgent
from agents.remediation.remediation_service import RemediationService

from shared.repositories.validation_repository import ValidationRepository
from agents.validation.validation_agent import ValidationAgent
from agents.validation.validation_service import ValidationService


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

    knowledge_retriever = KnowledgeRetriever()
    rca_repository = RCARepository(db)
    rca_agent = RCAAgent()
    rca_service = RCAService(
        incident_repo=repository,
        evidence_repo=evidence_repository,
        rca_repo=rca_repository,
        rca_agent=rca_agent,
    )


    remediation_repository = (
        RemediationRepository(db)
    )

    remediation_agent = (
        RemediationAgent()
    )

    remediation_service = (
        RemediationService(
            incident_repo=repository,
            evidence_repo=evidence_repository,
            remediation_repo=remediation_repository,
            remediation_agent=remediation_agent,
        )
    )

    validation_repository = ValidationRepository(db)

    validation_agent = ValidationAgent()

    validation_service = ValidationService(
        incident_repo=repository,
        evidence_repo=evidence_repository,
        validation_repo=validation_repository,
        validation_agent=validation_agent,
    )

    workflow_context = WorkflowContext(
        context_collector=context_collector,
        triage_service=triage_service,
        knowledge_retriever=knowledge_retriever,
        rca_service=rca_service,
        remediation_service=remediation_service,
        validation_service=validation_service
    )

    graph = create_investigation_graph(
        workflow_context
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