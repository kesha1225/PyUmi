import pytest

from umipy import UmiPy


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount, message",
    [
        (
            "ba8ad045020342980676146ea03a70477f7923159005be037daf8e81616d746c",
            "error",
            None,
            None,
            "Not Found",
        ),
        (
            "6f5857caf39db233fd118b33b3e242a58332ac8644c458b5762a070e8bb49a2",
            "error",
            None,
            None,
            "encoding/hex: odd length hex string",
        ),
        (
            "f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51",
            "success",
            55765323,
            1_00,
            None,
        ),
    ],
)
async def test_get_tx(
    umi_testnet_v1: UmiPy,
    tx_hash: str,
    status: str,
    height: str | None,
    amount: str | None,
    message: str,
):
    transaction_data = await umi_testnet_v1.get_transaction(tx_hash)
    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount

    assert transaction_data.message == message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount, message",
    [
        (
            "f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51",
            "success",
            55765323,
            100,
            None,
        ),
        (
            "6f3458c067c6ccc05bee8b5a30706c832a93ae1d965b93c2373ecf902f2403bd",
            "error",
            None,
            None,
            "Not Found",
        ),
        (
            "a7c96d1306889f7d211f1fb018239c9489f4396a19dd8a70bea83293c304a46d",
            "success",
            61653172,
            30_000_00,
            None,
        ),
        (
            "f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51",
            "success",
            55765323,
            1_00,
            None,
        ),
        (
            "6f3458c067c6ccc05bee8b5a30706c832a93ae1d965b93c2373ecf902f2403bd",
            "error",
            None,
            None,
            "Not Found",
        ),
        (
            "6f5857caf39db233fd118b33b3e242a58332ac8644c458b5762a070e8bb49a2",
            "error",
            None,
            None,
            "encoding/hex: odd length hex string",
        ),
    ],
)
async def test_get_tx(
    umi_mainnet_v1: UmiPy,
    tx_hash: str,
    status: str,
    height: str | None,
    amount: str | None,
    message: str,
):
    transaction_data = await umi_mainnet_v1.get_transaction(tx_hash)
    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount

    assert transaction_data.message == message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount, message",
    [
        (
            "3d361f1a2ca22d4b73cae4da641bc2cfe8e31da9583804ac0a351101225e9fbb",
            "success",
            18,
            10_00,
            None,
        ),
        (
            "6fbb5a93fc4e2a6ba435c08157dd9c129234217fcf3711146b34da1963b6c1be",
            "success",
            22,
            1,
            None,
        ),
        (
            "4a43760552510497ce135f6d0579e601f4ff8352ded5cf19f7e156a5dc73c2fe",
            "error",
            None,
            None,
            "Not Found",
        ),
        (
            "1fd090de0225510871a26b67458948d49b0e5de04295d0c1f8b3d607720c4924",
            "error",
            None,
            None,
            "Not Found",
        ),
        (
            "6fbb5a93fce2a6ba435c08157dd9c129234217fcf3711146b34da1963b6c1be",
            "error",
            None,
            None,
            "encoding/hex: odd length hex string",
        ),
        (
            "b870b0b52e8398fa50eb54f1a1d7f27ab10a425df13301c155641e3fe4d67d65",
            "success",
            30,
            1_00,
            None,
        ),
    ],
)
async def test_get_tx_legend(
    umi_legend_testnet: UmiPy,
    tx_hash: str,
    status: str,
    height: str | None,
    amount: str | None,
    message: str,
):
    transaction_data = await umi_legend_testnet.get_transaction(tx_hash)

    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount

    assert transaction_data.message == message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tx_hash, status, height, amount, message",
    [
        (
            "7bdd8b4f9cd79158bf77af2e6696248b611ae8545f6c5ac91d3e87dcd29ae6cb",
            "success",
            33,
            1,
            None,
        )
    ],
)
async def test_get_tx_legend(
    umi_legend_mainnet: UmiPy,
    tx_hash: str,
    status: str,
    height: str | None,
    amount: str | None,
    message: str,
):
    transaction_data = await umi_legend_mainnet.get_transaction(tx_hash)

    assert transaction_data.status == status

    if height:
        assert transaction_data.data.height == height

    if amount:
        assert transaction_data.data.amount == amount

    assert transaction_data.message == message
