import logging
from logging import config as logging_config

from config.settings import settings
from models.movie import MovieDTO
from models.etl import ETL, Indexes, Tables
from utils.logger import LOGGING_CONFIG
from etl.etl import etl


def main():
    logger = logging.getLogger(__name__)
    logging_config.dictConfig(LOGGING_CONFIG)

    movies_etl = ETL(
        Indexes.MOVIES.value,
        Tables.FILM_WORK.value,
        MovieDTO
    )

    logger.info(
        '📊 Старт ETL процесса для индекса: %s и таблицы: %s',
        Indexes.MOVIES.value,
        Tables.FILM_WORK.value
    )

    etl(movies_etl, settings)

    logger.info('✅ ETL процесс завершён успешно!')


if __name__ == '__main__':
    main()
