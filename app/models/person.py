from pydantic import Field

from .mixins import UUIDMixin


class FilmDTO(UUIDMixin):
    roles: list[str] = Field(default_factory=list)


class PersonInfoDTO(UUIDMixin):
    """Модель людей"""
    name: str = Field(default_factory=str)
    roles: list[str] = Field(default_factory=list)
    films: list[FilmDTO] = Field(default_factory=list)
