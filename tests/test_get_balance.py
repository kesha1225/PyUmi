import pytest

from umipy import UmiPy


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "address, balance",
    [
        ("glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq", 7544.22),  # some address meh
        ("glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfd", 0),  # broken address
    ],
)
async def test_get_balance(umi: UmiPy, address: str, balance: float):
    assert (await umi.get_balance(address)).balance == balance
