import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()

    trans_data = await umi.get_input_transactions(
        address="glz1ajlr7tx8csegkkwqn93c3ntsszqelrdr4z77ak05fctpl6yrvnpql8f0uv",
        limit=300,
    )
    print(len(trans_data.items))

    await umi.close()


asyncio.run(main())
