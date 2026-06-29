from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from shared.llm import LLMClient

from .prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)
from .validation_schema import (
    ValidationResultSchema,
)


class ValidationAgent:

    def __init__(self):

        self.llm = LLMClient(
            output_schema=ValidationResultSchema,
        )

    def validate(
        self,
        incident_context,
        evidence_context,
        knowledge_context,
        triage_context,
        rca_context,
        remediation_context,
    ) -> ValidationResultSchema:

        prompt = build_prompt(
            incident_context,
            evidence_context,
            knowledge_context,
            triage_context,
            rca_context,
            remediation_context,
        )

        return self.llm.invoke(
            [
                SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                HumanMessage(
                    content=prompt
                ),
            ],
            generation_name="Validation Agent",
            metadata={
                "agent": "validation",
                "prompt_version": "v1",
            },
        )