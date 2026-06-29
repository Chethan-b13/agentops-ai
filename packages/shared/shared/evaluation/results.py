from pydantic import BaseModel


class WorkflowResult(BaseModel):
    incident_id: str

    triage: dict

    rca: dict

    remediation: dict

    validation: dict

    latency_ms: float