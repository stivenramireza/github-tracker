import json
import pytest
import datetime
from unittest.mock import Mock

from src.entities.commit_entity import Commit
from src.repositories.commit_repository import CommitRepository
from src.functions.post_github_webhook import handler

from tests.config.test_database import mocked_database, mocked_ctx


@pytest.fixture
def mocked_datetime_now(monkeypatch):
    current_datetime = datetime.datetime(2024, 3, 19)

    class mydatetime:
        @classmethod
        def now(cls):
            return current_datetime

    monkeypatch.setattr(datetime, 'datetime', mydatetime)

    return current_datetime


@pytest.fixture
def mocked_insert_repository_success(monkeypatch):
    mocked_insert = Mock(return_value=True)
    monkeypatch.setattr(CommitRepository, 'insert', mocked_insert)

    return mocked_insert


@pytest.fixture
def mocked_insert_repository_error(monkeypatch):
    mocked_insert = Mock(return_value=False)
    monkeypatch.setattr(CommitRepository, 'insert', mocked_insert)

    return mocked_insert


def test_handler_success(
    mocked_database,
    mocked_ctx,
    mocked_datetime_now,
    mocked_insert_repository_success,
) -> None:
    # Arrange
    event, ctx = {
        'Body': json.dumps(
            {
                'repository': {'full_name': 'stivenramireza/github-tracker'},
                'head_commit': {
                    'id': 'f2fecb40-97fe-41d0-9336-268349d2ee36',
                    'message': '[ADD] Handler github-webhook event',
                    'author': {'email': 'stivenramireza@gmail.com', 'username': 'stivenramireza'},
                },
            }
        )
    }, {}

    mocked_commit = Commit(
        id=None,
        repo_name='stivenramireza/github-tracker',
        commit_id='f2fecb40-97fe-41d0-9336-268349d2ee36',
        commit_message='[ADD] Handler github-webhook event',
        author_username='stivenramireza',
        author_email='stivenramireza@gmail.com',
        payload=event.get('Body'),
        created_at=mocked_datetime_now,
        updated_at=mocked_datetime_now,
    )

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'The commit has been inserted successfully'}),
    }

    mocked_insert_repository_success.assert_called_once_with(mocked_ctx, mocked_commit)


def test_handler_error(
    mocked_database,
    mocked_ctx,
    mocked_datetime_now,
    mocked_insert_repository_error,
) -> None:
    # Arrange
    event, ctx = {
        'Body': json.dumps(
            {
                'repository': {'full_name': 'stivenramireza/github-tracker'},
                'head_commit': {
                    'id': 'f2fecb40-97fe-41d0-9336-268349d2ee36',
                    'message': '[ADD] Handler github-webhook event',
                    'author': {'email': 'stivenramireza@gmail.com', 'username': 'stivenramireza'},
                },
            }
        )
    }, {}

    mocked_commit = Commit(
        id=None,
        repo_name='stivenramireza/github-tracker',
        commit_id='f2fecb40-97fe-41d0-9336-268349d2ee36',
        commit_message='[ADD] Handler github-webhook event',
        author_username='stivenramireza',
        author_email='stivenramireza@gmail.com',
        payload=event.get('Body'),
        created_at=mocked_datetime_now,
        updated_at=mocked_datetime_now,
    )

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == {
        'statusCode': 409,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Error to insert the commit'}),
    }

    mocked_insert_repository_error.assert_called_once_with(mocked_ctx, mocked_commit)
