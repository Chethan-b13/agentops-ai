from typing import Type

from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from shared.observability import get_current_trace
from shared.settings import settings
from shared.telemetry import get_tracer


def _build_llm(output_schema: Type[BaseModel]):
    """Instantiate the correct LangChain chat model based on ``settings.llm_provider``."""

    provider = settings.llm_provider.lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0,
        )
        model_name = settings.gemini_model
        provider_label = "gemini"

    else:  # default: ollama
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )
        model_name = settings.ollama_model
        provider_label = "ollama"

    return llm.with_structured_output(output_schema), model_name, provider_label


class LLMClient:

    def __init__(
        self,
        output_schema: Type[BaseModel],
    ):
        self.llm, self.model_name, self.provider = _build_llm(output_schema)

    def invoke(
        self,
        messages: list[BaseMessage],
        *,
        generation_name: str,
        metadata: dict | None = None,
    ):
        tracer = get_tracer(__name__)

        with tracer.start_as_current_span("LLM Call") as span:

            span.set_attribute("llm.provider", self.provider)
            span.set_attribute("llm.model", self.model_name)
            span.set_attribute("llm.message_count", len(messages))

            # --- Rate limiting (Gemini only) ---
            rate_wait_s: float = 0.0
            if self.provider == "gemini":
                from shared.llm.rate_limiter import GeminiRateLimiter

                rate_wait_s = GeminiRateLimiter().wait()
                span.set_attribute("llm.rate_limit_wait_s", rate_wait_s)

            # --- Langfuse generation tracking ---
            trace = get_current_trace()
            generation = None

            if trace:
                generation = trace.generation(
                    name=generation_name,
                    model=self.model_name,
                    input=[m.model_dump() for m in messages],
                    metadata={
                        "provider": self.provider,
                        "temperature": 0,
                        **({"rate_limit_wait_s": round(rate_wait_s, 3)} if rate_wait_s > 0 else {}),
                        **(metadata or {}),
                    },
                )

            try:
                response = self.llm.invoke(messages)

                if generation:
                    generation.end(output=response.model_dump())

                return response

            except Exception as ex:
                if generation:
                    generation.end(
                        level="ERROR",
                        status_message=str(ex),
                    )
                raise