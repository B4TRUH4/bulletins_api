__all__ = [
    'router',
]

from fastapi import APIRouter
from src.api.routers import trading_result_router

router = APIRouter()
router.include_router(trading_result_router, tags=['Trading Result'])
