import pytest

from tests.utils import get_random_string
from umipy import UmiPy


@pytest.mark.asyncio
@pytest.mark.parametrize("message", [get_random_string() for _ in range(100)])
async def test_get_balance(umi: UmiPy, message: str):
    old_wallet = umi.generate_wallet()
    signed_message = umi.sign_message(
        message=message, private_key=old_wallet.keys.private_key
    )

    verify_result = umi.sign_verify(
        signature=signed_message, address=old_wallet.address, original_message=message
    )
    assert verify_result
