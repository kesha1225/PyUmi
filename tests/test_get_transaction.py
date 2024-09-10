import pytest

from umipy import UmiPy


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount",
    [
        (
            "f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51",
            "success",
            55765323,
            100,
        ),
        (
            "6f3458c067c6ccc05bee8b5a30706c832a93ae1d965b93c2373ecf902f2403bd",
            "error",
            None,
            None,
        ),
        (
            "a7c96d1306889f7d211f1fb018239c9489f4396a19dd8a70bea83293c304a46d",
            "success",
            61653172,
            30_000_00,
        ),
        (
            "4eb15719e1be5ba8a59dedc22f1138c0ad88b0c7ea8b9ea08754f0d34d6da9fd",
            "success",
            61570731,
            40_01,
        ),
    ],
)
async def test_get_tx(
    umi: UmiPy, tx_hash: str, status: str, height: str | None, amount: str | None
):
    transaction_data = await umi.get_transaction(tx_hash)
    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount",
    [
        (
            "3d361f1a2ca22d4b73cae4da641bc2cfe8e31da9583804ac0a351101225e9fbb",
            "success",
            18,
            10_00,
        ),
        (
            "6fbb5a93fc4e2a6ba435c08157dd9c129234217fcf3711146b34da1963b6c1be",
            "success",
            22,
            1,
        ),
        (
            "4a43760552510497ce135f6d0579e601f4ff8352ded5cf19f7e156a5dc73c2fe",
            "error",
            None,
            None,
        ),
    ],
)
async def test_get_tx_legend(
    umi_testnet_legend: UmiPy,
    tx_hash: str,
    status: str,
    height: str | None,
    amount: str | None,
):
    transaction_data = await umi_testnet_legend.get_transaction(tx_hash)

    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount
