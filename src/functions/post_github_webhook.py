import json
import hmac
import hashlib
import datetime

from src.middlewares import database
from src.models.models import GitHubWebhook
from src.entities.commit_entity import Commit
from src.repositories.commit_repository import CommitRepository
from src.utils.logger import Logger
from src.utils.secrets import secrets
from src.utils.secrets_manager import get_secret
from src.utils.responses import CreatedResponse, ConflictResponse, UnauthorizedResponse


GITHUB_SIGNATURE_HEADER = 'x-hub-signature-256'
GITHUB_SIGNATURE_PREFIX = 'sha256='


def calculate_signature(secret: str, body: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def validate_github_request(event: dict, ctx: dict, logger: Logger) -> bool:
    try:
        full_signature = event.get('Headers').get(GITHUB_SIGNATURE_HEADER)
        if not full_signature:
            logger.error(f'Missing {GITHUB_SIGNATURE_HEADER}')
            return False

        signature = full_signature.removeprefix(GITHUB_SIGNATURE_PREFIX)

        secret = get_secret(secrets.get('GITHUB').get('secret')).get('secret')

        calculated_signature = calculate_signature(secret, event.get('Body'))

        return hmac.compare_digest(calculated_signature, signature)
    except Exception as e:
        logger.error(f'Error to validate the signature: {e}')
        return False


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
    logger = Logger('post_github_webhook handler')

    is_valid_request = validate_github_request(event, ctx, logger)
    if not is_valid_request:
        return UnauthorizedResponse('Invalid GitHub webhook').to_dict()

    body = event.get('Body')
    webhook: GitHubWebhook = json.loads(body)

    properties: dict = {}
    properties['head_commit'] = webhook['head_commit']
    logger.info('Valid GitHub webhook received', properties)

    commit_repository = CommitRepository()
    inserted_commit = insert_github_webhook(ctx, commit_repository, webhook, body)
    if not inserted_commit:
        return ConflictResponse('Error to insert the commit').to_dict()

    return CreatedResponse('The commit has been inserted successfully').to_dict()
