from dataclasses import dataclass
from enum import Enum
from typing import Type

from psycopg.sql import SQL

from models.genre import GenreDTO
from models.movie import MovieDTO
from models.person import PersonInfoDTO


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
    query: SQL
    model: Type[GenreDTO | MovieDTO | PersonInfoDTO]
