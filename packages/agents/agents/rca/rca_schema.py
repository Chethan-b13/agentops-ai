from pydantic import BaseModel, Field


class RCAResultSchema(BaseModel):

    root_cause: str = Field(
        description="Most likely root cause."
    )

    explanation: str = Field(
        description="Detailed explanation of the reasoning."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score."
    )

    supporting_evidence: list[str] = Field(
        description="Evidence supporting the conclusion."
    )