from shared.repositories.incident_repository import (
    IncidentRepository,
)
from shared.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)

from shared.constants.evidence_types import (
    LOGS,
    METRICS,
    DEPLOYMENTS
)

from shared.services.collectors import ( 
    LogsCollector,
    MetricsCollector,
    DeploymentsCollector,
)


class ContextCollector:

    def __init__(
        self,
        incident_repo: IncidentRepository,
        evidence_repo: IncidentEvidenceRepository,
    ):
        self.incident_repo = incident_repo
        self.evidence_repo = evidence_repo

        self.logs_collector = LogsCollector()
        self.metrics_collector = MetricsCollector()
        self.deployments_collector = DeploymentsCollector()

    def collect(
        self,
        incident_id: str,
    ):

        self.incident_repo.update_status(
            incident_id,
            "collecting_evidence",
        )

        logs = self.logs_collector.collect(
            incident_id
        )

        metrics = self.metrics_collector.collect(
            incident_id
        )

        deployments = (
            self.deployments_collector.collect(
                incident_id
            )
        )

        self.evidence_repo.create(
            incident_id=incident_id,
            evidence_type=LOGS,
            source="mock-cloudwatch",
            raw_data=logs,
            summary_data={
                "top_error": "Database connection timeout",
                "occurrences": 3,
            }
        )

        self.evidence_repo.create(
            incident_id=incident_id,
            evidence_type=METRICS,
            source="mock-cloudwatch",
            raw_data=metrics,
            summary_data=metrics,
        )

        self.evidence_repo.create(
            incident_id=incident_id,
            evidence_type=DEPLOYMENTS,
            source="mock-github",
            raw_data=deployments,
            summary_data={
                "version": deployments["version"]
            },
        )

        self.incident_repo.update_status(
            incident_id,
            "evidence_collected",
        )