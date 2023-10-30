import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()
    balance = await umi.get_balance(
        "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq"
    )
    print(balance)

    trans = await umi.get_transactions(
        "umi17ymaed9h9hq7s5pc2f5fhmlzpmsk3qtc6g2cgm360zysz0uvq44qnxlsuz"
    )
    print(trans)

    await umi.close()


asyncio.run(main())
