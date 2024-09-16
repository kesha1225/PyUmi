import datetime

import pydantic
from pydantic import AliasChoices


class BalanceResponse(pydantic.BaseModel):
    balance: float


class Transaction(pydantic.BaseModel):
    height: int
    block_timestamp: str = pydantic.Field(
        validation_alias=AliasChoices("blockTimestamp", "block_timestamp")
    )
    block_height: int = pydantic.Field(
        validation_alias=AliasChoices("blockHeight", "block_height")
    )
    block_transaction_index: int = pydantic.Field(
        validation_alias=AliasChoices(
            "blockTransactionIndex", "block_transaction_index"
        )
    )
    hash: str
    type: str
    version: int
    amount: int
    sender_address: str = pydantic.Field(
        validation_alias=AliasChoices("senderAddress", "sender_address")
    )
    sender_account_type: str = pydantic.Field(
        validation_alias=AliasChoices("senderAccountType", "sender_account_type")
    )
    sender_account_balance: int = pydantic.Field(
        validation_alias=AliasChoices("senderAccountBalance", "sender_account_balance")
    )
    sender_account_interest_rate: int = pydantic.Field(
        validation_alias=AliasChoices(
            "senderAccountInterestRate", "sender_account_interest_rate"
        )
    )
    sender_account_transaction_count: int = pydantic.Field(
        validation_alias=AliasChoices(
            "senderAccountTransactionCount", "sender_account_transaction_count"
        )
    )
    recipient_amount: int = pydantic.Field(
        validation_alias=AliasChoices("recipientAmount", "recipient_amount")
    )
    recipient_address: str = pydantic.Field(
        validation_alias=AliasChoices("recipientAddress", "recipient_address")
    )
    recipient_account_type: str = pydantic.Field(
        validation_alias=AliasChoices("recipientAccountType", "recipient_account_type")
    )
    recipient_account_balance: int = pydantic.Field(
        validation_alias=AliasChoices(
            "recipientAccountBalance", "recipient_account_balance"
        )
    )
    recipient_account_interest_rate: int = pydantic.Field(
        validation_alias=AliasChoices(
            "recipientAccountInterestRate", "recipient_account_interest_rate"
        )
    )
    recipient_account_transaction_count: int = pydantic.Field(
        validation_alias=AliasChoices(
            "recipientAccountTransactionCount", "recipient_account_transaction_count"
        )
    )
    timestamp: str = pydantic.Field(
        validation_alias=AliasChoices("timestamp", "confirmed_at")
    )


class TransactionsResponse(pydantic.BaseModel):
    total_count: int = pydantic.Field(
        alias="totalCount", validation_alias=AliasChoices("totalCount", "total_count")
    )
    items: list[Transaction]


class InputTransactionsResponse(pydantic.BaseModel):
    total_count: int = pydantic.Field(
        alias="totalCount", validation_alias=AliasChoices("totalCount", "total_count")
    )
    items: list[Transaction]


class Keys(pydantic.BaseModel):
    public_key: list[int]
    private_key: list[int]
    key_type: str


class WalletResponse(pydantic.BaseModel):
    mnemonic: str
    keys: Keys
    address: str


class TransactionResponse(pydantic.BaseModel):
    status: str
    code: int | None = None
    data: Transaction | None = None
    message: str | None = None


class SendDataSuccess(pydantic.BaseModel):
    hash: str
    type: str
    version: int
    amount: int
    sender_address: str = pydantic.Field(alias="senderAddress")
    recipient_address: str = pydantic.Field(alias="recipientAddress")
    timestamp: datetime.datetime


class SendDataError(pydantic.BaseModel):
    code: int
    message: str


class SendResponse(pydantic.BaseModel):
    data: SendDataSuccess | None = None
    error: SendDataError | None = None
