import datetime
from fastapi_cache.decorator import cache
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.services import TradingResultService
from src.schemas.trading_result import (
    TradingResultRetrieve,
    TradingResultFilters,
    TradingResultDynamicsFilters,
)
from src.models import TradingResult


router = APIRouter(prefix='/trading_results')


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[TradingResultRetrieve],
)
@cache()
async def get_trading_results(
    filters: Annotated[TradingResultFilters, Depends()],
    service: TradingResultService = Depends(TradingResultService),
) -> list[TradingResult]:
    trading_results = await service.get_trading_results(filters)
    return trading_results


@router.get(
    path='/last_trading_dates',
    status_code=status.HTTP_200_OK,
)
@cache()
async def get_last_trading_dates(
    days: int,
    service: TradingResultService = Depends(TradingResultService),
) -> list[datetime.date]:
    trading_results_dates = await service.get_last_trading_dates(days)
    return trading_results_dates


@router.get(
    path='/dynamics',
    status_code=status.HTTP_200_OK,
    response_model=list[TradingResultRetrieve],
)
@cache()
async def get_dynamics(
    filters: Annotated[TradingResultDynamicsFilters, Depends()],
    service: TradingResultService = Depends(TradingResultService),
) -> list[TradingResult]:
    dynamics = await service.get_dynamics(filters)
    return dynamics
