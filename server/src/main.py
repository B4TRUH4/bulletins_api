from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, BackgroundTasks
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.config import settings
from src.metadata import TITLE, TAG_METADATA, DESCRIPTION, VERSION

from src.api import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield


def create_fastapi_app() -> FastAPI:
    if settings.MODE == 'PROD':
        fastapi_app = FastAPI(
            lifespan=lifespan,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None,
        )
    else:
        fastapi_app = FastAPI(
            lifespan=lifespan,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
        )

    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fastapi_app()

# async def clear_cache_task():
#     redis = aioredis.from_url(settings.REDIS_URL)
#     keys = await redis.keys("fastapi-cache*")
#     if keys:
#         await redis.delete(*keys)
#         print(f"Cleared cache. Deleted {len(keys)} keys.")
#     else:
#         print("No cache keys to delete.")
#
#
# async def startup_event():
#     scheduler = AsyncIOScheduler()
#     trigger = CronTrigger(hour=16, minute=8, timezone='')
#     import tzlocal
#     print(tzlocal.get_localzone())
#     scheduler.add_job(clear_cache_task, trigger)
#     scheduler.start()
#     print("Scheduler started")
