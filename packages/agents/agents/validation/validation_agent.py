from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_ollama import ChatOllama

from shared.settings import settings

from .prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)
from .validation_schema import (
    ValidationResultSchema,
)


class ValidationAgent:

    def __init__(self):

        self.llm = (
            ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0,
            )
            .with_structured_output(
                ValidationResultSchema
            )
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
            ]
        )