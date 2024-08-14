import pytest

from umipy import UmiPy


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "address",
    [
        "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
    ],
)
async def test_get_balance(
    umi: UmiPy, address: str
):
    balance = (await umi.get_balance(address)).balance
    assert balance == 7544.22
