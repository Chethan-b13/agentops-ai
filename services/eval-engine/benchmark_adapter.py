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
            metric_name="benchmark",
            threshold=1,
            current_value=1,

            severity="unknown",
            source="benchmark",
            status="new",
        )