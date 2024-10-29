from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str

    REDIS_URL: str

    MODE: str


class CelerySettings(BaseSettings):
    broker_url: str = Field(alias='CELERY_BROKER_URL')
    result_backend: str = Field(alias='CELERY_RESULT_BACKEND')


settings = Settings()
celery_settings = CelerySettings()
