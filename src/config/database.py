import psycopg2

from src.utils.secrets import secrets
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
            self.logger.info(None, 'Secrets', self.secrets)
            self._connection = psycopg2.connect(
                host=self.secrets.get('DB_HOST'),
                port=self.secrets.get('DB_PORT'),
                dbname=self.secrets.get('DB_NAME'),
                user=self.secrets.get('DB_USER'),
                password=self.secrets.get('DB_PASSWORD'),
            )
            self.logger.info(None, 'Connected to PostgreSQL database successfully')
        except Exception as e:
            self.logger.error(None, 'Error to connect to PostgreSQL database', e)

    def get_connection(self) -> object:
        if self._connection:
            return self._connection.cursor

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            self.logger.info(None, 'PostgreSQL connection has been closed')
