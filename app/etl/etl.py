import logging
import time
from contextlib import closing
from datetime import datetime
from logging import config as logging_config

from config import ElasticsearchClient, PostgresClient, RedisClient
from state.state import State
from state.redis_storage import RedisStorage
from utils.logger import LOGGING_CONFIG
from models.etl import ETL
from config.settings import Settings

from etl.extract.data_extract import PostgresExtractor
from etl.load.data_loader import ElasticsearchLoader
from etl.transform.data_transform import DataTransform
from elasticsearch.helpers import BulkIndexError
logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


def etl(etl: ETL, settings: Settings) -> None:
    """ETL процесс для конкретного маппера."""

    logger.info('%s ETL начат', etl.index)

    with closing(ElasticsearchClient(settings.elasticsearch_dsn)) as elasticsearch_client, \
         closing(PostgresClient(settings.postgres_dsn)) as postgres_client, \
         closing(RedisClient(settings.redis_dsn)) as redis_client:

        # Логируем информацию о подключении к базам данных
        logger.info('Подключение к Elasticsearch: %s', settings.elasticsearch_dsn, type(elasticsearch_client))
        logger.info('Подключение к PostgreSQL: %s', settings.postgres_dsn)
        try:
            postgres_client.cursor.execute("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type='BASE TABLE'
                ORDER BY table_schema, table_name;
            """)
            tables = postgres_client.cursor.fetchall()
            logger.info('Список таблиц и схем:')
            for schema, table in tables:
                logger.info('Схема: %s, Таблица: %s', schema, table)
        except Exception as e:
            logger.error('Ошибка при получении таблиц: %s', e)
        state = State(storage=RedisStorage(redis_client=redis_client))

        if not state.get_state(key=str(etl.index)):
            state.set_state(key=str(etl.index), value=str(datetime.min))

        extractor = PostgresExtractor(
            postgres_client=postgres_client,
            state=state,
            etl=etl,
            batch_size=settings.batch_size
        )

        transformer = DataTransform(model=etl.model)

        loader = ElasticsearchLoader(
            client=elasticsearch_client,
            state=state,
            index=etl.index,
            batch_size=settings.batch_size
        )

        while True:
            for data, last_modified in extractor.extract():
                if data:
                    transformed_data = transformer.data_transform(data)
                    try:
                        loader.bulk_load(transformed_data, last_modified)
                    except BulkIndexError as e:
                        logger.error('Ошибка при индексации в Elasticsearch: %s', e)
                        for error in e.errors:
                            logger.error('Ошибка для документа ID=%s: %s', error['index']['_id'], error['index']['error'])

            logger.info(
                '%s ETL завершён, засыпаем на %s с',
                etl.index, settings.timeout
            )

            time.sleep(settings.timeout)