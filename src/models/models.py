class CommitUser:
    email: str
    username: str


class Commit:
    id: str
    message: str
    author: str


class Repository:
    full_name: str


class GitHubWebhook:
    repository: Repository
    head_commit: Commit
