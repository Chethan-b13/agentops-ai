from typing import Any

from pydantic import BaseModel


class BenchmarkMetadata(BaseModel):
    author: str
    created_at: str
    notes: str


class IncidentData(BaseModel):
    service: str
    severity: str
    region: str


class EvidenceData(BaseModel):
    logs: list[str]
    metrics: dict[str, Any]


class ExpectedTriage(BaseModel):
    severity: str
    category: str
    owner: str


class ExpectedRCA(BaseModel):
    root_cause: str


class ExpectedValidation(BaseModel):
    passed: bool


class ExpectedOutputs(BaseModel):
    triage: ExpectedTriage
    rca: ExpectedRCA
    remediation: list[str]
    validation: ExpectedValidation


class Benchmark(BaseModel):
    id: str
    name: str
    description: str

    tags: list[str]
    difficulty: str
    source: str
    version: int

    metadata: BenchmarkMetadata

    incident: IncidentData

    evidence: EvidenceData

    expected_outputs: ExpectedOutputs