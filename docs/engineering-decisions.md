# Engineering Decisions

This document explains the key architectural decisions made while building **AgentOps AI**, the trade-offs considered, and the reasoning behind each implementation.

---

# Design Philosophy

The goal of this project was **not** to build another AI chatbot.

Instead, the objective was to demonstrate modern production AI engineering patterns:

- Event-driven architectures
- Multi-agent orchestration
- Deterministic evidence collection
- Human-in-the-loop workflows
- AI observability
- Evaluation-driven development

Every major design decision was made with those goals in mind.

---

# 1. Event-Driven Architecture

## Decision

Use an event-driven pipeline:

```
CloudWatch Alarm
        ↓
EventBridge
        ↓
SQS
        ↓
Incident Worker
```

instead of exposing a REST endpoint directly to an LLM workflow.

## Why

Production infrastructure incidents are asynchronous.

CloudWatch emits alarms rather than users manually invoking AI agents.

Using EventBridge and SQS mirrors real production systems while providing:

- loose coupling
- retry capability
- horizontal scalability
- fault isolation

---

# 2. Deterministic Evidence Collection

## Decision

Evidence is collected before any AI reasoning begins.

Collectors gather:

- Logs
- Metrics
- Deployments
- Incident metadata

Agents never fetch infrastructure data directly.

## Why

LLMs should reason.

They should not perform infrastructure operations.

Separating evidence collection from reasoning provides:

- reproducibility
- auditability
- deterministic workflows
- reduced hallucinations

---

# 3. Multi-Agent Architecture

## Decision

Instead of one large prompt, the workflow is decomposed into specialized agents.

Current agents:

- Triage
- Knowledge Retrieval
- Root Cause Analysis
- Remediation
- Validation

## Why

Each agent owns a single responsibility.

Benefits include:

- simpler prompts
- easier evaluation
- modular development
- easier debugging
- agent replacement without affecting the workflow

---

# 4. LangGraph Instead of Sequential Chains

## Decision

Use LangGraph StateGraph to orchestrate the workflow.

## Why

LangGraph provides:

- explicit state transitions
- checkpointing
- interrupts
- resumability
- deterministic execution

This more closely resembles production orchestration engines than linear LLM chains.

---

# 5. Structured Outputs Everywhere

## Decision

Every agent returns Pydantic schemas instead of free-form text.

Examples:

- TriageResult
- RCAResult
- RemediationPlan
- ValidationResult

## Why

Structured outputs are:

- machine readable
- easier to validate
- easier to persist
- easier to evaluate
- easier to consume by downstream systems

---

# 6. Human-in-the-Loop

## Decision

The workflow pauses before execution.

A human approves remediation before automation continues.

## Why

Production systems should not execute infrastructure changes autonomously.

Human approval:

- reduces operational risk
- increases trust
- provides accountability
- mirrors enterprise workflows

---

# 7. GitHub Pull Requests Instead of Direct Changes

## Decision

The system creates Pull Requests rather than modifying production systems.

## Why

Infrastructure changes should remain reviewable.

Pull Requests provide:

- code review
- audit history
- rollback capability
- collaboration

---

# 8. LocalStack Instead of AWS

## Decision

The complete AWS event pipeline is simulated locally.

Services include:

- CloudWatch
- EventBridge
- SQS

## Why

Benefits include:

- zero AWS cost
- reproducible development
- offline testing
- easier demonstrations

---

# 9. Langfuse + OpenTelemetry

## Decision

Every workflow is instrumented.

Observability stack:

- Langfuse
- OpenTelemetry
- Jaeger

## Why

AI systems require observability similar to distributed systems.

Collected telemetry includes:

- prompts
- responses
- latency
- traces
- spans
- workflow execution

This greatly simplifies debugging and evaluation.

---

# 10. Evaluation-Driven Development

## Decision

The system is continuously evaluated using synthetic production incidents.

The evaluation framework includes:

- 25 benchmark incidents
- LLM-as-a-Judge
- Langfuse Experiments

## Why

Traditional unit tests are insufficient for LLM systems.

Evaluation provides measurable quality improvements over time.

---

# 11. Prompt Engineering Evolution

## Initial Problem

Early RCA responses were technically correct but overly generic.

Examples included:

- "Database issue"
- "Memory leak"

These lacked enough specificity for operational incident response.

---

## Improvement

The RCA prompt was redesigned to require:

- component identification
- precise failure mechanism
- evidence-backed explanation

Example:

Instead of:

```
Memory leak
```

The model now generates:

```
image-processor buffer cache retaining processed image binaries preventing garbage collection
```

---

## Evaluation Improvements

The LLM judge was also redesigned.

Instead of holistic scoring, evaluation now measures:

| Criterion | Weight |
|-----------|-------:|
| Component Match | 50% |
| Failure Mechanism | 30% |
| Symptom / Context | 20% |

This rewards technically accurate diagnoses rather than superficial semantic similarity.

---

## Result

| Metric | Before | After |
|---------|-------:|------:|
| Benchmarks Passed | 5 | 13 |
| Accuracy | 20% | 52% |

The improvement came from producing more operationally useful root cause analyses rather than simply optimizing for benchmark wording.

---

# 12. Current Limitations

The project intentionally simplifies several production concerns.

Current limitations include:

- Mock evidence collectors
- Limited operational knowledge corpus
- Static RAG documents
- Synthetic benchmark incidents
- Local infrastructure only

These choices keep the project self-contained while demonstrating the overall architecture.

---

# 13. Future Improvements

Potential next steps include:

- pgvector hybrid retrieval
- Real CloudWatch integration
- Kubernetes deployment
- CI benchmark regression testing
- Slack notifications
- Cost guardrails
- Multi-environment deployments

---

# Lessons Learned

The most important lesson from this project is that building reliable AI systems is less about prompting and more about engineering.

Successful AI systems require:

- deterministic inputs
- structured outputs
- orchestration
- observability
- evaluation
- human oversight

Prompt engineering alone is not enough.

Reliable AI applications are built through iterative measurement, evaluation, and continuous improvement.