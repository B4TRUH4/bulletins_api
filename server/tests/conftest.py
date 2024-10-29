from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock
import pytest
import pytest_asyncio
import sqlalchemy
from asyncpg import connect
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from pytest_mock import MockFixture

from src.api.services import TradingResultService
from src.main import app
from src.models import Base
from src.config import settings
from tests.fixtures import FakeTradingResultService


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_db() -> None:
    """Creates a test database for the duration of the tests."""
    assert settings.MODE == 'TEST'

    db_url = (
        f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
        f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/'
    )
    test_db_name = settings.POSTGRES_DB
    if settings.POSTGRES_DB != 'test_database':
        return
    conn = await connect(dsn=db_url)
    db_exists = await conn.fetchval(
        f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'"
    )

    if not db_exists:
        await conn.execute(f'CREATE DATABASE {settings.POSTGRES_DB}')

    await conn.close()

    yield

    conn = await connect(dsn=db_url)
    await conn.execute(f'DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)')
    await conn.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine(create_test_db) -> AsyncEngine:
    """Creates and returns the test database engine."""
    engine = create_async_engine(
        'postgresql+asyncpg://postgres:postgres@db:5432/test_database',
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)
    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def setup_schemas(db_engine: AsyncEngine) -> None:
    """Creates schemas in the test database."""
    assert settings.MODE == 'TEST'

    schemas = ('schema_for_example',)

    async with db_engine.connect() as conn:
        for schema in schemas:
            schema_exists = await conn.execute(
                text(
                    f"SELECT schema_name FROM information_schema.schemata "
                    f"WHERE schema_name = '{schema}'"
                )
            )
            if not schema_exists:
                await conn.execute(sqlalchemy.schema.CreateSchema(schema))
            await conn.commit()


@pytest_asyncio.fixture(autouse=True)
async def setup_db(db_engine: AsyncEngine, setup_schemas: None) -> None:
    """Creates tables in the test database."""
    assert settings.MODE == 'TEST'

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)
        await db_conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def transaction_session(
    db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Returns a connection to the database.

    Any changes made to the database will NOT be applied,
    only for the duration of the TestCase.
    """
    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)
    yield session

    await session.rollback()
    await connection.close()


@pytest.fixture
def fake_trading_result_service(
    transaction_session: AsyncSession,
) -> Generator[FakeTradingResultService, None]:
    _fake_trading_result_service = FakeTradingResultService(transaction_session)
    yield _fake_trading_result_service


@pytest.fixture
def mock_cache(mocker: MockFixture) -> AsyncMock:
    mock_cache = mocker.patch(
        'fastapi_cache.decorator.cache', new_callable=AsyncMock
    )
    mock_cache.return_value = None
    FastAPICache.init(InMemoryBackend())
    return mock_cache


@pytest_asyncio.fixture
async def async_client(
    fake_trading_result_service: FakeTradingResultService,
    mock_cache: AsyncMock,
) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[TradingResultService] = (
        lambda: fake_trading_result_service
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
