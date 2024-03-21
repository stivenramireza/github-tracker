import pytest
from unittest.mock import patch
from typing import Generator, Callable

from src.functions.authorizer import handler


@pytest.fixture
def dynamic_allowed_policy(scope='function') -> Callable:
    def inner(route: str) -> Generator:
        yield {
            'PrincipalID': 'user',
            'PolicyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {'Effect': 'Allow', 'Action': 'execute-api:Invoke', 'Resource': route}
                ],
            },
        }

    return inner


@pytest.fixture
def denied_policy() -> dict:
    return {
        'PrincipalID': 'anonymous',
        'PolicyDocument': {
            'Version': '2012-10-17',
            'Statement': [{'Effect': 'Deny', 'Action': 'execute-api:Invoke', 'Resource': '*'}],
        },
    }


@pytest.fixture
def valid_jwt() -> Generator:
    with patch('jwt.decode') as mocked_func:
        mocked_func.return_value = True
        yield mocked_func


def test_handler_error__commit_path__missing_user_agent(denied_policy: dict) -> None:
    # Arrange
    event, ctx = {
        'Headers': {'Authorization': 'eyyy'},
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/commit'}},
    }, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == denied_policy


def test_handler_success__commit_path__invalid_user_agent(denied_policy: dict) -> None:
    # Arrange
    event, ctx = {
        'Headers': {'user-agent': 'X'},
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/commit'}},
    }, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == denied_policy


def test_handler_success__commit_path(dynamic_allowed_policy: Callable) -> None:
    # Arrange
    event, ctx = {
        'Headers': {'user-agent': 'GitHub-Hookshot'},
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/commit'}},
    }, {}

    # Act
    result = handler(event, ctx)
    allowed_policy = next(dynamic_allowed_policy('X'))

    # Assert
    assert result == allowed_policy


def test_handler_error__normal_path__missing_authorization(denied_policy: dict) -> None:
    # Arrange
    event, ctx = {
        'Headers': {'user-agent': 'GitHub-Hookshot'},
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/metrics'}},
    }, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == denied_policy


def test_handler_error__normal_path__missing_authorization_bearer_token(
    denied_policy: dict,
) -> None:
    # Arrange
    event, ctx = {
        'Headers': {
            'user-agent': 'GitHub-Hookshot',
            'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1GRE',
        },
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/metrics'}},
    }, {}

    # Act
    result = handler(event, ctx)

    # Assert
    assert result == denied_policy


def test_handler_success__normal_path(
    valid_jwt: Generator,
    dynamic_allowed_policy: Callable,
) -> None:
    # Arrange
    event, ctx = {
        'Headers': {
            'user-agent': 'GitHub-Hookshot',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1GREJ2Y2VrRVVYUEZPaC0wOXc2biJ9.eyJpc3MiOiJodHRwczovL',
        },
        'RouteArn': 'X',
        'RequestContext': {'HTTP': {'Path': '/metrics'}},
    }, {}

    # Act
    result = handler(event, ctx)
    allowed_policy = next(dynamic_allowed_policy('X'))

    # Assert
    assert result == allowed_policy
