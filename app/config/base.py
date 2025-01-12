import abc
from dataclasses import dataclass, field
from pydantic import AnyUrl


@dataclass
class BaseConfig(abc.ABC):
    """Базовый класс для клиента."""

    dsn: AnyUrl
    connect: any = field(default=None, init=False)

    @abc.abstractmethod
    def reconnect(self) -> any:
        """Переподключить соединение"""

    def close(self) -> None:
        """Закрыть соединение клиента."""
        if self.connection:
            self.connection.close()

    @property
    def connection(self) -> any:
        """Получить/восстановить соединение."""
        return self.connect if self.connect else self.reconnect()
