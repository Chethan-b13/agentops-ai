class LogsCollector:

    def collect(
        self,
        incident_id: str,
    ) -> dict:

        return {
            "entries": [
                "Database connection timeout",
                "Database connection timeout",
                "Database connection timeout",
                "Connection pool exhausted",
            ]
        }