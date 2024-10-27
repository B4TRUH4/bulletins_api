import typing

from fastapi_cache.decorator import cache
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.services import TradingResultService
from src.schemas.trading_result import (
    TradingResultFilters,
    TradingResultDynamicsFilters,
    TradingResultListResponse,
    TradingResultDatesResponse,
)


if typing.TYPE_CHECKING:
    from src.models import TradingResult


router = APIRouter(prefix='/trading_results')


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=TradingResultListResponse,
)
@cache()
async def get_trading_results(
    filters: Annotated[TradingResultFilters, Depends()],
    service: TradingResultService = Depends(TradingResultService),
) -> TradingResultListResponse:
    trading_results: list[TradingResult] = await service.get_trading_results(
        filters
    )
    return TradingResultListResponse(
        payload=[result.to_pydantic_schema() for result in trading_results]
    )


@router.get(
    path='/last_trading_dates',
    status_code=status.HTTP_200_OK,
    response_model=TradingResultDatesResponse,
)
@cache()
async def get_last_trading_dates(
    days: int,
    service: TradingResultService = Depends(TradingResultService),
) -> TradingResultDatesResponse:
    trading_results_dates = await service.get_last_trading_dates(days)
    return TradingResultDatesResponse(payload=trading_results_dates)


@router.get(
    path='/dynamics',
    status_code=status.HTTP_200_OK,
    response_model=TradingResultListResponse,
)
@cache()
async def get_dynamics(
    filters: Annotated[TradingResultDynamicsFilters, Depends()],
    service: TradingResultService = Depends(TradingResultService),
) -> TradingResultListResponse:
    dynamics: list[TradingResult] = await service.get_dynamics(filters)
    return TradingResultListResponse(
        payload=[result.to_pydantic_schema() for result in dynamics]
    )
