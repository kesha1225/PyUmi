from unittest.mock import AsyncMock

import pytest

from umipy import UmiPy, BalanceType


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
    umi: UmiPy,
    address: str,
    mock_response: dict,
    balance_type: BalanceType,
    expected_balance: float,
):
    mocker.patch.object(umi, "request", AsyncMock(return_value=mock_response))

    if balance_type is BalanceType.confirmed:
        assert (await umi.get_balance(address=address)).balance == expected_balance

    assert (
        await umi.get_balance(address=address, balance_type=balance_type)
    ).balance == expected_balance
