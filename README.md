# 🤖 AgentOps AI

> **Production-Grade Autonomous Incident Response Platform built with LangGraph**

<p align="center">
Build autonomous AI systems that investigate infrastructure incidents end-to-end using a production-inspired multi-agent architecture.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-orange" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" />
  <img src="https://img.shields.io/badge/PostgreSQL-pgvector-blue" />
  <img src="https://img.shields.io/badge/Langfuse-Observability-purple" />
  <img src="https://img.shields.io/badge/OpenTelemetry-Tracing-informational" />
  <img src="https://img.shields.io/badge/LocalStack-AWS%20Simulation-yellow" />
</p>

------------------------------------------------------------------------

# 🚀 Overview

AgentOps AI is an end-to-end autonomous incident response platform
demonstrating modern AI engineering patterns.

Instead of building another chatbot, this project automates the
lifecycle of infrastructure incidents:

-   Receives AWS CloudWatch alarms
-   Collects evidence deterministically
-   Performs AI-powered triage
-   Retrieves historical knowledge (RAG)
-   Performs Root Cause Analysis
-   Generates remediation plans
-   Validates proposed fixes
-   Pauses for Human Approval
-   Creates GitHub Pull Requests
-   Evaluates itself using synthetic production benchmarks

------------------------------------------------------------------------

# ✨ Highlights

  Capability                             Status
  -------------------------------------- --------
  LangGraph Multi-Agent Workflow         ✅
  AWS Event-Driven Architecture          ✅
  Human-in-the-Loop                      ✅
  GitHub PR Automation                   ✅
  OpenTelemetry Tracing                  ✅
  Langfuse LLM Observability             ✅
  Local AWS via LocalStack               ✅
  Evaluation Framework (25 Benchmarks)   ✅

------------------------------------------------------------------------

# 🏗 Architecture

<!-- <img src="./screenshots/architecture.png"> -->

```mermaid
flowchart LR

%% =========================
%% Event Pipeline
%% =========================

subgraph AWS["AWS (LocalStack)"]
    CW[CloudWatch Alarm]
    EB[EventBridge]
    SQS[SQS Queue]
end

Worker[Incident Worker]

%% =========================
%% Context Collection
%% =========================

subgraph Context["Context Collection"]
    Logs[Logs Collector]
    Metrics[Metrics Collector]
    Deployments[Deployments Collector]
end

%% =========================
%% Storage
%% =========================

subgraph Storage["PostgreSQL"]
    Incidents[(Incidents)]
    Evidence[(Incident Evidence)]
    Runbooks[(Runbooks)]
    Workflow[(Workflow Checkpoints)]
end

%% =========================
%% AI Workflow
%% =========================

subgraph LangGraph["LangGraph Workflow"]
    Triage[Triage Agent]
    Retrieval[Knowledge Retrieval]
    RCA[Root Cause Analysis]
    Fix[Remediation Agent]
    Validation[Validation Agent]
    HITL{"Human Approval"}
    GitHub[GitHub Pull Request]
end

%% =========================
%% Observability
%% =========================

subgraph Observability["Observability"]
    Langfuse[Langfuse]
    OTel[OpenTelemetry]
    Jaeger[Jaeger]
end

%% Event Flow
CW --> EB
EB --> SQS
SQS --> Worker

%% Evidence Collection
Worker --> Logs
Worker --> Metrics
Worker --> Deployments

Logs --> Evidence
Metrics --> Evidence
Deployments --> Evidence

Worker --> Incidents

%% AI Workflow
Evidence --> Triage
Runbooks --> Retrieval
Triage --> Retrieval
Retrieval --> RCA
RCA --> Fix
Fix --> Validation
Validation --> HITL
HITL --> GitHub

%% Persistence
LangGraph --> Workflow

%% Observability
LangGraph -. Traces .-> Langfuse
LangGraph -. Spans .-> OTel
OTel --> Jaeger
```
---

## 🧠 LangGraph Workflow

![Workflow](assets/langgraph-workflow.png)

---

## 📊 Evaluation

![Benchmark Results](assets/benchmark-results.png)

---

## 🔭 Observability

### Langfuse

![Langfuse](assets/langfuse-trace.png)

![Langfuse-llm-call](assets/langfuse-llm-call-trace.png)

![Langfuse-experiment](assets/langfuse-experiment.png)

### Jaeger

![Jaeger](assets/jaeger-trace.png)

---

## 🎥 Demo

![Demo](assets/demo.gif)

------------------------------------------------------------------------

# 🧠 LangGraph Workflow

1.  Evidence Collection
2.  Incident Triage
3.  Knowledge Retrieval (RAG)
4.  Root Cause Analysis
5.  Remediation Planning
6.  Validation
7.  Human Approval
8.  GitHub Pull Request Creation

------------------------------------------------------------------------

# 📊 Evaluation

The project includes a production-style evaluation framework.

-   25 synthetic production incidents
-   LLM-as-a-Judge evaluation
-   Langfuse Experiments
-   Root Cause Accuracy scoring
-   Detailed benchmark reports

Current benchmark coverage includes:

-   Kubernetes
-   PostgreSQL
-   Redis
-   AWS
-   Networking
-   Application failures

------------------------------------------------------------------------

# 🔭 Observability

Every workflow execution is fully observable.

-   Langfuse traces
-   Prompt & response logging
-   Token usage
-   Agent latency
-   OpenTelemetry spans
-   Jaeger distributed tracing

------------------------------------------------------------------------

# 🛠 Tech Stack

  Category          Technology
  ----------------- -----------------------------------
  Agent Framework   LangGraph
  LLM               Ollama (Qwen3 8B)
  Backend           FastAPI
  Queue             SQS + EventBridge
  Database          PostgreSQL + pgvector
  Observability     Langfuse + OpenTelemetry + Jaeger
  Infrastructure    Docker + LocalStack
  Evaluation        Langfuse Experiments

------------------------------------------------------------------------

# 📁 Repository Structure

``` text
apps/
services/
packages/
datasets/
infra/
docs/
reports/
```

------------------------------------------------------------------------

# 🚀 Getting Started

``` bash
docker compose up -d

uv sync

bash infra/bootstrap/create_resources.sh

uv run python services/incident_worker/worker.py
```

------------------------------------------------------------------------

# 📈 What This Project Demonstrates

-   Multi-Agent AI Systems
-   LangGraph Orchestration
-   Retrieval-Augmented Generation (RAG)
-   Human-in-the-Loop Workflows
-   AI Observability
-   Event-Driven Architecture
-   Evaluation Frameworks
-   Production-inspired Backend Engineering

------------------------------------------------------------------------

# 🔮 Production Roadmap

-   Real CloudWatch integrations
-   Dynamic pgvector retrieval
-   CI benchmark regression testing
-   Cost guardrails
-   Kubernetes deployment
-   Slack integration

------------------------------------------------------------------------

# 📄 License

MIT
