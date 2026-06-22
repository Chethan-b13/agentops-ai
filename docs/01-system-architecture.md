# AgentOps AI - System Architecture

## Vision

AgentOps AI is a production-grade autonomous incident response platform.

The system receives infrastructure incidents, gathers evidence, performs root cause analysis, recommends fixes, validates solutions, and requests human approval before taking actions.

---

# Core Design Principles

## Principle 1

Deterministic systems collect evidence.

Agents never fetch logs, metrics, traces, or infrastructure data.

Evidence collection is handled by dedicated services.

---

## Principle 2

Agents reason over evidence.

LLMs are only used when judgment, reasoning, or decision-making is required.

---

## Principle 3

Infrastructure is reproducible.

All AWS resources inside LocalStack must be created through bootstrap scripts or infrastructure-as-code.

Manual resource creation is not allowed.

---

# High-Level Architecture
```
CloudWatch Alarm

↓

EventBridge

↓

SQS

↓

Incident Consumer

↓

PostgreSQL

↓

Context Collector

↓

Evidence Store

↓

LangGraph Workflow

↓

Human Approval

↓

GitHub Automation

---

# LangGraph Workflow

Supervisor

↓

Triage Agent

↓

Root Cause Analysis Agent

↓

Fix Recommendation Agent

↓

Validator Service

↓

Human Approval
```
---

# Agent Responsibilities

## Triage Agent

Inputs:

* Incident
* Evidence

Outputs:

* Severity
* Category
* Owner

---

## RCA Agent

Inputs:

* Incident
* Evidence
* Retrieved Knowledge

Outputs:

* Root Cause
* Confidence Score

---

## Fix Recommendation Agent

Inputs:

* Root Cause
* Retrieved Knowledge

Outputs:

* Remediation Plan

---

## Validator Service

Inputs:

* Remediation Plan

Outputs:

* PASS
* FAIL

with explanation.

---

# Evidence Collection Layer

The Context Collector gathers:

* CloudWatch Metrics
* CloudWatch Logs
* AWS Traces
* Deployment History
* Historical Incidents
* Runbooks
* Postmortems

This layer is deterministic and contains no LLM logic.

---

# Knowledge Layer

Knowledge sources include:

* Runbooks
* Postmortems
* Architecture Documentation
* Historical Incidents

Knowledge is stored using PostgreSQL and pgvector.

---

# Human-In-The-Loop

All potentially dangerous actions require human approval.

The system must never automatically deploy fixes or merge pull requests.

---

# Long-Term Architecture Goals

* Multi-Agent System
* MCP Integration
* Memory
* Evaluation Framework
* OpenTelemetry
* Langfuse
* Cost Tracking
* Agent-to-Agent Communication
* Production Deployment
