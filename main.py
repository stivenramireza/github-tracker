import json

from src.functions import get_metrics, post_github_webhook
from src.utils.logger import Logger


def handle_get_metrics(logger: Logger) -> None:
    event, ctx = {'PathParameters': {'email': 'stivenramireza@gmail.com'}}, {}
    response = get_metrics.handler(event, ctx)
    logger.info('Handler response', response)


def handle_post_github_webhook(logger: Logger) -> None:
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
    response = post_github_webhook.handler(event, ctx)
    logger.info('Handler response', response)


def main() -> dict:
    logger = Logger('main')

    handle_get_metrics(logger)
    # handle_post_github_webhook(logger)


if __name__ == '__main__':
    main()
