import logging
from logging import config as logging_config

from config.settings import settings
from models.genre import GenreDTO
from models.person import PersonInfoDTO
from models.movie import MovieDTO
from models.etl import ETL, Indexes, Tables, ETLManager
from utils.logger import LOGGING_CONFIG
from etl.extract.query import Query

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


def main():

    etl_manager = ETLManager(settings)

    etl_configs = [
        ETL(
            Indexes.MOVIES,
            Tables.FILM_WORK,
            MovieDTO,
            Query.get_films_query
        ),
        ETL(
            Indexes.GENRES,
            Tables.GENRE,
            PersonInfoDTO,
            Query.get_genres_query
        ),
        ETL(
            Indexes.PERSONS,
            Tables.PERSON,
            GenreDTO,
            Query.get_genres_query
        ),
    ]

    for config in etl_configs:
        etl_manager.run_etl(config)

    logger.info('✅ Все ETL процессы завершены успешно!')


if __name__ == '__main__':
    main()
