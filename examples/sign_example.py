import asyncio

import aiohttp

from umipy import UmiPy, Prefix


async def main():
    umi = UmiPy(session=aiohttp.ClientSession())

    my_mnemonic = "word1 word2 ..."
    old_wallet = umi.restore_wallet(my_mnemonic, prefix=Prefix.GLIZE)

    message = "test1234"
    signed_message = umi.sign_message(
        message=message, private_key=old_wallet.keys.private_key
    )
    print(signed_message)

    verify_result = umi.sign_verify(
        signature=signed_message, address=old_wallet.address, original_message=message
    )
    print(verify_result)

    await umi.close()


asyncio.run(main())
