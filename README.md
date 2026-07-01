# 🤖 AgentOps AI

> **Production-Grade Autonomous Incident Response Platform orchestrated by LangGraph.**

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Orchestrator](https://img.shields.io/badge/orchestrator-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Observability](https://img.shields.io/badge/observability-Langfuse%20%2B%20OpenTelemetry-purple.svg)](https://langfuse.com/)
[![Local Cloud](https://img.shields.io/badge/local--cloud-LocalStack-gold.svg)](https://localstack.cloud/)

AgentOps AI is an advanced, production-grade autonomous incident response platform designed to automate the entire lifecycle of system and infrastructure incidents. Utilizing a multi-agent workflow orchestrated via **LangGraph**, the system ingests live cloud alerts, gathers system/application logs and metrics deterministically, retrieves runbooks and historical case-histories via a vector database, performs root-cause analysis (RCA), recommends remediation actions, runs sandboxed validation checks, stops for human-in-the-loop (HITL) approval, and automatically generates pull requests.

---

## 🧭 Core Architectural Philosophy

Our design is grounded in three core engineering principles:

1. **Deterministic Context Collection**: Agents should never make arbitrary API calls to fetch logs, traces, or metrics. Instead, dedicated, robust integrations gather evidence beforehand and structure it deterministically into the incident workspace.
2. **AI for Reasoning & Judgment**: Large Language Models (LLMs) are reserved strictly for high-level reasoning, classification, synthesis, and planning.
3. **Reproducible Local Infrastructure**: The entire environment (AWS LocalStack, PostgreSQL with pgvector, Redis, Jaeger OpenTelemetry, and Langfuse) runs out-of-the-box via Docker Compose, eliminating developer setup overhead.

---

## 🏗️ System Architecture

The platform operates on a decoupled event-driven architecture, starting from cloud infrastructure alarms down to automatic pull requests:

```text
       AWS CloudWatch Alarm
                │
                ▼
      AWS EventBridge Rules
                │
                ▼
          AWS SQS Queue
                │
                ▼
   services/incident-engine (Worker)
                │
                ▼ (Saves Incident & Collects Evidence)
       PostgreSQL Database
                │
                ▼
      Workflow State Machine
    ┌─────────────────────────┐
    │  LangGraph Orchestration│
    │                         │
    │  1. Collect Evidence    │
    │           │             │
    │  2. Triage Incident     │
    │           │             │
    │  3. RAG Retrieval       │
    │           │             │
    │  4. RCA Diagnosis       │
    │           │             │
    │  5. Remediation Plan    │
    │           │             │
    │  6. Sandbox Validation  │
    │           │             │
    │  7. Human Approval Inter.│
    │           │             │
    │  8. GitHub PR Autom.    │
    └─────────────────────────┘
                │
                ├── [Langfuse (Traces & LLM Costs)]
                └── [Jaeger (OTLP Distributed Traces)]
```

### 🧠 The LangGraph Agentic Workflow

The core processing engine is implemented as a stateful `StateGraph` in LangGraph, implementing conditional routing and human-in-the-loop hooks:

- **Collect Evidence Node**: Collects CloudWatch logs, CPU/Memory metrics, and git deployment context.
- **Triage Agent**: Classifies the incident severity, maps it to a team category, and assigns an engineering owner.
- **Retrieve Knowledge**: Queries historical incident memories and Markdown runbooks using cosine similarity embeddings.
- **RCA Agent**: Diagnoses the exact root-cause from logs, metrics, and retrieved runbooks.
- **Remediation Agent**: Recommends config patches, code adjustments, or manual interventions.
- **Validator Agent**: Runs tests and validates potential patches inside safe runtime environments.
- **Human-in-the-Loop Interrupt**: Halts the workflow execution, persisting state to PostgreSQL, waiting for human approval before committing code/actions.
- **Execution / GitHub Agent**: Creates automated Pull Requests with the validated fix.

---

## ⚡ Key Highlights & Capabilities

* **Multi-Agent Systems**: Modular, single-purpose LLM agents specialized in Triage, RCA, and Fix Generation.
* **Stateful Orchestration**: LangGraph-based workflow allows recovery, checkpointing, and branch logic.
* **pgvector RAG & Memory**: Employs Postgres pgvector for semantic search over technical runbooks, postmortems, and historical incidents.
* **Human-in-the-Loop (HITL)**: Interactive step approvals built using LangGraph interrupts to prevent unsafe deployments.
* **Observability Suite**:
  * **OpenTelemetry & Jaeger**: Distributed tracing for latency, API bottlenecks, and queue processing.
  * **Langfuse**: Detailed tracking of prompts, LLM outputs, token usage, and financial cost statistics.
* **Production-Style Evaluation Framework**: Custom benchmark execution engine running against 25+ real-world production incident scenarios (e.g., OOM kills, N+1 query slowdowns, bad SQL, Redis evictions).
* **Local-first Event pipeline**: Simulates full CloudWatch event routing to SQS via LocalStack.

---

## 📦 Repository Structure

The monorepo structure is organized around domain capabilities to ensure high modularity:

```text
agentops-ai/
├── apps/
│   └── api/                    # FastAPI web server hosting Incident, Approval, and Runbook endpoints
├── services/
│   ├── incident_worker/        # Background queue consumer listening to SQS events
│   └── eval-engine/            # LLM-as-a-Judge benchmark suite and report generator
├── packages/
│   ├── agents/                 # Specialized Agent prompt systems (Triage, RCA, Remediation, Validation)
│   ├── workflows/              # LangGraph state machine definitions, routers, nodes, and checkpointers
│   └── shared/                 # Database repositories, schemas, settings, and telemetry utilities
├── datasets/
│   └── benchmarks/             # 25 production incident benchmark testbeds (Kubernetes, Postgres, etc.)
├── infra/
│   ├── docker/                 # Container definition files
│   ├── localstack/             # LocalStack event configuration files
│   └── bootstrap/              # Automation scripts for creating queues and event rules
├── docs/                       # Detailed specifications for state, schema, database, and system architecture
└── reports/                    # Generated benchmark execution summaries (Markdown/JSON)
```

---

## 🛠️ Tech Stack

| Domain | Technology / Tool |
|---|---|
| **Agentic Framework** | [LangGraph](https://github.com/langchain-ai/langgraph) / [LangChain](https://github.com/langchain-ai/langchain) |
| **LLM Model** | Ollama (Qwen 3 8B / Llama 3) |
| **Service Engine** | FastAPI, Celery, Redis |
| **Infrastructure Services** | SQS, CloudWatch, EventBridge via LocalStack |
| **Database & Vector Store** | PostgreSQL + pgvector extension |
| **Observability** | Langfuse (AI Tracing) & OpenTelemetry + Jaeger (Service Tracing) |
| **Environment Management** | `uv` package manager, Docker Compose |

---

## 🚀 Getting Started

### 📋 Prerequisites
Make sure you have [Docker & Docker Compose](https://www.docker.com/) and [uv](https://github.com/astral-sh/uv) installed.

### 1. Launch Services
Spin up local AWS resources, databases, tracing, and dashboard systems:
```bash
docker compose up -d
```

### 2. Install Project Dependencies
Synchronize project-wide Python packages:
```bash
uv sync
```

### 3. Bootstrap LocalStack Resources
Create the SQS queues and EventBridge routing rules inside LocalStack:
```bash
bash infra/bootstrap/create_resources.sh
```

### 4. Run the Incident Engine
Start the worker process that consumes incoming SQS incidents:
```bash
uv run python services/incident_worker/worker.py
```

### 5. Trigger a Synthetic Alarm
Publish a mock CloudWatch alarm event to LocalStack:
```bash
aws --endpoint-url=http://localhost:4566 \
    sqs send-message \
    --queue-url http://localhost:4566/000000000000/incident-events \
    --message-body "$(cat infra/bootstrap/sample_alarm_event.json)"
```

---

## ⚖️ Evaluation & Benchmarking

The project comes packaged with a comprehensive evaluation suite to measure agent accuracy. It executes the **actual** LangGraph workflow against real scenarios rather than mocking outputs, using a **GPT-4 / Claude / Ollama** model as an LLM Judge.

To execute the suite:
```bash
cd services/eval-engine
uv run python run_suite.py
```

### Generated Reports
After completion, the engine produces detailed reports in `reports/benchmark-report.md`:
```text
✓ Loaded Benchmark
✓ Executed Real Workflow
✓ Evaluated
--------------------------------
Expected RCA: Container OOMKilled (Exit Code 137) because memory footprint exceeded 512MB.
Predicted RCA: Process terminated by kernel OOM killer (exit code 137). Memory footprint exceeded limit.
Score: 0.95
Reason: Identified exit code and memory limit discrepancy correctly.
PASS (95%)
```

---

## 🔮 Future Enhancements

* **Persistent Memory Retrieval**: Vector storage memory tracking across resolved incidents.
* **Model Cost Guardrails**: Budget limitations per-agent and per-workflow to halt runaways.
* **Interactive Next.js Dashboard**: Visual management of active incidents, approval interrupts, and cost stats.
* **Kubernetes Operator Deployment**: Moving the background runner onto active staging EKS clusters.

---

## 📄 License

This repository is available under the [MIT License](LICENSE).
