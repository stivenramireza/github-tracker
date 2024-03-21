import jwt

from src.utils.logger import Logger


GITHUB_USER_AGENT_PREFIX = 'GitHub-Hookshot'


def validate_token(logger: Logger, token: str, route: str) -> dict:
    try:
        jwt.decode(token, algorithms=['RS256'])
        return allow_request(route)
    except Exception as e:
        return deny_request(logger, 'Invalid token')


def deny_request(logger: Logger, reason: str) -> dict:
    logger.info('Reason', reason)

    return {
        'PrincipalID': 'anonymous',
        'PolicyDocument': {
            'Version': '2012-10-17',
            'Statement': [{'Effect': 'Deny', 'Action': 'execute-api:Invoke', 'Resource': '*'}],
        },
    }


def allow_request(route: str) -> dict:
    return {
        'PrincipalID': 'user',
        'PolicyDocument': {
            'Version': '2012-10-17',
            'Statement': [{'Effect': 'Allow', 'Action': 'execute-api:Invoke', 'Resource': route}],
        },
    }


def handler(event: dict, ctx: dict) -> dict:
    logger = Logger('authorizer')
    route, path = event['RouteArn'], event['RequestContext']['HTTP']['Path']

    if path == '/commit':
        user_agent: str = event['Headers'].get('user-agent')
        if not user_agent:
            return deny_request(logger, 'Missing user-agent')

        is_valid_github_user_agent = user_agent.startswith(GITHUB_USER_AGENT_PREFIX)
        if not is_valid_github_user_agent:
            return deny_request(logger, 'Invalid GitHub user agent')

        return allow_request(route)

    auth_token: str = event['Headers'].get('Authorization')
    if not auth_token:
        return deny_request(logger, 'Missing Authorization token')

    token = auth_token.removeprefix('Bearer ')
    if token == '':
        return deny_request(logger, 'Missing Authorization Bearer token')

    return validate_token(logger, token, route)
