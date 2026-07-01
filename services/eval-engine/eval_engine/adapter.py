import uuid

from shared.models.incident import Incident
from shared.evaluation import Benchmark


class BenchmarkAdapter:

    def create_incident(
        self,
        benchmark: Benchmark,
    ) -> Incident:

        return Incident(
            id=f"INC-{uuid.uuid4().hex[:8]}",
            alarm_name=benchmark.name,
            service=benchmark.incident.service,
            region=benchmark.incident.region,

            # Synthetic benchmark values
            metric_name=benchmark.incident.metric_name or "benchmark",
            threshold=benchmark.incident.threshold if benchmark.incident.threshold is not None else 1.0,
            current_value=benchmark.incident.current_value if benchmark.incident.current_value is not None else 1.0,

            severity="unknown",
            source="benchmark",
            status="new",
        )