from psycopg.sql import SQL, Identifier


class Query:
    """Класс SQL-запросов."""

    @staticmethod
    def get_genres_query(last_modified: str) -> SQL:
        return SQL(
            '''
            SELECT genres.id,
                   genres.name
            FROM content.genre AS genres
            WHERE genres.modified > {last_modified}
            GROUP BY genres.id
            ORDER BY MAX(genres.modified);
            '''
        ).format(
            last_modified=last_modified
        )

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
            WHERE fw.modified > {modified_time}
            GROUP BY fw.id
            ORDER BY fw.modified
            LIMIT 100;
            '''
        ).format(
            modified_time=modified_time
        )

    @staticmethod
    def check_modified(table, last_mod):
        return SQL(
            '''
            SELECT MAX(modified) AS last_modified
            FROM {table}
            WHERE modified > {last_mod}
            '''
        ).format(
            table=Identifier(f'content.{table}'),  # Указываем схему content
            last_mod=last_mod
        )
