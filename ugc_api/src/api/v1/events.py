from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from schemas.events import SendEvent
from services.event import EventService, get_role_service
from services.exceptions import EventNotFound

router = APIRouter()


@router.post(
    "/",
    response_model=dict,
    summary="Добавление эвента",
    response_description="Добавление эвента в брокер Kafka",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешный запрос.",
            "content": {
                "application/json": {"example": {"detail": "Event sent successfully."}}
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных.",
            "content": {
                "application/json": {
                    "example": {"detail": "Input should be a valid string."}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Эвент не найден.",
            "content": {
                "application/json": {"example": {"detail": "Unsupported event type."}}
            },
        },
    },
)
async def add_event(
    event: SendEvent,
    event_service: EventService = Depends(get_role_service),
) -> dict:
    try:
        await event_service.send_event(event.dict())
        return {"detail": "Event sent successfully."}
    except EventNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
