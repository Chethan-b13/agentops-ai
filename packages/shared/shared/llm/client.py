from typing import Type

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from shared.observability import get_current_trace
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
        *,
        generation_name: str,
        metadata: dict | None = None,
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

            trace = get_current_trace()

            generation = None

            if trace:

                generation = trace.generation(
                    name=generation_name,
                    model=self.model_name,
                    input=[m.model_dump() for m in messages],
                    metadata={
                        "provider": "ollama",
                        "temperature": 0,
                        **(metadata or {}),
                    },
                )

            try:

                response = self.llm.invoke(messages)

                if generation:

                    generation.end(
                        output=response.model_dump(),
                    )

                return response

            except Exception as ex:

                if generation:

                    generation.end(
                        level="ERROR",
                        status_message=str(ex),
                    )

                raise