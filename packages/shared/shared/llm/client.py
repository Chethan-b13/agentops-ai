from typing import Type

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from shared.settings import settings
from shared.telemetry import get_tracer


class LLMClient:

    def __init__(
        self,
        output_schema: Type[BaseModel],
    ):

        llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )

        self.model_name = settings.ollama_model

        self.llm = llm.with_structured_output(
            output_schema,
        )

    def invoke(
        self,
        messages: list[BaseMessage],
    ):

        tracer = get_tracer(__name__)

        with tracer.start_as_current_span("LLM Call") as span:

            span.set_attribute(
                "llm.provider",
                "ollama",
            )

            span.set_attribute(
                "llm.model",
                self.model_name,
            )

            span.set_attribute(
                "llm.message_count",
                len(messages),
            )

            return self.llm.invoke(messages)