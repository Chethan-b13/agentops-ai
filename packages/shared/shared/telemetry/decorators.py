from collections.abc import Callable
from functools import wraps
from typing import Any

from langgraph.errors import GraphInterrupt
from opentelemetry.trace import Status, StatusCode

from .tracer import get_tracer
from .context import enrich_current_span


def trace_span(span_name: str):
    """
    Decorator that wraps a function inside an OpenTelemetry span.

    Automatically:
    - Creates a span
    - Records expected workflow interrupts
    - Records unexpected exceptions
    """

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:

            tracer = get_tracer(func.__module__)

            with tracer.start_as_current_span(span_name) as span:
                
                enrich_current_span()

                try:

                    result = func(*args, **kwargs)

                    span.set_status(Status(StatusCode.OK))

                    return result

                except GraphInterrupt:

                    span.add_event(
                        "Workflow Paused",
                        {
                            "reason": "Awaiting Human Approval",
                        },
                    )

                    span.set_status(Status(StatusCode.OK))

                    raise

                except Exception as ex:

                    span.record_exception(ex)

                    span.set_status(
                        Status(
                            StatusCode.ERROR,
                            str(ex),
                        )
                    )

                    raise

        return wrapper

    return decorator