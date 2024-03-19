import os

secrets = {
    'DATABASE': {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'schema': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    },
}
