from redis import Redis
from redis.exceptions import ConnectionError
from redis.typing import EncodableT, KeyT

from utils.backoff import backoff

from base import BaseConfig
from pydantic import AnyUrl


class RedisConfig(BaseConfig):
    """Конфигурация и операции клиента Redis."""

    def __init__(self, dsn: AnyUrl):
        """Инициализация RedisConfig с DSN.

        Параметры:
            dsn (AnyUrl): Строка подключения к Redis.
        """
        super().__init__(dsn)
        self.redis_client: Redis | None = None

    @backoff(ConnectionError)
    def reconnect(self) -> Redis:
        """Переподключение к Redis, если соединение отсутствует.

        Возвращает:
            Redis: Клиент Redis.
        """
        if not hasattr(self, 'redis_client') or self.redis_client is None:
            self.redis_client = Redis(
                host=self.dsn.host or 'localhost',
                port=int(self.dsn.port) if self.dsn.port else 6379,
                db=int(self.dsn.path[1:]) if self.dsn.path else 0
            )
        return self.redis_client

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
