import datetime
from typing import Any, Sequence

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TradingResult
from src.schemas.trading_result import (
    TradingResultFilters,
    TradingResultDynamicsFilters,
)
from tests import fixtures
from tests.fixtures import FakeTradingResultService


@pytest.mark.asyncio(loop_scope='session')
class TestTradingResultService:
    class _TradingResultService(FakeTradingResultService):
        base_repository = 'trading_result'

    def __get_service(self, session: AsyncSession) -> FakeTradingResultService:
        return self._TradingResultService(session)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.SERVICE_TRADING_RESULT_GET_TRADING_RESULTS,
    )
    async def test_get_trading_results(
        self,
        values: dict,
        expected: Sequence[TradingResult],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        service = self.__get_service(transaction_session)
        with expectation:
            trading_results_in_db: Sequence[
                TradingResult
            ] = await service.get_trading_results(
                TradingResultFilters(**values)
            )
            assert len(trading_results_in_db) == len(expected)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.SERVICE_TRADING_RESULT_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        self,
        values: dict,
        expected: Sequence[TradingResult],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        service = self.__get_service(transaction_session)
        with expectation:
            trading_results_in_db: Sequence[
                TradingResult
            ] = await service.get_dynamics(
                TradingResultDynamicsFilters(**values)
            )
            assert len(trading_results_in_db) == len(expected)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.SERVICE_TRADING_RESULT_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        self,
        values: dict,
        expected: list[datetime.date],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        service = self.__get_service(transaction_session)
        with expectation:
            last_dates: list[
                datetime.date
            ] = await service.get_last_trading_dates(**values)
            assert len(last_dates) == len(expected)
