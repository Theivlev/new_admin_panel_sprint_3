from config.redis import RedisClient

from .base_storage import BaseStorage


from dataclasses import dataclass
from typing import Optional


@dataclass
class RedisStorage(BaseStorage):
    """Хранилище состояния в Redis."""

    redis_client: RedisClient

    def save_state(self, key: str, value: str) -> None:
        """Сохранить состояние в хранилище.
        """
        self.redis_client.set(key, value)

    def retrieve_state(self, key: str) -> Optional[str]:
        """Получить состояние из хранилища.
        """
        value = self.redis_client.get(key)
        return value.decode() if value else None
