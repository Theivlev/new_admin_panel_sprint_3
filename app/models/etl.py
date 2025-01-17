from dataclasses import dataclass
from enum import Enum

from models.movie import MovieDTO


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
    index: str
    table: str
    model: type[MovieDTO]
