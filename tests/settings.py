from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    service_url: str = "http://127.0.0.1"


test_settings = TestSettings()
