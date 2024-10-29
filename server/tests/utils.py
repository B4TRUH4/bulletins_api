from typing import Iterable, Any, Sequence

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from requests import Response


async def bulk_save_models(
    session: AsyncSession,
    model: type[DeclarativeBase],
    data: Iterable[dict[str, Any]],
    *,
    commit: bool = False,
) -> None:
    for values in data:
        await session.execute(insert(model).values(**values))
    if commit:
        await session.commit()
    else:
        await session.flush()


def prepare_payload(
    response: Response, exclude: Sequence[str] | None = None
) -> dict:
    """Extracts the payload from the response."""
    payload = response.json().get('payload')
    if payload is None:
        return {}

    if exclude is None:
        return payload

    for key in exclude:
        payload.pop(key, None)

    return payload
