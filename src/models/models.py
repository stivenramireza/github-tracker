from dataclasses import dataclass


@dataclass
class CommitUser:
    email: str
    username: str


@dataclass
class Commit:
    id: str
    message: str
    author: CommitUser


@dataclass
class Repository:
    full_name: str


@dataclass
class GitHubWebhook:
    repository: Repository
    head_commit: Commit
