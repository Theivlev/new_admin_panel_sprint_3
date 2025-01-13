import logging

from logging import config as logging_config


from psycopg.errors import ConnectionFailure
from psycopg.sql import SQL, Identifier, Placeholder

from config.postgres import PostgresClient
from state.state import State
from utils.logger import LOGGING_CONFIG
from utils.backoff import backoff


logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)
