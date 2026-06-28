from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from shared.settings import settings

from .prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)

from .rca_schema import RCAResultSchema


class RCAAgent:

    def __init__(self):

        self.llm = (
            ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0,
            )
            .with_structured_output(
                RCAResultSchema
            )
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