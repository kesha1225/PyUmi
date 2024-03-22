import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()

    trans_data = await umi.get_input_transactions(
        address="rod1t6q9zdg9wnmet3hc9fwulsqa4qhd52fg53eqdwnx2wccp2czmllq3t302y",
        limit=300,
    )
    print(len(trans_data.items))

    await umi.close()


asyncio.run(main())
