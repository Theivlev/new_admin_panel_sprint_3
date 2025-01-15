import logging
from concurrent.futures import ThreadPoolExecutor
from logging import config as logging_config

from models.genre import GenreDTO
from models.movie import MovieDTO
from models.person import PersonInfoDTO
from models.etl import ETL, Indexes, Tables
from utils.logger import LOGGING_CONFIG
from config.settings import settings
from etl.extract.query import Query
from etl.etl import etl

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging_config.dictConfig(LOGGING_CONFIG)

    MOVIES = ETL(
        Indexes.MOVIES,
        Tables.FILM_WORK,
        #  Query.get_films_query(),
        MovieDTO
    )
    logger.info('Старт ETL')
    etl(MOVIES, settings)
