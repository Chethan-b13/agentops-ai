class MetricsCollector:

    def collect(
        self,
        incident_id: str,
    ) -> dict:

        return {
            "cpu_utilization": 94,
            "memory_utilization": 78,
            "request_rate": 1250,
        }