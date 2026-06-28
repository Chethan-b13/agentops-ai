from langchain_ollama import ChatOllama

from .triage_schema import (
    TriageResultSchema,
)
from .prompts import build_triage_messages
from shared.settings import settings

class TriageAgent:

    def __init__(self):

        llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )

        self.llm = llm.with_structured_output(
            TriageResultSchema
        )

    def classify(self, incident: dict, evidence: list[dict]) -> TriageResultSchema:

        messages = build_triage_messages(
            incident,
            evidence,
        )

        return self.llm.invoke(messages)