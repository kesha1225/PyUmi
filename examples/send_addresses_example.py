import asyncio

from umipy import UmiPy, Prefix


async def main():
    umi = UmiPy()
    my_mnemonic = "word1 word2..."
    old_wallet = umi.restore_wallet(my_mnemonic, prefix=Prefix.ROD_TRADING)
    # restore old wallet with balance by mnemonic

    new_wallet = umi.generate_wallet(prefix=Prefix.ROD_TRADING)
    print(new_wallet.mnemonic)
    balance = await umi.get_balance(new_wallet.address)
    print(balance)  # 0
    # create new wallet

    amount = 0.02
    print(f"send from {old_wallet.address} to {new_wallet.address} {amount} GLZ")
    send_result = await umi.send_addresses(
        private_key=old_wallet.keys.private_key,
        from_address=old_wallet.address,
        target_address=new_wallet.address,
        amount=amount,
    )
    print("send result -", send_result)
    await asyncio.sleep(1)
    balance = await umi.get_balance(new_wallet.address)
    print(balance)  # 0.01

    await umi.close()


asyncio.run(main())
