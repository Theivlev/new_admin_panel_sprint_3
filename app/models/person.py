from pydantic import Field

from .mixins import UUIDMixin


class PersonInfoDTO(UUIDMixin):
    full_name: str = Field(default_factory=str)


class RolesDTO(UUIDMixin):
    roles: list[str] = Field(default_factory=list)


class PersonDTO(PersonInfoDTO):
    films: list[RolesDTO] = Field(default_factory=list)
