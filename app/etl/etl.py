import logging
import threading
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

from extract.data_extract import PostgresExtractor
from load.data_loader import ElasticsearchLoader
from transform.data_transform import DataTransform

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


def etl(etl: ETL, settings: Settings) -> None:
    """ETL процесс для конкретного маппера."""

    logger.info('%s ETL начат', etl.index)

    with closing(ElasticsearchClient(settings.elasticsearch_dsn)) as elasticsearch_client, \
         closing(PostgresClient(settings.postgres_dsn)) as postgres_client, \
         closing(RedisClient(settings.redis_dsn)) as redis_client:

        state = State(storage=RedisStorage(redis_client=redis_client))

        if not state.get_state(key=etl.index):
            state.set_state(key=etl.index, value=str(datetime.min))

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
                    loader.load(transformed_data, last_modified)

            logger.info(
                '%s ETL завершён, засыпаем на %s с',
                etl.index, settings.timeout
            )

            time.sleep(settings.timeout)
