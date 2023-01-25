# UMIPY

Asynchronous python api wrapper for [umi-api](https://github.com/RoyFractal/umi-api)

Implements all methods from umi-api.

Now there are the following methods:
- /get_balance
- /get_transactions
- /generate_wallet
- /send
- /sign_message
- /restore_wallet

### Usage

You can find more examples - [examples/](examples/)

#### simple getting a address data

```python3
import asyncio

from umipy import UmiPy


async def main():
    umi = UmiPy()
    balance = await umi.get_balance(
        "umi17ymaed9h9hq7s5pc2f5fhmlzpmsk3qtc6g2cgm360zysz0uvq44qnxlsuz"
    )
    print(balance)

    trans = await umi.get_transactions(
        "umi17ymaed9h9hq7s5pc2f5fhmlzpmsk3qtc6g2cgm360zysz0uvq44qnxlsuz"
    )
    print(trans)

    await umi.close()


asyncio.run(main())
```
