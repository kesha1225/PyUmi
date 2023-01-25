from typing import Optional, Union

import aiohttp

from umipy.models import BalanceResponse, TransactionsResponse, WalletResponse

BASE_URL = "https://api.umipay.me"


class Prefix:
    UMI = "umi"
    GLIZE = "glz"


class UmiPy:
    def __init__(
        self, session: Optional[aiohttp.ClientSession] = None, base_url: str = BASE_URL
    ):
        self.base_url = base_url
        self.session = session or aiohttp.ClientSession()

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        response = await self.session.request(
            method, f"{self.base_url}/{path}", params=params, data=data
        )
        json_response = await response.json()
        return json_response

    async def close(self):
        await self.session.close()

    async def get_balance(self, address: str) -> BalanceResponse:
        return BalanceResponse(**await self.request("GET", f"get_balance/{address}"))

    async def get_transactions(
        self, address: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> TransactionsResponse:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return TransactionsResponse(
            **(
                await self.request(
                    "GET",
                    f"get_transactions/{address}",
                    params=params,
                )
            )["transactions"]
        )

    async def generate_wallet(self, prefix: Prefix = Prefix.UMI) -> WalletResponse:
        return WalletResponse(
            **(
                await self.request(
                    "POST",
                    f"generate_wallet",
                    data={"prefix": prefix},
                )
            )["wallet"]
        )

    async def send(
        self,
        private_key: list[int],
        public_key: list[int],
        target_address: str,
        amount: Union[float, int],
        prefix: Prefix = Prefix.UMI,
    ) -> bool:
        return (
            await self.request(
                "POST",
                f"send",
                data={
                    "prefix": prefix,
                    "privateKey": private_key,
                    "publicKey": public_key,
                    "targetAddress": target_address,
                    "amount": amount,
                },
            )
        )["result"]

    async def restore_wallet(
        self,
        mnemonic: str,
        prefix: Prefix = Prefix.UMI,
    ) -> WalletResponse:
        return WalletResponse(
            **(
                await self.request(
                    "POST",
                    f"restore_wallet",
                    data={
                        "prefix": prefix,
                        "mnemonic": mnemonic,
                    },
                )
            )["result"]
        )

    async def sign_message(
        self,
        private_key: list[int],
        message: str,
    ) -> str:
        return (
            await self.request(
                "POST",
                f"sign_message",
                data={
                    "privateKey": private_key,
                    "message": message,
                },
            )
        )["result"]
