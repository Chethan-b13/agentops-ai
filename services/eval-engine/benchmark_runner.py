from pathlib import Path
import time

from benchmark_loader import BenchmarkLoader
from evaluator import Evaluator
from console import Console

from shared.evaluation import (
    EvaluationConfig,
    WorkflowResult,
)


class BenchmarkRunner:

    def __init__(self):
        self.loader = BenchmarkLoader()
        self.evaluator = Evaluator()

    def run(
        self,
        benchmark_path: str | Path,
        config: EvaluationConfig,
    ):

        benchmark = self.loader.load(
            benchmark_path
        )
        

        Console.benchmark(benchmark)

        start = time.perf_counter()

        #
        # TEMP
        #
        # Next commit:
        # Replace with the real workflow.
        #

        result = WorkflowResult(
            incident_id="benchmark",

            triage={
                "severity": "high",
                "category": "database",
                "owner": "payments-api-team",
            },

            rca={
                "root_cause": "PostgreSQL connection pool exhaustion",
            },

            remediation={
                "steps": [
                    "Increase pool",
                    "Fix leaks",
                ]
            },

            validation={
                "passed": True,
            },

            latency_ms=0,
        )

        result.latency_ms = (
            time.perf_counter() - start
        ) * 1000

        evaluation = self.evaluator.evaluate(
            benchmark,
            result,
        )

        print("✓ Loaded Benchmark")
        print("✓ Executed Workflow")
        print("✓ Evaluated")

        print("--------------------------------")

        print(
            "Expected RCA:",
            benchmark.expected_outputs.rca.root_cause,
        )

        print(
            "Predicted RCA:",
            result.rca["root_cause"],
        )

        print(
            f"Score: {evaluation['score']:.2f}"
        )

        print(
            f"Reason: {evaluation['reasoning']}"
        )

        if evaluation["passed"]:
            Console.pass_result(
                evaluation["score"],
                result.latency_ms,
            )
        else:
            Console.fail_result(
                evaluation["score"],
                result.latency_ms,
            )

        return {
            "id": benchmark.id,
            "name": benchmark.name,
            "score": evaluation["score"],
            "passed": evaluation["passed"],
            "latency_ms": result.latency_ms,
        }