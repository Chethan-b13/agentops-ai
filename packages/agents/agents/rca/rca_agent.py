from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from shared.llm import LLMClient

from .prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)

from .rca_schema import RCAResultSchema


class RCAAgent:

    def __init__(self):

        self.llm = LLMClient(
            output_schema=RCAResultSchema,
        )

    def analyze(
        self,
        incident_context,
        evidence_context,
        knowledge_context,
        triage_context,
    ) -> RCAResultSchema:

        prompt = build_prompt(
            incident_context,
            evidence_context,
            knowledge_context,
            triage_context,
        )

        return self.llm.invoke(
            [
                SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                HumanMessage(
                    content=prompt,
                ),
            ]
        )