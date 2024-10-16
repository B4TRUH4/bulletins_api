from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    MODE: str = 'TEST'


class CelerySettings(BaseSettings):
    broker_url: str = Field(alias='CELERY_BROKER_URL')
    result_backend: str = Field(alias='CELERY_RESULT_BACKEND')


settings = Settings()
celery_settings = CelerySettings()
