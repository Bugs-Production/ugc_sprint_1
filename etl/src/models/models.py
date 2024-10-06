from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventTypes(Enum):
    CLICK = "click"
    PAGE_VIEW = "page_view"
    QUALITY_CHANGE = "quality_change"
    VIDEO_COMPLETE = "video_complete"
    SEARCH_FILTER_USE = "search_filter_use"


class Event(BaseModel):
    event_type: str
    timestamp: datetime
    user_id: UUID | None = None
    country: str | None = None
    device: str | None = None
    element: str | None = None
    page_url: str | None = None
    referrer_url: str | None = None
    video_id: str | None = None
    from_quality: str | None = None
    to_quality: str | None = None
    current_time: int | None = None
    duration: int | None = None
    filter_type: str | None = None
    filter_value: str | None = None
