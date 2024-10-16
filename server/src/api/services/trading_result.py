import datetime

from src.models import TradingResult
from src.schemas.trading_result import (
    TradingResultFilters,
    TradingResultDynamicsFilters,
)
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class TradingResultService(BaseService):
    base_repository: str = 'trading_result'

    @transaction_mode
    async def get_trading_results(
        self, filters: TradingResultFilters
    ) -> list[TradingResult]:
        kwargs = filters.model_dump(exclude_none=True)
        trading_results = await self.uow.trading_result.get_trading_results(
            **kwargs
        )
        return trading_results

    @transaction_mode
    async def get_last_trading_dates(self, days: int) -> list[datetime.date]:
        last_trading_dates: list[
            datetime.date
        ] = await self.uow.trading_result.get_last_trading_dates(days)
        return last_trading_dates

    @transaction_mode
    async def get_dynamics(
        self, filters: TradingResultDynamicsFilters
    ) -> list[TradingResult]:
        start_date = filters.start_date
        end_date = filters.end_date
        print(start_date, end_date)
        kwargs = filters.model_dump(
            exclude={'start_date', 'end_date'}, exclude_none=True
        )
        trading_results = await self.uow.trading_result.get_dynamics(
            start_date, end_date, **kwargs
        )
        return trading_results
