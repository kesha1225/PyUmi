import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()

    bad_trans_data = await umi.get_transaction(
        transaction_hash="6f3458c067c6ccc05bee8b5a30706c832a93ae1d965b93c2373ecf902f2403bd"
    )
    print(bad_trans_data)
    good_trans_data = await umi.get_transaction(
        transaction_hash="f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51"
    )
    print(good_trans_data)
    await umi.close()


asyncio.run(main())
