from contextvars import ContextVar

from langfuse.client import StatefulTraceClient

langfuse_trace_ctx: ContextVar[
    StatefulTraceClient | None
] = ContextVar(
    "langfuse_trace",
    default=None,
)


def set_current_trace(
    trace: StatefulTraceClient,
) -> None:

    langfuse_trace_ctx.set(trace)


def get_current_trace() -> StatefulTraceClient | None:

    return langfuse_trace_ctx.get()