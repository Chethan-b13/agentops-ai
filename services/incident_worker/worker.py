import json

import boto3

from mappers.incident_mapper import map_event_to_incident

from shared.database.session import SessionLocal
from shared.settings import settings

from workflows.factory import create_workflow
from shared.repositories.incident_repository import IncidentRepository


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
    incident_repository = IncidentRepository(db)

    try:

        with create_workflow(db) as graph:

            incident = map_event_to_incident(body)

            incident = incident_repository.create(
                incident
            )

            print(
                f"Created incident: {incident.id}"
            )

            config = {
                "configurable": {
                    "thread_id": incident.id,
                }
            }

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

            workflow.incident_repository.update_status(
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