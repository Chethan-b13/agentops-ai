from langchain_core.messages import HumanMessage

from shared.llm.client import LLMClient

from eval_engine.judge.judge_schema import JudgeResult


class LLMJudge:

    def __init__(self):
        self.llm = LLMClient(JudgeResult)

    def evaluate(
        self,
        expected: str,
        actual: str,
    ) -> JudgeResult:

        prompt = f"""
        You are an expert evaluator.

        Compare the expected answer with the predicted answer.

        Use the following evaluation criteria and weighting:
        - Component match (50%): does the predicted root cause name the correct component/service or subsystem?
        - Mechanism match (30%): does the predicted root cause identify the concrete failure mechanism (e.g. missing policy, memory leak in buffer cache, blocking external call)?
        - Symptom/context match (20%): does the prediction mention the key symptom or effect described in the expected answer (e.g. GC not collecting, timeout, AccessDenied)?

        Expected:
        {expected}

        Predicted:
        {actual}

        Return:

        - score between 0.0 and 1.0
        - passed (true if score >= 0.8)
        - reasoning

        Do NOT explain outside the JSON.
        """

        return self.llm.invoke(
            [HumanMessage(content=prompt)],
            generation_name="LLM Judge",
            metadata={
                "agent": "judge",
                "prompt_version": "v1",
            },
        )