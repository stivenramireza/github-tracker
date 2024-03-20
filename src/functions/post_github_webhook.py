import json
import datetime

from src.middlewares import database
from src.models.models import GitHubWebhook
from src.entities.commit_entity import Commit
from src.repositories.commit_repository import CommitRepository


def insert_github_webhook(
    ctx: dict, repository: CommitRepository, webhook: GitHubWebhook, body: str
) -> bool:
    commit = Commit(
        id=None,
        repo_name=webhook['repository']['full_name'],
        commit_id=webhook['head_commit']['id'],
        commit_message=webhook['head_commit']['message'],
        author_username=webhook['head_commit']['author']['username'],
        author_email=webhook['head_commit']['author']['email'],
        payload=body,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    return repository.insert(ctx, commit)


@database.manager
def handler(event: dict, ctx: dict) -> dict:
    body = event.get('Body')

    webhook: GitHubWebhook = json.loads(body)

    commit_repository = CommitRepository()
    inserted_commit = insert_github_webhook(ctx, commit_repository, webhook, body)
    if not inserted_commit:
        return {
            'statusCode': 409,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Error to insert the commit'}),
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'The commit has been inserted successfully'}),
    }
