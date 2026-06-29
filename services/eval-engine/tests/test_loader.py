from benchmark_loader import BenchmarkLoader

loader = BenchmarkLoader()

benchmark = loader.load(
    "../../datasets/benchmarks/database/connection_pool_exhaustion.yaml"
)

print()

print(benchmark.name)

print()

print(benchmark.tags)

print()

print(benchmark.expected_outputs.rca.root_cause)

print()

print(benchmark.evidence.logs)