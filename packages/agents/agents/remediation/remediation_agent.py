from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from shared.llm import LLMClient

from .prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)
from agents.remediation.schema import RemediationPlanSchema


class RemediationAgent:

    def __init__(self):

        self.llm = LLMClient(
            output_schema=RemediationPlanSchema,
        )

    def generate(
        self,
        incident_context,
        evidence_context,
        knowledge_context,
        triage_context,
        rca_context,
    ) -> RemediationPlanSchema:

        prompt = build_prompt(
            incident_context,
            evidence_context,
            knowledge_context,
            triage_context,
            rca_context,
        )

        return self.llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ],
            generation_name="Remediation Agent",
            metadata={
                "agent": "remediation",
                "prompt_version": "v1",
            },
        )