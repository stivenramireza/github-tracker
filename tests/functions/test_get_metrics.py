import json
import pytest
from unittest.mock import Mock

from src.config.database import Database
from src.repositories.commit_repository import CommitRepository
from src.functions.get_metrics import handler


@pytest.fixture
def mocked_database(monkeypatch):
    return monkeypatch.setattr(Database, 'get_connection', Mock(return_value=(None, None)))


@pytest.fixture
def mocked_get_commits_from_repository(monkeypatch):
    mocked_commits = Mock(return_value=[])
    monkeypatch.setattr(CommitRepository, 'get_commits_by_author_email', mocked_commits)

    return mocked_commits


def test_handler_success_with_data(mocked_database, mocked_get_commits_from_repository) -> None:
    # Arrange
    event, ctx = {'PathParameters': {'email': 'stivenramireza@gmail.com'}}, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'commits': []}),
    }

    mocked_get_commits_from_repository.assert_called_once_with(
        (None, None), 'stivenramireza@gmail.com'
    )
