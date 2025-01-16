import psycopg
from psycopg.errors import ConnectionFailure
from pydantic import PostgresDsn
from psycopg.rows import dict_row
from utils.backoff import backoff

from .base import BaseConfig


class PostgresClient(BaseConfig):
    """Класс клиента для работы с PostgreSQL."""

    def __init__(self, dsn: PostgresDsn, connect=None):
        super().__init__(dsn, connect)
        self.cursor = self.connection.cursor(row_factory=dict_row)

    @backoff(ConnectionFailure)
    def reconnect(self):
        """Подключение к PostgreSQL."""
        self.connect = psycopg.connect(str(self.dsn))
        self.cursor = self.connection.cursor(row_factory=dict_row)
        return self.connect
