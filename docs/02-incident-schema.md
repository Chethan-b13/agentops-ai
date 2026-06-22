# Incident Schema

## Purpose

The Incident schema represents the source-of-truth record for an infrastructure incident.

An Incident is not merely a CloudWatch alarm.

An Incident represents the entire investigation case created from an infrastructure event.

The alarm acts as the trigger, while the incident becomes the lifecycle record that moves through triage, root-cause analysis, remediation, validation, approval, and resolution.

---

# Incident Lifecycle

```
CloudWatch Alarm

↓

Incident Created

↓

Evidence Collected

↓

Triage

↓

Root Cause Analysis

↓

Fix Recommendation

↓

Validation

↓

Human Approval

↓

Resolution

```


# Incident Model

```python
from typing import TypedDict


class Incident(TypedDict):
    incident_id: str

    alarm_name: str

    service: str

    region: str

    metric_name: str

    threshold: float

    current_value: float

    severity: str

    source: str

    status: str

    created_at: str
```

---

# Field Definitions

## incident_id

Unique identifier for the incident.

Example:

```text
INC-000001
```

---

## alarm_name

Name of the alarm that triggered the incident.

Example:

```text
High CPU Usage
```

---

## service

Impacted service.

Example:

```text
payments-api
```

---

## region

AWS region where the incident occurred.

Example:

```text
us-east-1
```

---

## metric_name

Metric that triggered the alarm.

Examples:

```text
CPUUtilization

MemoryUtilization

RequestLatency
```

---

## threshold

Configured alarm threshold.

Example:

```text
80
```

---

## current_value

Observed value that breached the threshold.

Example:

```text
94
```

---

## severity

Incident severity level.

Possible values:

```text
unknown
low
medium
high
critical
```

Initially set to:

```text
unknown
```

Later updated by the Triage Agent.

---

## source

Origin of the incident.

Examples:

```text
cloudwatch
datadog
grafana
newrelic
```

Initial implementation:

```text
cloudwatch
```

---

## status

Current incident state.

Possible values:

```text
new

collecting_evidence

triaging

investigating

fix_recommended

awaiting_approval

approved

resolved

failed
```

---

## created_at

Timestamp when the incident was created.

Example:

```text
2026-06-21T18:35:00Z
```

---

# Retrieved Context

The incident itself contains only metadata.

Evidence is collected separately and attached to the workflow.

```python
retrieved_context = {
    "logs": {
        "raw": [],
        "summary": {}
    },

    "metrics": {
        "raw": [],
        "summary": {}
    },

    "traces": {
        "raw": [],
        "summary": {}
    },

    "deployments": [],

    "related_incidents": [],

    "runbooks": [],

    "postmortems": []
}
```

---

# Evidence Storage Strategy

Evidence should not be stored directly inside LangGraph state.

Raw evidence is stored in PostgreSQL.

Examples:

* CloudWatch Logs
* Metrics
* Traces
* Deployment Events

LangGraph state should store references to evidence rather than large payloads.

Benefits:

* Smaller checkpoints
* Faster workflow execution
* Easier debugging
* Better scalability
* Easier Human-In-The-Loop recovery

---

# Embedding Strategy

Embeddings are only generated for semantic knowledge.

Examples:

* Historical incidents
* Runbooks
* Postmortems
* Architecture documentation

Embeddings are not generated for raw logs, metrics, or traces.

These datasets are stored as operational evidence rather than semantic knowledge.

---

# Architecture Rule

Incident metadata belongs in the Incident record.

Evidence belongs in storage.

Semantic knowledge belongs in pgvector.

Workflow state contains only the minimum information required for the next workflow step.
