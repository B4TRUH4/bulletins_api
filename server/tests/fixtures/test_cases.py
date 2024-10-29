import datetime
from copy import deepcopy

from src.models import TradingResult
from tests.fixtures.postgres import TRADING_RESULTS
from contextlib import nullcontext as does_not_raise

SERVICE_TRADING_RESULT_GET_TRADING_RESULTS = [
    (
        {},
        [TradingResult(**result) for result in TRADING_RESULTS[:2]],
        does_not_raise(),
    ),
    (
        {'delivery_type_id': 'F'},
        [
            TradingResult(**TRADING_RESULTS[0]),
        ],
        does_not_raise(),
    ),
    ({'delivery_type_id': 'not_existing_id'}, [], does_not_raise()),
]

SERVICE_TRADING_RESULT_GET_DYNAMICS = [
    (
        {
            'start_date': datetime.date(year=2024, month=9, day=21),
            'end_date': datetime.date(year=2024, month=9, day=23),
        },
        [TradingResult(**result) for result in TRADING_RESULTS[2:5]],
        does_not_raise(),
    ),
    (
        {
            'start_date': datetime.date(year=2024, month=1, day=1),
            'end_date': datetime.date(year=2024, month=1, day=10),
        },
        [],
        does_not_raise(),
    ),
]

SERVICE_TRADING_RESULT_GET_LAST_TRADING_DATES = [
    (
        {'days': 10},
        [datetime.date(year=2024, month=9, day=day) for day in range(20, 25)],
        does_not_raise(),
    ),
    (
        {'days': 3},
        [datetime.date(year=2024, month=9, day=day) for day in range(22, 25)],
        does_not_raise(),
    ),
]

REPOSITORY_TRADING_RESULT_GET_TRADING_RESULTS = deepcopy(
    SERVICE_TRADING_RESULT_GET_TRADING_RESULTS
)

REPOSITORY_TRADING_RESULT_GET_DYNAMICS = deepcopy(
    SERVICE_TRADING_RESULT_GET_DYNAMICS
)

REPOSITORY_TRADING_RESULT_GET_LAST_TRADING_DATES = deepcopy(
    SERVICE_TRADING_RESULT_GET_LAST_TRADING_DATES
)

API_TRADING_RESULT_ROUTE_GET_TRADING_RESULTS = [
    (
        'api/trading_results/',
        {},
        200,
        [
            {
                'id': 87856,
                'exchange_product_id': 'A592AKR060F',
                'exchange_product_name': 'Бензин (АИ-92-К5) по ГОСТ, ст. '
                                         'Аксарайская II (ст. отправления)',
                'oil_id': 'A592',
                'delivery_basis_id': 'AKR',
                'delivery_basis_name': 'ст. Аксарайская II',
                'delivery_type_id': 'F',
                'volume': 2700,
                'total': 163987680,
                'count': 38,
                'date': '2024-09-24',
            },
            {
                'id': 87855,
                'exchange_product_id': 'A592ACH005A',
                'exchange_product_name': 'Бензин (АИ-92-К5) по ГОСТ, Ачинский '
                                         'НПЗ (самовывоз автотранспортом)',
                'oil_id': 'A592',
                'delivery_basis_id': 'ACH',
                'delivery_basis_name': 'Ачинский НПЗ',
                'delivery_type_id': 'A',
                'volume': 50,
                'total': 3300000,
                'count': 2,
                'date': '2024-09-24',
            },
        ],
        does_not_raise(),
    ),
    (
        'api/trading_results/?delivery_type_id=F',
        {},
        200,
        [
            {
                'id': 87856,
                'exchange_product_id': 'A592AKR060F',
                'exchange_product_name': 'Бензин (АИ-92-К5) по ГОСТ, '
                                         'ст. Аксарайская II (ст. отправления)',
                'oil_id': 'A592',
                'delivery_basis_id': 'AKR',
                'delivery_basis_name': 'ст. Аксарайская II',
                'delivery_type_id': 'F',
                'volume': 2700,
                'total': 163987680,
                'count': 38,
                'date': '2024-09-24',
            },
        ],
        does_not_raise(),
    ),
    (
        'api/trading_results/?delivery_type_id=not_existing_id',
        {},
        200,
        [],
        does_not_raise(),
    ),
]

API_TRADING_RESULT_ROUTE_GET_LAST_TRADING_DATES = [
    (
        'api/trading_results/last_trading_dates?days=10',
        {},
        200,
        [
            '2024-09-24',
            '2024-09-23',
            '2024-09-22',
            '2024-09-21',
            '2024-09-20',
        ],
        does_not_raise(),
    ),
    (
        'api/trading_results/last_trading_dates?days=3',
        {},
        200,
        [
            '2024-09-24',
            '2024-09-23',
            '2024-09-22',
        ],
        does_not_raise(),
    ),
]


API_TRADING_RESULT_ROUTE_GET_DYNAMICS = [
    (
        'api/trading_results/dynamics?start_date=2024-09-22&end_date=2024-09-23',
        {},
        200,
        [
            {
                'id': 87858,
                'exchange_product_id': 'A592ANK060F',
                'exchange_product_name': 'Бензин (АИ-92-К5) по ГОСТ, Ангарск-'
                                         'группа станций (ст. отправления)',
                'oil_id': 'A592',
                'delivery_basis_id': 'ANK',
                'delivery_basis_name': 'Ангарск-группа станций',
                'delivery_type_id': 'F',
                'volume': 240,
                'total': 15193080,
                'count': 4,
                'date': '2024-09-22',
            },
            {
                'id': 87857,
                'exchange_product_id': 'A592ALL060F',
                'exchange_product_name': 'Бензин (АИ-92-К5) по ГОСТ, ст. '
                                         'Аллагуват (ст. отправления)',
                'oil_id': 'A592',
                'delivery_basis_id': 'ALL',
                'delivery_basis_name': 'ст. Аллагуват',
                'delivery_type_id': 'F',
                'volume': 1500,
                'total': 87713640,
                'count': 18,
                'date': '2024-09-23',
            },
            # Тут можно было сделать и так. Не знаю, как лучше:
            # TradingResultDB(**result).model_dump(mode='json')
            # for result in TRADING_RESULTS[3:1:-1]
        ],
        does_not_raise(),
    )
]
