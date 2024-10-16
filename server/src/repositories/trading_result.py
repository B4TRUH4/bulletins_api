import datetime
from typing import Sequence

from sqlalchemy import select, Result, func

from src.models import TradingResult
from src.utils.repository import SqlAlchemyRepository


class TradingResultRepository(SqlAlchemyRepository):
    model = TradingResult

    async def get_trading_results(self, **kwargs) -> Sequence[model]:
        recent_date = select(func.max(self.model.date)).scalar_subquery()
        query = (
            select(self.model)
            .filter(self.model.date == recent_date)
            .filter_by(**kwargs)
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def get_last_trading_dates(
        self, days: int
    ) -> Sequence[datetime.date]:
        query = (
            select(self.model.date)
            .order_by(self.model.date.desc())
            .distinct()
            .limit(days)
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def get_dynamics(
        self, start_date: str, end_date: str, **kwargs
    ) -> Sequence[model]:
        query = (
            select(self.model)
            .filter(self.model.date >= start_date, self.model.date <= end_date)
            .filter_by(**kwargs)
            .order_by(self.model.date)
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()
