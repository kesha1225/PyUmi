import asyncio

import aiohttp

from umipy import UmiPy


async def main():
    umi = UmiPy(session=aiohttp.ClientSession(), is_legend=True, is_testnet=False)

    res = await umi.get_transactions(
        address="umistake1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylswu0l6g",
        limit=10,
        offset=0,
    )
    print(res)
    await umi.close()


asyncio.run(main())
