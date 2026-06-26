from typing import TypedDict


class TriageState(TypedDict):
    incident_id: str

    incident: dict

    evidence: list[dict]

    triage_result: dict | None