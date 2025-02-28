import base64
from typing import Sequence, Any

import aiohttp
from nacl.bindings import crypto_sign, crypto_sign_open
from nacl.exceptions import BadSignatureError

from umipy.enums import BalanceType, Prefix
from umipy.exceptions import UmiApiException
from umipy.generate_wallet import generate_wallet, restore_wallet
from umipy.helpers import get_api_url, get_send_version
from umipy.models import (
    BalanceResponse,
    TransactionsResponse,
    WalletResponse,
    Keys,
    TransactionResponse,
    SendResponse,
    Transaction,
    BalancesResponse,
    BalanceAddressData,
)
from umipy.transfer import transfer_addresses, to_public_key


class UmiPy:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        is_testnet: bool = False,
        is_legend: bool = False,
    ):
        base_url = get_api_url(is_testnet=is_testnet, is_legend=is_legend)
        self.base_url = base_url
        self.send_version = get_send_version(is_legend=is_legend)

        self.session = session

    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | str | None = None,
    ) -> Any:
        response = await self.session.request(
            method=method, url=f"{self.base_url}{path}", params=params, json=data
        )

        if response.status != 200:
            raise UmiApiException(f"Error {response.status} - {await response.text()}")

        json_response = await response.json()
        return json_response

    async def close(self) -> None:
        await self.session.close()

    async def get_balance(
        self, address: str, balance_type: BalanceType = BalanceType.confirmed
    ) -> BalanceResponse:
        response = await self.request("GET", f"/api/addresses/{address}/account")
        if "error" in response:
            return BalanceResponse(balance=0)

        if "confirmedBalanceMicro" in response["data"]:
            return BalanceResponse(
                balance=response["data"]["confirmedBalanceMicro"] / 1_000_000
            )

        return BalanceResponse(balance=response["data"][balance_type.value] / 100)

    async def get_balances_bulk(
        self,
        addresses: Sequence[str],
    ) -> BalancesResponse:
        response = await self.request(
            "POST", "/api/balances", data={"data": list(addresses)}
        )
        return BalancesResponse(
            items=list(
                map(
                    lambda balance: BalanceAddressData(
                        balance=balance["balance"] / 100, address=balance["address"]
                    ),
                    response["data"],
                )
            )
        )

    async def get_transactions(
        self, address: str, limit: int | None = None, offset: int | None = None
    ) -> TransactionsResponse:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await self.request(
            "GET",
            f"/api/addresses/{address}/transactions",
            params=params,
        )

        if "error" in response:
            return TransactionsResponse(total_count=0, items=[])

        return TransactionsResponse(**response["data"])

    def generate_wallet(self, prefix: Prefix = Prefix.UMI) -> WalletResponse:
        address, mnemonic, public_key, private_key = generate_wallet(prefix=prefix)
        return WalletResponse(
            address=address,
            mnemonic=mnemonic,
            keys=Keys(
                public_key=public_key, private_key=private_key, key_type="банан беби"
            ),
        )

    async def send_addresses(
        self,
        private_key: list[int],
        from_address: str,
        target_address: str,
        amount: float | int,
    ) -> SendResponse:
        encoded_data = transfer_addresses(
            private_key=private_key,
            from_address=from_address,
            to_address=target_address,
            amount=amount,
            send_version=self.send_version,
        )
        response = await self.request(
            method="POST", path="/api/mempool", data={"data": encoded_data}
        )

        return SendResponse(**response)

    def restore_wallet(
        self,
        mnemonic: str,
        prefix: Prefix = Prefix.UMI,
    ) -> WalletResponse:
        address, mnemonic, public_key, private_key = restore_wallet(
            mnemonic=mnemonic, prefix=prefix
        )
        return WalletResponse(
            address=address,
            mnemonic=mnemonic,
            keys=Keys(
                public_key=public_key, private_key=private_key, key_type="банан беби"
            ),
        )

    def sign_message(
        self,
        private_key: list[int],
        message: str,
    ) -> str:
        encoded_message = message.encode()
        result = crypto_sign(message=encoded_message, sk=bytes(private_key))

        return base64.b64encode(result[: -len(encoded_message)]).decode()

    def sign_verify(self, signature: str, original_message: str, address: str) -> bool:
        public_key = to_public_key(address)
        base64_sig = base64.b64decode(signature)

        base64_sig += original_message.encode()
        try:
            result = crypto_sign_open(signed=base64_sig, pk=bytes(public_key))
        except BadSignatureError:
            return False

        return result.decode() == original_message

    async def get_transaction(self, transaction_hash: str) -> TransactionResponse:
        response = await (
            await self.session.request(
                method="GET",
                url=f"{self.base_url}/api/transactions/{transaction_hash}",
            )
        ).json()
        if "error" in response:
            return TransactionResponse(
                status="error", code=500, message=response["error"]["message"]
            )
        return TransactionResponse(
            status="success", code=None, data=Transaction(**response["data"])
        )
