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