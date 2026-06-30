class DeploymentsCollector:

    def collect(
        self,
        incident_id: str,
    ) -> dict:

        return {
            "version": "v2.3.1",
            "deployed_at": "2026-06-25T12:00:00Z",
            "deployed_by": "github-actions",
        }