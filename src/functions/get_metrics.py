import json

from src.middlewares import database
from src.entities.commit_entity import Commit
from src.repositories.commit_repository import CommitRepository
from src.utils.logger import Logger

logger = Logger('get_metrics')


def parse_response(email: str, commits: list[Commit]) -> dict:
    response_commits = [
        {'id': commit['id'], 'message': commit['commit_message'], 'repo': commit['repo_name']}
        for commit in commits
    ]

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

    response = parse_response(email, commits)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response),
    }
