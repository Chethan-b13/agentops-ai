import yaml
from shared.settings import ROOT

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

        incident = self.incident_repo.get_by_id(incident_id)

        # Check if the incident is from a benchmark
        if incident and incident.source == "benchmark":
            benchmarks_dir = ROOT / "datasets" / "benchmarks"
            benchmark_data = None
            for p in benchmarks_dir.rglob("*.yaml"):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data and (data.get("name") == incident.alarm_name or data.get("id") == incident.alarm_name):
                            benchmark_data = data
                            break
                except Exception:
                    continue
            
            if benchmark_data and "evidence" in benchmark_data:
                evidence_data = benchmark_data["evidence"]
                logs = {"entries": evidence_data.get("logs", [])}
                metrics = evidence_data.get("metrics", {})
                deployments = self.deployments_collector.collect(incident_id)
            else:
                logs = self.logs_collector.collect(incident_id)
                metrics = self.metrics_collector.collect(incident_id)
                deployments = self.deployments_collector.collect(incident_id)
        else:
            logs = self.logs_collector.collect(incident_id)
            metrics = self.metrics_collector.collect(incident_id)
            deployments = self.deployments_collector.collect(incident_id)

        # Extract top error and occurrences dynamically
        entries = logs.get("entries", [])
        if entries:
            top_error = entries[0]
            occurrences = len(entries)
        else:
            top_error = "No logs collected"
            occurrences = 0

        self.evidence_repo.create(
            incident_id=incident_id,
            evidence_type=LOGS,
            source="mock-cloudwatch",
            raw_data=logs,
            summary_data={
                "top_error": top_error,
                "occurrences": occurrences,
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
                "version": deployments.get("version", "v1.0.0")
            },
        )

        self.incident_repo.update_status(
            incident_id,
            "evidence_collected",
        )