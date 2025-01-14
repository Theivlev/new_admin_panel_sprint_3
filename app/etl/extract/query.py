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
                fw.id,
                fw.title,
                fw.description,
                fw.rating,
                fw.type,
                fw.created,
                fw.modified,
                COALESCE (
                    json_agg(
                        DISTINCT jsonb_build_object(
                            'person_role', pfw.role,
                            'person_id', p.id,
                            'person_name', p.full_name
                        )
                    ) FILTER (WHERE p.id IS NOT NULL),
                    '[]'
                ) AS persons,
                array_agg(DISTINCT g.name) AS genres
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
