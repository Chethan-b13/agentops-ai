from shared.executors.github_executor import (
    GitHubExecutor,
)


class ExecutionService:

    def __init__(
        self,
        github_executor: GitHubExecutor,
    ):
        self.github_executor = github_executor

    def execute(
        self,
        incident_id,
        remediation_plan,
        validation_result,
    ):

        self.github_executor.execute(
            incident_id=incident_id,
            remediation_plan=remediation_plan,
            validation_result=validation_result,
        )