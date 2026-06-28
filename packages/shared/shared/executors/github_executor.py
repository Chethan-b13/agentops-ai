from shared.clients.github_client import GitHubClient


class GitHubExecutor:

    def __init__(
        self,
        github_client: GitHubClient,
    ):
        self.github = github_client

    def execute(
        self,
        incident_id: str,
        remediation_plan,
        validation_result,
    ):

        branch = f"incident/{incident_id}"

        self.github.create_branch(branch)

        markdown = f"""
        # Incident

        {incident_id}

        # Remediation

        ## {remediation_plan.title}

        {remediation_plan.summary}

        ## Recommended Actions

        {chr(10).join(f"- {x}" for x in remediation_plan.recommended_actions)}

        ## Rollback

        {chr(10).join(f"- {x}" for x in remediation_plan.rollback_plan)}

        # Validation

        Status:
        {validation_result.status}

        Summary

        {validation_result.summary}
        """

        self.github.create_file(
            path=f"automation/{incident_id}/remediation.md",
            message=f"Incident {incident_id}",
            content=markdown,
            branch=branch,
        )

        self.github.create_pull_request(
            title=f"Incident {incident_id}",
            body=remediation_plan.summary,
            branch=branch,
        )