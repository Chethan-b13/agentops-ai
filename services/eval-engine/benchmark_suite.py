from benchmark_discovery import BenchmarkDiscovery
from benchmark_runner import BenchmarkRunner
from console import Console
from json_report_generator import JsonReportGenerator
from report_generator import ReportGenerator
from run_state import RunState

from shared.evaluation import EvaluationConfig


class BenchmarkSuite:

    def __init__(self):

        self.discovery = BenchmarkDiscovery()
        self.runner = BenchmarkRunner()

        self.report_generator = ReportGenerator()
        self.json_generator = JsonReportGenerator()

        self.state = RunState()

    def run(self, benchmark_dir):

        Console.header()

        config = EvaluationConfig(
            model="qwen3:8b",
            prompt_version="v1",
        )

        benchmarks = self.discovery.discover(
            benchmark_dir
        )

        state = self.state.load()

        completed = set(state["completed"])
        results = state["results"]

        passed = sum(
            r["passed"]
            for r in results
        )

        for benchmark in benchmarks:

            benchmark_id = benchmark.stem

            if benchmark_id in completed:

                print(
                    f"⏭ Skipping {benchmark_id}"
                )

                continue

            try:

                result = self.runner.run(
                    benchmark,
                    config,
                )

                results.append(result)

                if result["passed"]:
                    passed += 1

                completed.add(
                    benchmark_id
                )

                self.state.save(
                    sorted(completed),
                    results,
                )

                self.report_generator.generate(
                    results
                )

                self.json_generator.generate(
                    results
                )

            except Exception as e:

                print()

                print(
                    f"❌ {benchmark_id} failed"
                )

                print(e)

                continue

        markdown_report = (
            self.report_generator.generate(
                results
            )
        )

        json_report = (
            self.json_generator.generate(
                results
            )
        )

        Console.summary(
            total=len(results),
            passed=passed,
            markdown_report=markdown_report,
            json_report=json_report,
        )