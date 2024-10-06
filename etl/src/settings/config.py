from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BATCH_SIZE = 50


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    ch_host: str = Field("clickhouse-node1", alias="CH_HOST")
    ch_port: int = Field(9000, alias="CH_PORT")
    ch_db: str = Field("example", alias="CH_DB")
    ch_table: str = Field("events", alias="CH_TABLE")
    ch_user: str = Field("default", alias="CH_USER")
    ch_password: str = Field("default", alias="CH_PASSWORD")
    kafka_host: str = Field("kafka", alias="KAFKA_HOST")
    kafka_port: int = Field(29092, alias="KAFKA_PORT")
    scheduler_interval_seconds: int = Field(60, alias="SCHEDULER_INTERVAL_SECONDS")


settings = Settings()
