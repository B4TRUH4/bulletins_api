import datetime

from pydantic import BaseModel


class TradingResultRetrieve(BaseModel):
    id: int
    exchange_product_id: str | None = None
    exchange_product_name: str | None = None
    oil_id: str | None = None
    delivery_basis_id: str | None = None
    delivery_basis_name: str | None = None
    delivery_type_id: str | None = None
    volume: int | None = None
    total: int | None = None
    count: int | None = None
    date: datetime.date


class TradingResultFilters(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None


class TradingResultDynamicsFilters(TradingResultFilters):
    start_date: datetime.date
    end_date: datetime.date
