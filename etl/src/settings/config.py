from pydantic_settings import BaseSettings, SettingsConfigDict

BATCH_SIZE = 50


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    ch_host: str = "localhost"
    ch_port: int = 9000
    ch_db: str = "example"
    ch_table: str = "events"
    ch_user: str = "default"
    ch_password: str = "default"
    kafka_host: str = "localhost"
    kafka_port: int = 29092
    scheduler_interval_seconds: int = 60


settings = Settings()
