import logging
from abc import ABC, abstractmethod
from uuid import UUID

from models.models import Event

logger = logging.getLogger("etl")


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, data):
        pass


class EventTransformer(BaseTransformer):
    def transform(self, data):
        try:
            event_model = Event(
                event_type=data["event_type"],
                timestamp=data["timestamp"],
                user_id=UUID(data.get("user_id", None)),
                country=data.get("country", None),
                device=data.get("device", None),
                element=data.get("element", None),
                page_url=data.get("page_url", None),
                referrer_url=data.get("referrer_url", None),
                video_id=data.get("video_id", None),
                from_quality=data.get("from_quality", None),
                to_quality=data.get("to_quality", None),
                current_time=data.get("current_time", None),
                duration=data.get("duration", None),
                filter_type=data.get("filter_type", None),
                filter_value=data.get("filter_value", None),
            )
            return event_model
        except Exception as e:
            logger.error(e)


event_transformer = EventTransformer()
