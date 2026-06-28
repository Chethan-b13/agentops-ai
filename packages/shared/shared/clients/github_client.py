from github import Github


class GitHubClient:

    def __init__(
        self,
        token: str,
        repository: str,
    ):
        self.repo = (
            Github(token)
            .get_repo(repository)
        )

    def create_branch(
        self,
        branch_name: str,
    ):

        source = self.repo.get_branch(
            "main"
        )

        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=source.commit.sha,
        )

    def create_file(
        self,
        path: str,
        message: str,
        content: str,
        branch: str,
    ):

        self.repo.create_file(
            path=path,
            message=message,
            content=content,
            branch=branch,
        )

    def create_pull_request(
        self,
        title: str,
        body: str,
        branch: str,
    ):

        return self.repo.create_pull(
            title=title,
            body=body,
            head=branch,
            base="main",
        )