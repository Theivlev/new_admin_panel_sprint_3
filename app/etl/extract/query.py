from psycopg.sql import SQL


class Query:
    """Класс SQL-запросов."""

    @staticmethod
    def get_genres_query(last_modified: str) -> SQL:
        return SQL(
            '''
            SELECT genres.id,
                   genres.name
            FROM content.genre AS genres
            WHERE genres.modified > %s
            GROUP BY genres.id
            ORDER BY MAX(genres.modified);
            '''
        ), (last_modified,)

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
                string_agg(DISTINCT p.full_name, ', ') FILTER (WHERE pfw.role = 'actor') AS actors_names,
                string_agg(DISTINCT d.full_name, ', ') FILTER (WHERE pfw.role = 'director') AS directors_names,
                string_agg(DISTINCT w.full_name, ', ') FILTER (WHERE pfw.role = 'writer') AS writers_names
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > %s
            GROUP BY fw.id
            ORDER BY fw.modified
            LIMIT 100;
            '''
        ), (modified_time,)

    @staticmethod
    def check_modified(table, last_mod):
        return SQL(
            '''
            SELECT MAX(modified) AS last_modified
            FROM %s
            WHERE modified > %s
            ''', (table, last_mod)
        )
