import datetime
from typing import Sequence, Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TradingResult
from src.repositories import TradingResultRepository
from tests import fixtures


@pytest.mark.asyncio(loop_scope='session')
class TestTradingResultRepository:
    def __get_repository(
        self, session: AsyncSession
    ) -> TradingResultRepository:
        return TradingResultRepository(session)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.REPOSITORY_TRADING_RESULT_GET_TRADING_RESULTS,
    )
    async def test_get_trading_results(
        self,
        values: dict,
        expected: Sequence[TradingResult],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        service = self.__get_repository(transaction_session)
        with expectation:
            trading_results_in_db: Sequence[
                TradingResult
            ] = await service.get_trading_results(**values)
            assert len(trading_results_in_db) == len(expected)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.REPOSITORY_TRADING_RESULT_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        self,
        values: dict,
        expected: Sequence[TradingResult],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        repository = self.__get_repository(transaction_session)
        with expectation:
            trading_results_in_db: Sequence[
                TradingResult
            ] = await repository.get_dynamics(
                start_date=values['start_date'],
                end_date=values['end_date'],
            )
            assert len(trading_results_in_db) == len(expected)

    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        ('values', 'expected', 'expectation'),
        fixtures.test_cases.REPOSITORY_TRADING_RESULT_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        self,
        values: dict,
        expected: Sequence[datetime.date],
        expectation: Any,
        transaction_session: AsyncSession,
    ):
        repository = self.__get_repository(transaction_session)
        with expectation:
            last_dates: Sequence[
                datetime.date
            ] = await repository.get_last_trading_dates(**values)
            assert len(last_dates) == len(expected)
