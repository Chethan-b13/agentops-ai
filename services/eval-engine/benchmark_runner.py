from pathlib import Path

from benchmark_loader import BenchmarkLoader
from shared.evaluation import EvaluationConfig


class BenchmarkRunner:

    def __init__(self):
        self.loader = BenchmarkLoader()

    def run(
        self,
        benchmark_path: str | Path,
        config: EvaluationConfig,
    ):

        benchmark = self.loader.load(benchmark_path)

        print(f"Running benchmark: {benchmark.name}")

        print(f"Model: {config.model}")

        print(f"Prompt: {config.prompt_version}")

        print()

        print("✓ Benchmark loaded")

        return benchmark