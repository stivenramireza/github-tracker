import json
import pytest
from unittest.mock import Mock

from src.config.database import Database
from src.models.models import Commit
from src.repositories.commit_repository import CommitRepository
from src.functions.get_metrics import handler


@pytest.fixture
def mocked_db_connection() -> tuple:
    return (None, None)


@pytest.fixture
def mocked_database(monkeypatch, mocked_db_connection):
    mocked_db = Mock(return_value=mocked_db_connection)
    monkeypatch.setattr(Database, 'get_connection', mocked_db)

    return mocked_db


@pytest.fixture
def mocked_get_commits_from_repository_without_data(monkeypatch):
    mocked_commits = Mock(return_value=[])
    monkeypatch.setattr(CommitRepository, 'get_commits_by_author_email', mocked_commits)

    return mocked_commits


@pytest.fixture
def mocked_commits_from_repository() -> list[Commit]:
    return [
        {
            'id': '4ac5123c-d772-4e99-ad69-d163789b6108',
            'commit_message': '[ADD] Handler github-webhook event 1',
            'repo_name': 'stivenramireza/github-tracker',
        },
        {
            'id': '1365317b-8263-45d2-80d4-612ac9e2ec6a',
            'commit_message': '[ADD] Handler github-webhook event 2',
            'repo_name': 'stivenramireza/github-tracker',
        },
    ]


@pytest.fixture
def mocked_get_commits_from_repository_with_data(monkeypatch, mocked_commits_from_repository):
    mocked_commits = Mock(return_value=mocked_commits_from_repository)
    monkeypatch.setattr(CommitRepository, 'get_commits_by_author_email', mocked_commits)

    return mocked_commits


def test_handler_success_with_data(
    mocked_database,
    mocked_db_connection,
    mocked_commits_from_repository,
    mocked_get_commits_from_repository_with_data,
) -> None:
    # Arrange
    email = 'stivenramireza@gmail.com'

    event, ctx = {'PathParameters': {'email': email}}, {}

    # Act
    result = handler(event, ctx)

    # Assert
    mocked_commits = [
        {'id': commit['id'], 'message': commit['commit_message'], 'repo': commit['repo_name']}
        for commit in mocked_commits_from_repository
    ]

    assert result == {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(
            {
                'author': email,
                'count': len(mocked_commits),
                'commits': mocked_commits,
            }
        ),
    }

    mocked_get_commits_from_repository_with_data.assert_called_once_with(
        mocked_db_connection, email
    )


def test_handler_success_without_data(
    mocked_database,
    mocked_db_connection,
    mocked_get_commits_from_repository_without_data,
) -> None:
    # Arrange
    email = 'stivenramireza@gmail.com'

    event, ctx = {'PathParameters': {'email': email}}, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(
            {
                'author': email,
                'count': 0,
                'commits': [],
            }
        ),
    }

    mocked_get_commits_from_repository_without_data.assert_called_once_with(
        mocked_db_connection, email
    )


def test_handler_failed(
    mocked_database,
    mocked_get_commits_from_repository_without_data,
) -> None:
    # Arrange
    email = ''

    event, ctx = {'PathParameters': {'email': email}}, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == {
        'statusCode': 400,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Missing email parameter'}),
    }

    mocked_get_commits_from_repository_without_data.assert_not_called()
