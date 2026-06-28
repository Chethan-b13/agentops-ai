from enum import Enum

from pydantic import BaseModel


class ValidationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class ValidationResultSchema(BaseModel):
    status: ValidationStatus

    summary: str

    findings: list[str]

    recommendations: list[str]

    confidence: float