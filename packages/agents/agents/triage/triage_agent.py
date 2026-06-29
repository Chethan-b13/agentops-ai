from .triage_schema import (
    TriageResultSchema,
)
from .prompts import build_triage_messages
from shared.llm import LLMClient

class TriageAgent:

    def __init__(self):

        self.llm = LLMClient(
            output_schema=TriageResultSchema,
        )

    def classify(self, incident: dict, evidence: list[dict]) -> TriageResultSchema:

        messages = build_triage_messages(
            incident,
            evidence,
        )

        return self.llm.invoke(
            messages,
            generation_name="Triage Agent",
            metadata={
                "agent": "triage",
                "prompt_version": "v1",
            },
        )