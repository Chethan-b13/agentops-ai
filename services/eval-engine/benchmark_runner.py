from pathlib import Path
import time

from sqlalchemy.orm import Session

from benchmark_loader import BenchmarkLoader
from benchmark_adapter import BenchmarkAdapter
from evaluator import Evaluator
from console import Console

from shared.database.session import SessionLocal
from shared.services import IncidentProcessingService
from shared.evaluation import (
    EvaluationConfig,
    WorkflowResult,
)

from workflows.factory import create_workflow


class BenchmarkRunner:

    def __init__(self):
        self.loader = BenchmarkLoader()
        self.adapter = BenchmarkAdapter()
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

        db: Session = SessionLocal()

        try:

            processing_service = (
                IncidentProcessingService(db)
            )

            incident = self.adapter.create_incident(
                benchmark
            )

            incident = processing_service.process(
                incident
            )

            start = time.perf_counter()

            with create_workflow(db) as graph:

                state = graph.invoke(
                    {
                        "incident_id": incident.id,
                    },
                    config={
                        "configurable": {
                            "thread_id": incident.id,
                        }
                    },
                )

            latency_ms = (
                time.perf_counter() - start
            ) * 1000

            result = WorkflowResult(
                incident_id=incident.id,
                triage=state["triage_result"].model_dump(),
                rca=state["rca_result"].model_dump(),
                remediation=state[
                    "remediation_plan"
                ].model_dump(),
                validation=state[
                    "validation_result"
                ].model_dump(),
                latency_ms=latency_ms,
            )

            evaluation = self.evaluator.evaluate(
                benchmark,
                result,
            )

            print("✓ Loaded Benchmark")
            print("✓ Executed Real Workflow")
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

        finally:
            db.close()