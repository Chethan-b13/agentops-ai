from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes


def initialize_tracing(
    service_name: str,
    endpoint: str = "http://localhost:4318/v1/traces",
) -> None:
    """
    Configure the global OpenTelemetry tracer provider.
    This should be called exactly once during application startup.
    """

    resource = Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: service_name,
        }
    )

    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(
        endpoint=endpoint,
    )

    processor = BatchSpanProcessor(exporter)

    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)


def get_tracer(name: str):
    """
    Return a tracer scoped to the given module/component.
    """

    return trace.get_tracer(name)