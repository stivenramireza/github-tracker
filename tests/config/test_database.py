import pytest
from unittest.mock import Mock

from src.config.database import Database


@pytest.fixture
def mocked_ctx() -> tuple:
    return (None, None)


@pytest.fixture
def mocked_database(monkeypatch, mocked_ctx):
    mocked_db = Mock(return_value=mocked_ctx)
    monkeypatch.setattr(Database, 'get_connection', mocked_db)

    return mocked_db
