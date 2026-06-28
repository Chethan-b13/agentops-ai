from contextvars import ContextVar

from opentelemetry import trace


incident_id_ctx: ContextVar[str | None] = ContextVar(
    "incident_id",
    default=None,
)

workflow_id_ctx: ContextVar[str | None] = ContextVar(
    "workflow_id",
    default=None,
)

service_ctx: ContextVar[str | None] = ContextVar(
    "service",
    default=None,
)

severity_ctx: ContextVar[str | None] = ContextVar(
    "severity",
    default=None,
)


def set_incident_context(
    *,
    incident_id: str,
    workflow_id: str | None = None,
    service: str | None = None,
    severity: str | None = None,
):

    incident_id_ctx.set(incident_id)
    workflow_id_ctx.set(workflow_id)
    service_ctx.set(service)
    severity_ctx.set(severity)


def enrich_current_span():

    span = trace.get_current_span()

    if not span.is_recording():
        return

    if incident_id := incident_id_ctx.get():
        span.set_attribute(
            "incident.id",
            incident_id,
        )

    if workflow_id := workflow_id_ctx.get():
        span.set_attribute(
            "workflow.id",
            workflow_id,
        )

    if service := service_ctx.get():
        span.set_attribute(
            "incident.service",
            service,
        )

    if severity := severity_ctx.get():
        span.set_attribute(
            "incident.severity",
            severity,
        )