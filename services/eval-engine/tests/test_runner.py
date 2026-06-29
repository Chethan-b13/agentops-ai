from benchmark_runner import BenchmarkRunner

from shared.evaluation import EvaluationConfig

runner = BenchmarkRunner()

config = EvaluationConfig(
    model="qwen3:8b",
    prompt_version="v1",
)

runner.run(
    benchmark_path="../../datasets/benchmarks/database/connection_pool_exhaustion.yaml",
    config=config,
)