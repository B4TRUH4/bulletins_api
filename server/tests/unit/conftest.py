from copy import deepcopy
from typing import Sequence

import pytest
import pytest_asyncio
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TradingResult
from src.utils.custom_types import AsyncFunc
from tests.fixtures.postgres import TRADING_RESULTS
from tests.utils import bulk_save_models


@pytest_asyncio.fixture
async def setup_trading_results(
    transaction_session: AsyncSession, trading_results: tuple[dict]
) -> None:
    await bulk_save_models(transaction_session, TradingResult, trading_results)


@pytest_asyncio.fixture
def get_trading_results(transaction_session: AsyncSession) -> AsyncFunc:
    async def _get_users() -> Sequence[TradingResult]:
        res: Result = await transaction_session.execute(select(TradingResult))
        return res.scalars().all()

    return _get_users


@pytest.fixture
def trading_results() -> tuple[dict]:
    return deepcopy(TRADING_RESULTS)
