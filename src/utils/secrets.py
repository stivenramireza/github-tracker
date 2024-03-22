import os

secrets = {
    'AWS': {
        'access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'region': os.getenv('AWS_REGION'),
    },
    'DATABASE': {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'name': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    },
    'GITHUB': {'secret': os.getenv('GITHUB_SECRET')},
}
