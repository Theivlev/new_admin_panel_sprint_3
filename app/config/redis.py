from redis import Redis
from redis.exceptions import ConnectionError
from redis.typing import EncodableT, KeyT

from utils.backoff import backoff

from .base import BaseConfig
from pydantic import AnyUrl


class RedisClient(BaseConfig):
    """Конфигурация и операции клиента Redis."""

    @backoff(ConnectionError)
    def reconnect(self) -> Redis:
        """Переподключение к Redis, если соединение отсутствует.

        Возвращает:
            Redis: Клиент Redis.
        """
        return Redis(host=self.dsn.host, port=int(self.dsn.port), db=self.dsn.path[1:])

    @backoff(ConnectionError)
    def set(self, key: KeyT, value: EncodableT, *args, **kwargs) -> None:
        """Устанавливает значение в Redis.
        """
        self.connection.set(key, value, *args, **kwargs)

    @backoff(ConnectionError)
    def get(self, key: KeyT) -> bytes | None:
        """Получает значение из Redis.
        """
        return self.connection.get(key)
