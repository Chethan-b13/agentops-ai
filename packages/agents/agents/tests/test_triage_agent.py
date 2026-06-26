from agents.triage.triage_agent import (
    TriageAgent,
)

agent = TriageAgent()

result = agent.classify(
    incident={
        "service": "payments-api",
        "metric_name": "CPUUtilization",
    },
    evidence=[
        {
            "type": "logs",
            "entries": [
                "Database connection timeout",
                "Database connection timeout",
                "Connection pool exhausted",
            ],
        },
        {
            "type": "metrics",
            "cpu": 94,
        },
    ],
)

print(result)