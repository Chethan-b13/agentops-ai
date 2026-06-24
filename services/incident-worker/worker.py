import json
import boto3

from mappers.incident_mapper import map_event_to_incident

from shared.database.session import SessionLocal
from shared.repositories.incident_repository import IncidentRepository
from shared.settings import settings



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

    try:
        incident = map_event_to_incident(body)

        repository.create(incident)

        print(f"Created incident: {incident.id}")

        sqs.delete_message(
            QueueUrl=settings.sqs_queue_url,
            ReceiptHandle=message["ReceiptHandle"],
        )

        print("Message deleted")
    except Exception as e:
        print(f"Failed processing message: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()