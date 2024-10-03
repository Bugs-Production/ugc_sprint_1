from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from api.v1 import events
from brokers import kafka
from core.config import settings as config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        kafka.producer = AIOKafkaProducer(
            bootstrap_servers=f"{config.kafka_host}:{config.kafka_port}"
        )
        await kafka.producer.start()
        yield
    finally:
        await kafka.producer.stop()


app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
