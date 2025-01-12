from pydantic import Field

from .mixins import UUIDMixin


class GenreDTO(UUIDMixin):
    """Модель жанров"""
    genre_name: str = Field(default_factory=str)
