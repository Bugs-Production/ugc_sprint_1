from aiokafka import AIOKafkaConsumer

from models.models import EventTypes
from settings.config import settings


class KafkaBroker:
    def __init__(self):
        topics = [e.value for e in EventTypes]
        self.consumer = AIOKafkaConsumer(
            *topics,
            group_id="etl",
            bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
        )

    async def __aenter__(self):
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.consumer.commit()
        await self.consumer.stop()
