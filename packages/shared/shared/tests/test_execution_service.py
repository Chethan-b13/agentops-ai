from agents.remediation.schema import (
    RemediationPlanSchema,
    RiskLevel,
)
from agents.validation.validation_schema import (
    ValidationResultSchema,
    ValidationStatus,
)

from shared.clients.github_client import (
    GitHubClient,
)
from shared.executors.github_executor import (
    GitHubExecutor,
)
from shared.services.execution_service import (
    ExecutionService,
)
from shared.settings import settings


def main():

    github_client = GitHubClient(
        token=settings.github_token,
        repository=settings.github_repository,
    )

    github_executor = GitHubExecutor(
        github_client,
    )

    execution_service = ExecutionService(
        github_executor,
    )

    remediation = RemediationPlanSchema(
        title="Increase PostgreSQL Connection Pool",
        summary="Connection pool exhausted.",
        reasoning="Database connections exhausted.",
        recommended_actions=[
            "Increase max pool size",
            "Restart deployment",
        ],
        rollback_plan=[
            "Restore previous pool size",
        ],
        risk=RiskLevel.LOW,
        requires_downtime=False,
        confidence=0.98,
    )

    validation = ValidationResultSchema(
        status=ValidationStatus.PASS,
        summary="Validation successful.",
        findings=[
            "Evidence supports remediation.",
        ],
        recommendations=[
            "Monitor database connections.",
        ],
        confidence=0.99,
    )

    execution_service.execute(
        incident_id="INC-TEST-001",
        remediation_plan=remediation,
        validation_result=validation,
    )

    print("Execution completed successfully.")


if __name__ == "__main__":
    main()