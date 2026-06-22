# Repository Structure

## Purpose

The repository is organized around business capabilities rather than technical layers.

Each major subsystem owns its code, tests, configuration, and dependencies.

This structure supports independent evolution of:

* Incident Processing
* Agent Workflows
* Evaluation Framework
* Dashboard
* Infrastructure

---

# Repository Layout

```text
agentops-ai/

apps/
├── api/
├── dashboard/

services/
├── incident-engine/
├── eval-engine/

packages/
├── shared/
├── agents/
├── mcp/
    ├── github_server/
    ├── aws_server/
    ├── postgres_server/

infra/
├── docker/
├── localstack/
├── bootstrap/

docs/

tests/
```

---

# apps

Applications exposed to users.

## api

FastAPI application.

Responsibilities:

* Incident APIs
* Approval APIs
* Workflow APIs
* Dashboard APIs

---

## dashboard

Next.js frontend.

Responsibilities:

* Incident List
* Incident Detail View
* Approval Screens
* Evaluation Dashboard
* Cost Dashboard

---

# services

Long-running backend services.

## incident-engine

Responsibilities:

* Consume SQS events
* Create incidents
* Trigger workflows
* Collect evidence

---

## eval-engine

Responsibilities:

* Execute benchmark incidents
* Calculate metrics
* Generate evaluation reports

---

# packages

Reusable libraries.

---

## agents

Contains all agent implementations.

Examples:

```text
triage_agent.py

rca_agent.py

fix_agent.py
```

---

## shared

Shared code used across applications.

Examples:

```text
database/

models/

settings/

logging/

telemetry/
```

---

## mcp-servers

Custom MCP servers.

Examples:

```text
github/

postgres/

aws/

slack/
```

---

# infra

Infrastructure configuration.

---

## docker

Dockerfiles.

Docker Compose.

Container configuration.

---

## localstack

LocalStack configuration.

Examples:

```text
eventbridge

sqs

cloudwatch
```

---

## bootstrap

Infrastructure initialization scripts.

Examples:

```text
create_queue.sh

create_rule.sh

create_alarm.sh
```

Purpose:

Recreate local infrastructure consistently.

---

# docs

Architecture and design documentation.

Examples:

```text
system architecture

state model

database schema

evaluation strategy
```

---

# tests

Project-wide tests.

Examples:

```text
integration

e2e

evaluation
```

---

# Architecture Principles

1. Applications remain thin.

2. Business logic belongs in services.

3. Agents live in reusable packages.

4. Infrastructure is reproducible.

5. Shared code is centralized.

6. Evaluation is treated as a first-class capability.

7. Every major subsystem should be independently testable.
