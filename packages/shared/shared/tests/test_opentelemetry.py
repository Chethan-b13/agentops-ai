import time

from shared.telemetry import initialize_tracing, trace_span


@trace_span("Hello Span")
def do_work():

    print("Working...")

    time.sleep(2)

import time

from shared.telemetry import initialize_tracing, trace_span


@trace_span("Failing Span")
def do_work_with_exception():

    time.sleep(1)

    raise RuntimeError("Database connection timeout")

def main():

    initialize_tracing(
        service_name="agentops-worker",
    )

    do_work()

    print("work Done")

    do_work_with_exception()

    print("exception Done")

if __name__ == "__main__":
    main()