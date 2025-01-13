import logging
from logging import config as logging_config

from models.genre import GenreDTO
from models.movie import MovieDTO
from models.person import PersonInfoDTO
from utils.logger import LOGGING_CONFIG
from dataclasses import dataclass


logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


@dataclass
class DataTransform:

    model: type[GenreDTO | MovieDTO | PersonInfoDTO]

    def data_transform(self, batch: list[dict]) -> list[dict]:

        return [self.model(**data).model_dump() for data in batch]


# @dataclass
# class DataTransform:

#     model: type[GenreDTO | MovieDTO | PersonInfoDTO]

#     def data_transform(self, batch: list[dict]) -> list[dict]:
#         result = []

#         for item in batch:
#             # Преобразуем persons в список объектов PersonInfoDTO
#             persons = [PersonInfoDTO(**person) for person in item.pop('persons', [])]
#             # Присваиваем список жанров
#             genres = item.pop('genres', [])
#             # Создаем объект модели
#             movie_instance = self.model(**item)
#             # Добавляем преобразованные данные
#             result.append({
#                 **movie_instance.model_dump(),
#                 'persons': persons,
#                 'genres': genres
#             })

#         return result