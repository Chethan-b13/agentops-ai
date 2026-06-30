import json
import uuid

from shared.models.incident import Incident


def map_event_to_incident(event: dict | list) -> Incident:
    # Handle list input (e.g. from sample_alarm_event.json)
    if isinstance(event, list):
        if len(event) > 0:
            event_dict = event[0]
        else:
            event_dict = {}
    elif isinstance(event, dict):
        event_dict = event
    else:
        event_dict = {}

    # Extract detail and region with case-insensitive support
    detail_val = event_dict.get("detail") or event_dict.get("Detail")
    region = event_dict.get("region") or event_dict.get("Region") or "us-east-1"
    
    # Parse detail if it is a JSON-serialized string
    if isinstance(detail_val, str):
        try:
            detail = json.loads(detail_val)
        except Exception:
            detail = {}
    elif isinstance(detail_val, dict):
        detail = detail_val
    else:
        detail = {}

    # Extract fields from detail (supporting camelCase, snake_case, PascalCase)
    alarm_name = (
        detail.get("alarmName")
        or detail.get("alarm_name")
        or detail.get("AlarmName")
        or "Unknown Alarm"
    )
    service = (
        detail.get("service")
        or detail.get("service_name")
        or detail.get("Service")
        or "unknown-service"
    )
    metric_name = (
        detail.get("metricName")
        or detail.get("metric_name")
        or detail.get("MetricName")
        or "unknown-metric"
    )

    def to_float(val, default=1.0):
        if val is None:
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    threshold = to_float(
        detail.get("threshold")
        or detail.get("Threshold")
    )
    current_value = to_float(
        detail.get("currentValue")
        or detail.get("current_value")
        or detail.get("CurrentValue")
    )

    severity = (
        detail.get("severity")
        or event_dict.get("severity")
        or "unknown"
    )
    source = (
        event_dict.get("source")
        or detail.get("source")
        or "cloudwatch"
    ).lower()

    return Incident(
        id=f"INC-{uuid.uuid4().hex[:8]}",
        alarm_name=alarm_name,
        service=service,
        region=region,
        metric_name=metric_name,
        threshold=threshold,
        current_value=current_value,
        severity=severity,
        source=source,
        status="new",
    )