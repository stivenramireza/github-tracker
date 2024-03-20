import json

from src.middlewares import database
from src.models import models
from src.entities.commit_entity import Commit
from src.repositories.commit_repository import CommitRepository


def parse_response(email: str, commits: list[Commit]) -> dict:
    response_commits: list[models.Commit] = []

    for commit in commits:
        response_commit = {
            'id': commit.id,
            'message': commit.commit_message,
            'repo': commit.repo_name,
        }
        response_commits.append(response_commit)

    return {'author': email, 'count': len(response_commits), 'commits': response_commits}


@database.manager
def handler(event: dict, ctx: tuple) -> dict:
    email = event.get('PathParameters').get('email')
    if email == '':
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Missing email parameter'}),
        }

    commit_repository = CommitRepository()
    commits = commit_repository.get_commits_by_author_email(ctx, email)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'commits': commits}),
    }
