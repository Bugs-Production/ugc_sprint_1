import logging
from abc import ABC, abstractmethod

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError, SocketTimeoutError

from models.models import Event
from settings.config import settings

logger = logging.getLogger("etl")


class BaseLoader(ABC):
    @abstractmethod
    def load(self, data):
        pass


class ClickHouseLoader(BaseLoader):
    def __init__(self):
        self.client = Client(host="localhost")

    @backoff.on_exception(
        backoff.expo,
        [NetworkError, SocketTimeoutError],
        max_tries=10,
        max_time=10,
    )
    def load(self, data):
        try:
            columns = ", ".join(Event.model_fields.keys())
            events = [tuple(item.model_dump().values()) for item in data]
            query = (
                f"INSERT INTO {settings.ch_db}.{settings.ch_table} ({columns}) VALUES"
            )
            self.client.execute(query, events)
        except Exception as e:
            logger.error(e)


loader = ClickHouseLoader()
