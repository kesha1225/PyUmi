import aiohttp
import pytest

from umipy import UmiPy


@pytest.fixture
async def umi_mainnet_v1():
    umi_ = UmiPy(session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_testnet_v1():
    umi_ = UmiPy(is_testnet=True, session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_legend_testnet():
    umi_ = UmiPy(is_testnet=True, is_legend=True, session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()


@pytest.fixture
async def umi_legend_mainnet():
    umi_ = UmiPy(is_testnet=False, is_legend=True, session=aiohttp.ClientSession())
    yield umi_
    await umi_.close()
