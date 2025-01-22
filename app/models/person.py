from pydantic import Field

from .mixins import UUIDMixin


class FilmDTO(UUIDMixin):
    roles: list[str] = Field(default_factory=list)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data.pop("el_id", None)
        return data


class PersonInfoDTO(UUIDMixin):
    """Модель людей"""
    name: str = Field(default_factory=str)
    films: list[FilmDTO] = Field(default_factory=list)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data.pop("el_id", None)
        return data
