import json

import boto3

from mappers.incident_mapper import map_event_to_incident

from shared.database.session import SessionLocal
from shared.settings import settings
from shared.repositories.incident_repository import IncidentRepository
from shared.services import IncidentProcessingService

from shared.telemetry import initialize_tracing
from shared.telemetry import get_tracer
from shared.telemetry import set_incident_context

from shared.observability import (
    initialize_langfuse,
    get_langfuse,
    set_current_trace,
)

from workflows.factory import create_workflow


def main():

    initialize_tracing(
        service_name="incident-worker",
    )
    initialize_langfuse()
    tracer = get_tracer(__name__)

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
    incident_repository = IncidentRepository(db)
    service = IncidentProcessingService(db)

    try:

        with create_workflow(db) as graph:

            incident = map_event_to_incident(body)

            incident = service.process(
                incident
            )

            config = {
                "configurable": {
                    "thread_id": incident.id,
                }
            }

            with tracer.start_as_current_span("Incident Workflow") as span:
                
                langfuse = get_langfuse()

                trace = langfuse.trace(
                    name="Incident Workflow",
                    user_id="agentops-ai",
                    metadata={
                        "incident_id": incident.id,
                        "service": incident.service,
                    },
                )

                set_current_trace(trace)

                set_incident_context(
                    incident_id=incident.id,
                    service=incident.service,
                    severity=incident.severity.value
                    if hasattr(incident.severity, "value")
                    else str(incident.severity),
                )

                state = graph.invoke(
                    {
                        "incident_id": incident.id,
                    },
                    config=config,
                )

                print(state)

                print(
                    f"Graph invoked for {incident.id}"
                )

            sqs.delete_message(
                QueueUrl=settings.sqs_queue_url,
                ReceiptHandle=message[
                    "ReceiptHandle"
                ],
            )

            print("Message deleted")

    except Exception as e:

        if "incident" in locals():

            incident_repository.update_status(
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