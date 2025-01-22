import logging
from logging import config as logging_config
from dataclasses import dataclass
from enum import Enum
from psycopg.sql import SQL

from config.settings import Settings
from models.genre import GenreDTO
from models.movie import MovieDTO
from models.person import PersonInfoDTO
from utils.logger import LOGGING_CONFIG
from etl.etl import etl
from typing import Callable

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class Indexes(Enum):
    GENRES = 'genres'
    MOVIES = 'movies'
    PERSONS = 'persons'


class Tables(Enum):
    GENRE = 'genre'
    FILM_WORK = 'film_work'
    PERSON = 'person'


@dataclass
class ETL:
    index: Indexes
    table: Tables
    model: type[MovieDTO | GenreDTO | PersonInfoDTO]
    query: Callable[[str], SQL]


@dataclass
class ETLManager:
    settings: Settings

    def run_etl(self, etl_config: ETL):
        logger.info(
            '📊 Старт ETL процесса для индекса: %s и таблицы: %s',
            etl_config.index.value,
            etl_config.table.value
        )
        try:
            etl(etl_config, self.settings)
            logger.info(
                '✅ ETL процесс для индекса %s завершён успешно!',
                etl_config.index.value
            )
        except Exception as e:
            logger.error(
                '❌ Ошибка в ETL процессе для индекса %s: %s',
                etl_config.index.value,
                str(e),
                exc_info=True
            )
            raise
