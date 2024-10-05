from datetime import datetime
from typing import Type

from pydantic import BaseModel, field_validator


class EventTypes:
    CLICK = "click"
    PAGE_VIEW = "page_view"
    QUALITY_CHANGE = "quality_change"
    VIDEO_COMPLETE = "video_complete"
    SEARCH_FILTER_USE = "search_filter_use"


class BaseEvent(BaseModel):
    event_type: str
    timestamp: datetime
    user_id: str | None
    country: str
    device: str

    @field_validator("event_type")
    def validate_event_type(cls, v):
        if v not in EVENT_MODEL_MAP.keys():
            raise ValueError(f"Invalid event_type: {v}")
        return v


class ClickEvent(BaseEvent):
    event_type: str = EventTypes.CLICK
    element: str
    page_url: str


class PageViewEvent(BaseEvent):
    event_type: str = EventTypes.PAGE_VIEW
    page_url: str
    referrer_url: str | None


class QualityChangeEvent(BaseEvent):
    event_type: str = EventTypes.QUALITY_CHANGE
    video_id: str
    from_quality: str
    to_quality: str
    current_time: int


class VideoCompleteEvent(BaseEvent):
    event_type: str = EventTypes.VIDEO_COMPLETE
    video_id: str
    duration: int


class SearchFilterUseEvent(BaseEvent):
    event_type: str = EventTypes.SEARCH_FILTER_USE
    filter_type: str
    filter_value: str


EVENT_MODEL_MAP: dict[str, Type[BaseModel]] = {
    EventTypes.CLICK: ClickEvent,
    EventTypes.PAGE_VIEW: PageViewEvent,
    EventTypes.QUALITY_CHANGE: QualityChangeEvent,
    EventTypes.VIDEO_COMPLETE: VideoCompleteEvent,
    EventTypes.SEARCH_FILTER_USE: SearchFilterUseEvent,
}
