import psycopg2

from src.utils.secrets import secrets
from src.utils.secrets_manager import get_secret
from src.utils.logger import Logger


class Database:
    logger: Logger
    secrets: dict
    _connection = None

    def __init__(self) -> None:
        self.logger = Logger('Database')
        self.secrets = secrets.get('DATABASE')
        self.connect()

    def connect(self) -> None:
        try:
            password = get_secret(self.secrets.get('password')).get('password')

            self._connection = psycopg2.connect(
                host=self.secrets.get('host'),
                port=int(self.secrets.get('port')),
                database=self.secrets.get('name'),
                user=self.secrets.get('user'),
                password=password,
            )

            self.logger.info('Connected to PostgreSQL database successfully')
        except Exception as e:
            self.logger.error('Error to connect to PostgreSQL database', e)

    def get_connection(self) -> tuple:
        if self._connection:
            return self._connection, self._connection.cursor()

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            self.logger.info('PostgreSQL connection has been closed')
