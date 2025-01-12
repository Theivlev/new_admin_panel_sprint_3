import psycopg
from psycopg.errors import ConnectionFailure
from pydantic import PostgresDsn

from utils.backoff import backoff

from base import BaseConfig


class PostgresClient(BaseConfig):
    """Класс клиента для работы с PostgreSQL."""

    def __init__(self, dsn: PostgresDsn, connection=None):

        super().__init__(dsn, connection)

        self.cursor = self.connection.cursor()

    @backoff(ConnectionFailure)
    def reconnect(self):
        """Подключение к PostgreSQL."""

        return psycopg.connect(self.dsn)
