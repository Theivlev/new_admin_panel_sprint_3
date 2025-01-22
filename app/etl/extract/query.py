import logging

from logging import config as logging_config
from psycopg.sql import SQL, Identifier

from utils.logger import LOGGING_CONFIG


logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class Query:
    """Класс SQL-запросов."""

    @staticmethod
    def get_films_query(modified_time: str) -> SQL:
        return SQL(
            '''
            SELECT
                fw.id AS id,
                fw.title AS title,
                fw.description AS description,
                fw.rating AS imdb_rating,
                COALESCE(
                    jsonb_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id,
                            'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'actor'),
                    '[]'
                ) AS actors,
                COALESCE(
                    jsonb_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id,
                            'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'director'),
                    '[]'
                ) AS directors,
                COALESCE(
                    jsonb_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id,
                            'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'writer'),
                    '[]'
                ) AS writers,
                array_agg(DISTINCT g.name) AS genres,
                COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor'), ARRAY[]::text[]) AS actors_names,
                COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director'), ARRAY[]::text[]) AS directors_names,
                COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer'), ARRAY[]::text[]) AS writers_names
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > {modified_time}
                  OR p.modified > {modified_time}
                  OR g.modified > {modified_time}
            GROUP BY fw.id
            ORDER BY fw.modified
            '''
        ).format(
            modified_time=modified_time
        )

    @staticmethod
    def check_modified(table, last_mod):

        logger.info(
            'Проверка последнего изменения для таблицы: %s с last_mod: %s',
            table,
            last_mod
        )

        query = SQL(
                '''
                SELECT MAX(modified) AS last_modified
                FROM {table}
                WHERE modified > {last_mod}
                '''
            ).format(
                table=Identifier('content', table),
                last_mod=last_mod
            )

        return query

    @staticmethod
    def get_genres_query(table, last_mod):
        pass

    @staticmethod
    def get_persons_query(table, last_mod):
        pass
