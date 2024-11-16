import asyncio

import aiohttp

from umipy import UmiPy


async def main():
    umi = UmiPy(session=aiohttp.ClientSession())

    addresses = [
        "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
        "gls1kjmggptlgafkxaf3pqs473l893e928gnjlrhxntmlyvumdnvj8hsq07g4e",
        "gls1axur4xve407rsejjzr2ft75x80rh3s86w8s4sytflw6383fj4tjszvuh5y",
        "rod011xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylszx22gc",
        "rod1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls547jk6",
        "rod021xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls2mn9xn",
        "rod1fjl4nchvpt8xm30luacrt5s50g8uvn086fg5r4wfdc48s26uesfs34dvzm",
        "rod391fjl4nchvpt8xm30luacrt5s50g8uvn086fg5r4wfdc48s26uesfs2plhhz",
    ]

    addresses *= 100

    balances = await umi.get_balances_bulk(addresses=addresses)
    for balance in balances.items:
        print(balance.address, balance.balance)

    await umi.close()


asyncio.run(main())
