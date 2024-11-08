from unittest.mock import AsyncMock

import pytest

from umipy import UmiPy, BalanceType
from umipy.models import BalancesResponse


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "address, mock_response, balance_type, expected_balance",
    [
        (
            "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
            {"data": {"confirmedBalance": 754422}},
            BalanceType.confirmed,
            7544.22,
        ),
        (
            "umi1570tt8sq40k3cahxt0xleaw4l20rwwnzvvupmlu6pcue4mhgm9cslgwvqk",
            {"data": {"confirmedBalance": 0}},
            BalanceType.confirmed,
            0,
        ),
        (
            "rod201jy0wk999yfww58r5ykms4lsllg9p5jayzz0gtwxh7vx3e948s4qsgassg9",
            {"data": {"confirmedBalance": 100}},
            BalanceType.confirmed,
            1,
        ),
        (
            "rod011ug698khvxfykmqjhyn0culjzwmu2a0q208shatrc35hugf0uv4zq95chg4",
            {"data": {"confirmedBalance": 12345}},
            BalanceType.confirmed,
            123.45,
        ),
        (
            "rod011ug698khvxfykmqjhyn0culjzwmu2a0q208shatrc35hugf0uv4zq95chg4",
            {"data": {"unconfirmedBalance": 12345}},
            BalanceType.unconfirmed,
            123.45,
        ),
        (
            "rod011ug698khvxfykmqjhyn0culjzwmu2a0q208shatrc35hugf0uv4zq95chg4",
            {"data": {"unconfirmedBalance": 0}},
            BalanceType.unconfirmed,
            0,
        ),
        (
            "rod011ug698khvxfykmqjhyn0culjzwmu2a0q208shatrc35hugf0uv4zq95chg4",
            {"data": {"unconfirmedBalance": 1}},
            BalanceType.unconfirmed,
            0.01,
        ),
        (
            "rod011ug698khvxfykmqjhyn0culjzwmu2a0q208shatrc35hugf0uv4zq95chg4",
            {"data": {"unconfirmedBalance": 100000}},
            BalanceType.unconfirmed,
            1000,
        ),
    ],
)
async def test_get_confirmed_balance(
    mocker,
    umi_mainnet_v1: UmiPy,
    address: str,
    mock_response: dict,
    balance_type: BalanceType,
    expected_balance: float,
):
    mocker.patch.object(
        umi_mainnet_v1, "request", AsyncMock(return_value=mock_response)
    )

    if balance_type is BalanceType.confirmed:
        assert (
            await umi_mainnet_v1.get_balance(address=address)
        ).balance == expected_balance

    assert (
        await umi_mainnet_v1.get_balance(address=address, balance_type=balance_type)
    ).balance == expected_balance


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "addresses, mock_response, response_len",
    [
        (
            [
                "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
                "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
            ],
            {
                "items": [
                    {
                        "address": "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
                        "balance": 754422,
                    },
                    {
                        "address": "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
                        "balance": 754422,
                    },
                ]
            },
            2,
        )
    ],
)
async def test_get_bulk_balance(
    mocker,
    umi_mainnet_v1: UmiPy,
    addresses: list[str],
    mock_response: dict,
    response_len: float,
):
    mocker.patch.object(
        umi_mainnet_v1, "request", AsyncMock(return_value=mock_response)
    )

    response = BalancesResponse(**mock_response)

    assert len(response.items) == response_len
