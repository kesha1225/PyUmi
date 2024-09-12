import base64

import aiohttp
from nacl.bindings import crypto_sign, crypto_sign_open
from nacl.exceptions import BadSignatureError

from umipy.constants import (
    Prefix,
    BASE_URL_MAINNET,
    BASE_STATS_URL_MAINNET,
    BASE_URL_TESTNET,
    BASE_STATS_URL_TESTNET,
    BASE_URL_LEGEND_MAINNET,
    BASE_URL_ORIGINAL_TESTNET,
)
from umipy.enums import BalanceType
from umipy.generate_wallet import generate_wallet, restore_wallet
from umipy.models import (
    BalanceResponse,
    TransactionsResponse,
    WalletResponse,
    Keys,
    TransactionResponse,
    InputTransactionsResponse,
    SendResponse,
    Transaction,
)
from umipy.transfer import transfer_coins, transfer_addresses, to_public_key


def get_api_urls(is_testnet: bool, is_legend: bool) -> tuple[str, str]:
    match (is_testnet, is_legend):
        case (True, True):
            return BASE_URL_TESTNET, BASE_STATS_URL_TESTNET
        case (True, False):
            return BASE_URL_ORIGINAL_TESTNET, BASE_STATS_URL_TESTNET
        case (False, True):
            return BASE_URL_LEGEND_MAINNET, BASE_STATS_URL_MAINNET
        case (False, False):
            return BASE_URL_MAINNET, BASE_STATS_URL_MAINNET


def get_send_version(is_legend: bool) -> int:
    if is_legend:
        return 100
    else:
        return 8


class UmiPy:
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        is_testnet: bool = False,
        is_legend: bool = False,
    ):
        base_url, stats_url = get_api_urls(is_testnet=is_testnet, is_legend=is_legend)
        self.is_legend = is_legend
        self.base_url = base_url
        self.base_stats_url = stats_url
        self.send_version = get_send_version(is_legend=is_legend)

        self.session = session or aiohttp.ClientSession()

    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        data: dict | str | None = None,
    ):
        response = await self.session.request(
            method=method, url=f"{self.base_url}{path}", params=params, json=data
        )
        json_response = await response.json()
        return json_response

    async def close(self):
        await self.session.close()

    async def get_balance(
        self, address: str, balance_type: BalanceType = BalanceType.confirmed
    ) -> BalanceResponse:
        response = await self.request("GET", f"/api/addresses/{address}/account")
        if "error" in response:
            return BalanceResponse(balance=0)

        return BalanceResponse(balance=response["data"][balance_type.value] / 100)

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

    async def get_input_transactions(
        self, address: str, limit: int | None = None, offset: int | None = None
    ) -> InputTransactionsResponse:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await (
            await self.session.request(
                method="GET",
                url=f"{self.base_stats_url}/address/{address}/transactions/received",
                params=params,
            )
        ).json()

        if response["status"] == "error":
            return InputTransactionsResponse(total_count=0, items=[])

        return InputTransactionsResponse(
            total_count=response["limit"], items=response["data"]
        )

    async def get_sent_transactions(
        self, address: str, limit: int | None = None, offset: int | None = None
    ) -> InputTransactionsResponse:
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await (
            await self.session.request(
                method="GET",
                url=f"{self.base_stats_url}/address/{address}/transactions/sended",
                params=params,
            )
        ).json()

        if response["status"] == "error":
            return InputTransactionsResponse(total_count=0, items=[])

        return InputTransactionsResponse(
            total_count=response["limit"], items=response["data"]
        )

    def generate_wallet(self, prefix: str = Prefix.UMI) -> WalletResponse:
        address, mnemonic, public_key, private_key = generate_wallet(prefix=prefix)
        return WalletResponse(
            address=address,
            mnemonic=mnemonic,
            keys=Keys(
                public_key=public_key, private_key=private_key, key_type="банан беби"
            ),
        )

    async def send(
        self,
        private_key: list[int],
        public_key: list[int],
        target_address: str,
        amount: float | int,
        prefix: str = Prefix.UMI,
    ) -> SendResponse:
        encoded_data = transfer_coins(
            public_key=public_key,
            private_key=private_key,
            target_address=target_address,
            amount=amount,
            prefix=prefix,
        )

        response = await self.request(
            method="POST", path=f"/api/mempool", data={"data": encoded_data}
        )
        if "error" in response:
            return SendResponse(status=False, send_data=response)

        return SendResponse(status=True, send_data=response)

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
            method="POST", path=f"/api/mempool", data={"data": encoded_data}
        )
        if "error" in response:
            return SendResponse(status=False, send_data=response)

        return SendResponse(status=True, send_data=response)

    def restore_wallet(
        self,
        mnemonic: str,
        prefix: str = Prefix.UMI,
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
        if self.is_legend:
            return await self._get_legend_transaction_from_node(
                transaction_hash=transaction_hash
            )

        response = TransactionResponse(
            **await (
                await self.session.request(
                    method="GET",
                    url=f"{self.base_stats_url}/transactions/{transaction_hash}",
                )
            ).json()
        )
        return response

    async def _get_legend_transaction_from_node(
        self, transaction_hash: str
    ) -> TransactionResponse:
        response = await (
            await self.session.request(
                method="GET",
                url=f"{self.base_url}/api/transactions/{transaction_hash}",
            )
        ).json()
        if "error" in response:
            return TransactionResponse(status="error", code=500, data=None)
        return TransactionResponse(
            status="success", code=None, data=Transaction(**response["data"])
        )
