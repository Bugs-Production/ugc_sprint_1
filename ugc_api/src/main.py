from core.config import settings as config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
