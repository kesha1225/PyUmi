import pytest

from umipy import UmiPy, Prefix


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "prefix",
    [
        Prefix.UMI,
        Prefix.GLIZE,
        Prefix.GLIZE_STAKING,
        Prefix.DOSTATOK,
        Prefix.ROD_TRADING,
    ],
)
async def test_get_balance(umi_mainnet_v1: UmiPy, prefix: Prefix):
    wallet = umi_mainnet_v1.generate_wallet(prefix=prefix)
    restored = umi_mainnet_v1.restore_wallet(mnemonic=wallet.mnemonic, prefix=prefix)

    assert wallet.mnemonic == restored.mnemonic
    assert wallet.address == restored.address
    assert wallet.keys == restored.keys
