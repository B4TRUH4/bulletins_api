__all__ = [
    'FakeBaseService',
    'FakeTradingResultService',
    'FakeUnitOfWork',
]

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import TradingResultService
from src.repositories import TradingResultRepository
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def __aenter__(self):
        self.trading_result = TradingResultRepository(self._session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.flush()


class FakeBaseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeTradingResultService(FakeBaseService, TradingResultService):
    base_repository: str = 'trading_result'
