import uuid

from shared.models.incident import Incident


def map_event_to_incident(event: dict) -> Incident:
    detail = event["detail"]

    return Incident(
        id=f"INC-{uuid.uuid4().hex[:8]}",
        alarm_name=detail["alarmName"],
        service=detail["service"],
        region=event["region"],
        metric_name=detail["metricName"],
        threshold=detail["threshold"],
        current_value=detail["currentValue"],
        severity="unknown",
        source="cloudwatch",
        status="new",
    )