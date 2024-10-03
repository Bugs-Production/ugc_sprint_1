from pydantic import BaseModel


class SendEvent(BaseModel):
    event: dict
