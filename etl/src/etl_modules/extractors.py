import logging
from abc import ABC, abstractmethod

import backoff
from aiokafka.errors import KafkaConnectionError, KafkaError
from etl_modules.brokers import KafkaBroker

logger = logging.getLogger("etl")


class BaseExtractor(ABC):
    @abstractmethod
    async def extract(self, data_source):
        pass


class KafkaExtractor(BaseExtractor):
    def __init__(self, data_source: KafkaBroker):
        self.kafka_consumer = data_source.consumer

    @backoff.on_exception(
        backoff.expo,
        KafkaConnectionError,
        max_tries=10,
        max_time=10,
    )
    async def extract(self):
        try:
            data = await self.kafka_consumer.getmany(timeout_ms=1000)
            if not data:
                logger.info("No messages received")
            else:
                for tp, messages in data.items():
                    for message in messages:
                        yield message.value
        except KafkaError as e:
            logger.error(f"Kafka error: {e}")
