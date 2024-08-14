import pytest

from umipy import UmiPy


@pytest.fixture
async def umi():
    umi_ = UmiPy()
    yield umi_
    await umi_.close()
