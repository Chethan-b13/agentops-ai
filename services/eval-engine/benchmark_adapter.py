from shared.evaluation import Benchmark


class BenchmarkAdapter:
    """
    Converts a benchmark dataset into the objects expected
    by the production incident pipeline.
    """

    def create_incident(self, benchmark: Benchmark) -> dict:
        return {
            "alarm_name": benchmark.name,
            "service": benchmark.incident.service,
            "region": benchmark.incident.region,
            "severity": benchmark.incident.severity,
            "source": benchmark.source,
        }

    def create_evidence(self, benchmark: Benchmark) -> dict:
        return {
            "logs": benchmark.evidence.logs,
            "metrics": benchmark.evidence.metrics,
        }