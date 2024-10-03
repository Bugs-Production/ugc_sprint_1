from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    ch_host: str = "localhost"
    ch_port: int = 9000
    ch_database: str = "example"
    ch_table: str = "events"
    ch_user: str = "default"
    ch_password: str = "default"


settings = Settings()
