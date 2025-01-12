from pydantic import Field
from .genre import GenreDTO
from .person import PersonInfoDTO
from mixins import UUIDMixin


class Movie(UUIDMixin):
    """Модель фильма"""
    title: str
    imdb_rating: float | None = Field(default=None)
    description: str | None = Field(default=None)
    genres: list[GenreDTO] = Field(default_factory=list)
    actors: list[PersonInfoDTO] = Field(default_factory=list)
    directors: list[PersonInfoDTO] = Field(default_factory=list)
    writers: list[PersonInfoDTO] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
