from abc import ABC, abstractmethod
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from brokers.kafka import get_kafka_producer
from fastapi import Depends
from models.event import EVENT_MODEL_MAP
from pydantic import ValidationError

from .exceptions import EventNotFound


class BaseEventService(ABC):
    """Абстрактный класс для работы с эвентами"""

    @abstractmethod
    async def send_event(self, event) -> None:
        pass


class EventService(BaseEventService):
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self._producer = kafka_producer

    async def send_event(self, event: dict) -> None:
        try:
            # определяем модель по типу события
            event_data = event.get("event")
            event_model = EVENT_MODEL_MAP.get(event_data.get("event_type"))

            # если модель найдена, валидируем событие
            if event_model:
                validated_event = event_model(**event_data)
                await self._producer.send_and_wait(
                    validated_event.event_type, validated_event.json().encode("utf-8")
                )
            else:
                raise EventNotFound(f"Unsupported event type")

        except ValidationError as e:
            raise ValidationError(f"Validation error for event: {e.errors()}")


@lru_cache()
def get_role_service(
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> EventService:
    return EventService(kafka_producer)
