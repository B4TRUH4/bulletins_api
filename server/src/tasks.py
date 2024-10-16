from celery import shared_task
from redis.utils import from_url

from src.config import settings


@shared_task
def clear_cache():
    redis = from_url(settings.REDIS_URL)
    keys = redis.keys('fastapi-cache*')
    if keys:
        redis.delete(*keys)
        print(f'Cleared cache. Deleted {len(keys)} keys.')
    else:
        print('No cache keys to delete.')
