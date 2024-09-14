import asyncio

import aiohttp

from umipy import UmiPy


async def main():
    umi = UmiPy(session=aiohttp.ClientSession())

    some_wallet = umi.generate_wallet()
    print(some_wallet.mnemonic)
    signed = umi.sign_message(some_wallet.keys.private_key, "123")
    print(signed)
    await umi.close()


asyncio.run(main())
