from langgraph.types import Command

from worker import (
    graph,
)

incident_id = input("Incident ID: ")

config = {
    "configurable": {
        "thread_id": incident_id,
    }
}

state = graph.invoke(
    Command(
        resume="approved",
    ),
    config=config,
)

print(state)