from eval_engine.discovery import BenchmarkDiscovery
from eval_engine.runner import BenchmarkRunner
from eval_engine.console import Console
from eval_engine.reporting.json_report import JsonReportGenerator
from eval_engine.reporting.html_report import ReportGenerator
from eval_engine.run_state import RunState

from shared.evaluation import EvaluationConfig
from shared.settings import settings


class BenchmarkSuite:

    def __init__(self):

        self.discovery = BenchmarkDiscovery()
        self.runner = BenchmarkRunner()

        self.report_generator = ReportGenerator()
        self.json_generator = JsonReportGenerator()

        self.state = RunState()

    def run(self, benchmark_dir):

        Console.header()

        # Resolve provider + model from env (LLM_PROVIDER / GEMINI_MODEL / OLLAMA_MODEL)
        _active_model = (
            settings.gemini_model
            if settings.llm_provider == "gemini"
            else settings.ollama_model
        )
        config = EvaluationConfig(
            model=_active_model,
            provider=settings.llm_provider,
            prompt_version="v1",
        )
        print(f"🤖 LLM Provider : {settings.llm_provider.upper()} ({_active_model})")

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