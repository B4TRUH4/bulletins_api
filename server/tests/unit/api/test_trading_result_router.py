from typing import Any

import pytest
from httpx import AsyncClient

from tests import fixtures
from tests.utils import prepare_payload


@pytest.mark.asyncio(loop_scope='session')
class TestTradingResultRouter:
    @staticmethod
    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        (
            'url',
            'headers',
            'expected_status_code',
            'expected_payload',
            'expectation',
        ),
        fixtures.test_cases.API_TRADING_RESULT_ROUTE_GET_TRADING_RESULTS,
    )
    async def test_get_trading_results(
        url: str,
        headers: dict,
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload

    @staticmethod
    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        (
            'url',
            'headers',
            'expected_status_code',
            'expected_payload',
            'expectation',
        ),
        fixtures.test_cases.API_TRADING_RESULT_ROUTE_GET_LAST_TRADING_DATES,
    )
    async def test_get_last_trading_dates(
        url: str,
        headers: dict,
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload

    @staticmethod
    @pytest.mark.usefixtures('setup_trading_results')
    @pytest.mark.parametrize(
        (
            'url',
            'headers',
            'expected_status_code',
            'expected_payload',
            'expectation',
        ),
        fixtures.test_cases.API_TRADING_RESULT_ROUTE_GET_DYNAMICS,
    )
    async def test_get_dynamics(
        url: str,
        headers: dict,
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload
