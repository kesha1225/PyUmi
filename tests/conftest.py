import aiohttp
import pytest

from umipy import UmiPy


@pytest.fixture
async def umi():
    umi_ = UmiPy(session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_testnet():
    umi_ = UmiPy(is_testnet=True, session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_testnet_legend():
    umi_ = UmiPy(is_testnet=True, is_legend=True, session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()
