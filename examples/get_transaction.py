import asyncio

import aiohttp

from umipy import UmiPy


async def main():
    umi = UmiPy(session=aiohttp.ClientSession(), is_testnet=True)

    bad_trans_data = await umi.get_transaction(
        transaction_hash="ba8ad045020342980676146ea03a70477f7923159005be037daf8e81616d746c"
    )
    print(f"v1 tesnet: bad_trans_data rod v1 many send - {bad_trans_data}\n")
    bad_trans_data = await umi.get_transaction(
        transaction_hash="6f5857caf39db233fd118b33b3e242a58332ac8644c458b5762a070e8bb49a2"
    )
    print(f"v1 tesnet: bad_trans_data rod v1 wrong hash - {bad_trans_data}\n")
    good_trans_data = await umi.get_transaction(
        transaction_hash="f55049cdfaf33a1004c16b6cd381f81711993e6ca17ed7181f5c40ec4da10d51"
    )
    print(f"v1 tesnet: good_trans_data rod v1 - {good_trans_data}\n")
    await umi.close()

    umi = UmiPy(session=aiohttp.ClientSession(), is_legend=True, is_testnet=True)

    bad_trans_data = await umi.get_transaction(
        transaction_hash="1fd090de0225510871a26b67458948d49b0e5de04295d0c1f8b3d607720c4924"
    )
    print(f"legend testnet: bad_trans_data umi legend many send - {bad_trans_data}\n")
    bad_trans_data2 = await umi.get_transaction(
        transaction_hash="6fbb5a93fce2a6ba435c08157dd9c129234217fcf3711146b34da1963b6c1be"
    )
    print(f"legend testnet: bad_trans_data umi legend wrong hash - {bad_trans_data2}\n")
    good_trans_data = await umi.get_transaction(
        transaction_hash="b870b0b52e8398fa50eb54f1a1d7f27ab10a425df13301c155641e3fe4d67d65"
    )
    print(f"legend testnet: good_trans_data umi legend - {good_trans_data}\n")

    await umi.close()

    umi = UmiPy(session=aiohttp.ClientSession(), is_legend=True, is_testnet=False)

    good_trans_data = await umi.get_transaction(
        transaction_hash="7bdd8b4f9cd79158bf77af2e6696248b611ae8545f6c5ac91d3e87dcd29ae6cb"
    )
    print(f"legend mainnet: good orig legend - {good_trans_data}\n")

    await umi.close()

    umi = UmiPy(session=aiohttp.ClientSession(), is_testnet=False)
    bad_trans_data = await umi.get_transaction(
        transaction_hash="48bd9721e245866b95629ed39a3768f7c8aa466e14dca858fa7a7555c3408bec"
    )
    print(f"v1 mainnet: good v1 - {bad_trans_data}\n")

    await umi.close()


asyncio.run(main())
