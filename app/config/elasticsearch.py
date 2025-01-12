from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from utils.backoff import backoff
from base import BaseConfig


class ElasticsearchClient(BaseConfig):
    """Класс для работы с Elasticsearch."""

    @backoff(ConnectionError)
    def reconnect(self) -> Elasticsearch:
        """Подключение к Elasticsearch"""

        return Elasticsearch(self.dsn)
