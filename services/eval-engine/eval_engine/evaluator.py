from shared.evaluation import Benchmark
from shared.evaluation import WorkflowResult

from eval_engine.judge.llm_judge import LLMJudge


class Evaluator:

    def __init__(self):
        self.judge = LLMJudge()

    def evaluate(
        self,
        benchmark: Benchmark,
        result: WorkflowResult,
    ):

        expected = (
            benchmark.expected_outputs.rca.root_cause
        )

        actual = (
            result.rca["root_cause"]
        )

        judge = self.judge.evaluate(
            expected,
            actual,
        )

        return {
            "score": judge.score,
            "passed": judge.passed,
            "reasoning": judge.reasoning,
        }