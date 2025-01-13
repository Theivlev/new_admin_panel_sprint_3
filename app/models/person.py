from pydantic import Field

from .mixins import UUIDMixin


class PersonInfoDTO(UUIDMixin):
    full_name: str = Field(default_factory=str)
