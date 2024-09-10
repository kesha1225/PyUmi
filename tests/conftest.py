import pytest

from umipy import UmiPy


@pytest.fixture
async def umi():
    umi_ = UmiPy()
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_testnet():
    umi_ = UmiPy(is_testnet=True)
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_testnet_legend():
    umi_ = UmiPy(is_testnet=True, is_legend=True)
    yield umi_
    await umi_.close()
