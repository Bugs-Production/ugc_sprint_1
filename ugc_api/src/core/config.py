from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/ugc_api/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    project_name: str = Field("ugc_api", alias="PROJECT_NAME")


settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
