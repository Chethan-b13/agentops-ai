# Database Schema

## Purpose

PostgreSQL is the primary datastore for AgentOps AI.

The database serves four purposes:

1. Incident Storage
2. Evidence Storage
3. Knowledge Storage
4. Workflow Persistence

pgvector is used for semantic retrieval.

---

# Architecture Overview

PostgreSQL

├── Operational Data

├── Knowledge Data

├── Workflow Data

└── Observability Data

---

# incidents

Stores incident metadata.

```sql
incidents
```

Columns:

```text
id

alarm_name

service

region

metric_name

threshold

current_value

severity

source

status

created_at

updated_at
```

---

# incident_evidence

Stores evidence collected during investigation.

```sql
incident_evidence
```

Columns:

```text

id

incident_id

evidence_type

source

raw_data (JSONB)

summary_data (JSONB)

created_at
```

Evidence Types:

```text
logs

metrics

traces

deployments
```

---

# workflow_runs

Stores LangGraph workflow executions.

```sql
workflow_runs
```

Columns:

```text
id

incident_id

workflow_status

current_node

started_at

completed_at
```

Example:

```text
waiting_for_approval
```

This enables workflow recovery.

---

# approvals

Stores Human-In-The-Loop decisions.

```sql
approvals
```

Columns:

```text
id

incident_id

status

approved_by

comments

created_at
```

Status:

```text
pending

approved

rejected
```

---

# incident_memory

Stores resolved incidents for future retrieval.

```sql
incident_memory
```

Columns:

```text
id

incident_id

root_cause

fix

outcome

embedding

created_at
```

Purpose:

Future incidents can retrieve previous solutions.

---

# runbooks

Stores operational runbooks.

```sql
runbooks
```

Columns:

```text
id

title

content

embedding

created_at
```

---

# postmortems

Stores historical outage investigations.

```sql
postmortems
```

Columns:

```text
id

title

content

embedding

created_at
```

---

# reasoning_traces

Stores structured agent decisions.

```sql
reasoning_traces
```

Columns:

```text
id

incident_id

agent_name

decision

confidence

evidence_ids

created_at
```

Purpose:

Observability and evaluation.

---

# agent_runs

Stores agent execution metadata.

```sql
agent_runs
```

Columns:

```text
id

incident_id

agent_name

model

latency_ms

tokens_input

tokens_output

cost

created_at
```

Purpose:

Performance and cost tracking.

---

# evaluation_runs

Stores benchmark execution results.

```sql
evaluation_runs
```

Columns:

```text
id

incident_id

expected_root_cause

predicted_root_cause

accuracy

resolution_time

created_at
```

Purpose:

Phase 17 evaluation framework.

---

# Vector Search

pgvector is used only for semantic knowledge.

Included tables:

* incident_memory
* runbooks
* postmortems

Excluded:

* logs
* metrics
* traces

Operational evidence is not embedded.

---

# Design Principles

1. State is not stored as evidence.

2. Evidence is stored separately from workflow state.

3. Semantic knowledge uses embeddings.

4. Workflow executions must be recoverable.

5. Every agent decision should be observable.

6. Human approval must be auditable.
