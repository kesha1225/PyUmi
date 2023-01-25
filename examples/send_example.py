import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()
    my_mnemonic = "word1 word2 word3 ..."
    old_wallet = await umi.restore_wallet(my_mnemonic)
    # restore old wallet with balance by mnemonic

    new_wallet = await umi.generate_wallet()
    balance = await umi.get_balance(new_wallet.address)
    print(balance)  # 0
    # create new wallet

    send_result = await umi.send(
        old_wallet.keys.private_key,
        old_wallet.keys.public_key,
        target_address=new_wallet.address,
        amount=0.01,
    )
    print("send result -", send_result)
    await asyncio.sleep(1)
    balance = await umi.get_balance(new_wallet.address)
    print(balance)  # 0.01

    # send from new wallet to some other address
    result = await umi.send(
        new_wallet.keys.private_key,
        new_wallet.keys.public_key,
        target_address="umi1570tt8sq40k3cahxt0xleaw4l20rwwnzvvupmlu6pcue4mhgm9cslgwvqk",
        amount=0.01,
    )
    print(result)

    await umi.close()


asyncio.run(main())
