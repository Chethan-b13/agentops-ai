# LangGraph State Design

## Purpose

The LangGraph state represents the shared workflow context used during incident investigation.

The state is not a database.

The state is not memory.

The state is not knowledge storage.

The state only contains the information required for workflow execution.

---

# Core Principle

State should contain only the minimum information required for the next workflow step.

Large datasets such as logs, traces, metrics, and documents must remain in storage and be referenced when needed.

---

# IncidentState

```python
from typing import TypedDict
from langchain_core.messages import BaseMessage


class IncidentState(TypedDict):

    incident_id: str

    messages: list[BaseMessage]

    evidence_ids: list[str]

    knowledge_ids: list[str]

    reasoning_trace: list[dict]

    triage_result: dict | None

    rca_result: dict | None

    fix_plan: dict | None

    validation_result: dict | None

    approval_status: str

    resolution_status: str
```

---

# State Ownership

## Triage Agent

Reads:

* incident
* evidence

Writes:

* triage_result

---

## RCA Agent

Reads:

* incident
* evidence
* triage_result
* knowledge

Writes:

* rca_result

---

## Fix Agent

Reads:

* incident
* rca_result
* knowledge

Writes:

* fix_plan

---

## Validator

Reads:

* fix_plan

Writes:

* validation_result

---

## Human Approval

Reads:

* fix_plan
* validation_result

Writes:

* approval_status

---

# Runtime Messages

Messages exist only for the current workflow execution.

Examples:

* Agent reasoning
* Tool outputs
* Human feedback

Messages are not long-term memory.

Messages are not stored as incident knowledge.

---

# Evidence References

Evidence is stored outside state.

Examples:

* Logs
* Metrics
* Traces
* Deployment Events

State stores references:

```python
evidence_ids = [
    "evidence-001",
    "evidence-002"
]
```

This keeps checkpoints lightweight.

---

# Knowledge References

Knowledge comes from:

* Runbooks
* Postmortems
* Historical Incidents
* Architecture Documentation

State stores references to retrieved knowledge.

---

# Checkpointing

LangGraph checkpoints persist workflow execution.

Examples:

* Human Approval
* Process Restart
* Failure Recovery

Checkpoint data should remain small and efficient.

---

# Architecture Rule

State is execution context.

Memory is learned experience.

Knowledge is retrieved information.

Storage is the source of truth.

These concerns must remain separated.
