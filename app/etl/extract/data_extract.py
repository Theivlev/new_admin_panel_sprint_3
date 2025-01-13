import logging

from logging import config as logging_config


from psycopg.errors import ConnectionFailure

from config.postgres import PostgresClient
from state.state import State
from utils.logger import LOGGING_CONFIG
from utils.backoff import backoff
from dataclasses import dataclass
from models.etl import ETL
from extract.query import Query

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


@dataclass
class PostgresExtractor:

    postgres_client: PostgresClient
    state: State
    etl: ETL
    batch_size: int

    @backoff(ConnectionFailure)
    def check_modified(self, prev_mod: str) -> str | None:

        self.postgres_client.cursor.execute(
            Query.check_modified(self.etl.table, prev_mod)

        )
        return self.postgres_client.cursor.fetchone()[0]

    @backoff(ConnectionFailure)
    def extract(self):
        """Extract movies from Postgres."""

        prev_mod = self.state.get_state(self.etl.index)

        if last_modified := self.check_modified(prev_mod):
            logger.info('Extracting new %s data', self.etl.index)

            self.postgres_client.cursor.execute(
                Query.check_modified(self.etl.table, prev_mod)
            )

            while data := self.postgres_client.cursor.fetchmany(
                size=self.batch_size
            ):
                yield data, str(last_modified)
