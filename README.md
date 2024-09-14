# UMIPY
[![codecov](https://codecov.io/github/kesha1225/PyUmi/graph/badge.svg?token=PZ12EHSKAH)](https://codecov.io/github/kesha1225/PyUmi)

Interaction with umi blockchain


### Install

for stable version

`pip install umipy`

for dev version

`pip install https://github.com/RoyFractal/PyUmi/archive/master.zip` 


### Usage

You can find more examples - [examples/](examples/)

#### simple getting a address data

```python3
import asyncio
import aiohttp

from umipy import UmiPy


async def main():
    umi = UmiPy(session=aiohttp.ClientSession())
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
