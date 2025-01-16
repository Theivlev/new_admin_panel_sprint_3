import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from utils.backoff import backoff
from .base import BaseConfig

# Настройка логирования
logger = logging.getLogger(__name__)


class ElasticsearchClient(BaseConfig):
    """Класс для работы с Elasticsearch."""

    @backoff(ConnectionError)
    def reconnect(self):
        """Подключение к Elasticsearch."""
        # Логируем текущее значение dsn
        logger.info('Попытка подключения к Elasticsearch с dsn: %s', self.dsn)
        logger.info(type(self.dsn))
        # Преобразуем dsn в список, если это строка

        logger.info('Преобразованный dsn для подключения: %s', self.dsn)
        return Elasticsearch(str(self.dsn))
