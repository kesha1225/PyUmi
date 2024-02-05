import pydantic
from pydantic import AliasChoices, validator, field_validator


class BalanceResponse(pydantic.BaseModel):
    balance: float


class Transaction(pydantic.BaseModel):
    height: int
    block_timestamp: str = pydantic.Field(alias="blockTimestamp")
    block_height: int = pydantic.Field(alias="blockHeight")
    block_transaction_index: int = pydantic.Field(alias="blockTransactionIndex")
    hash: str
    type: str
    version: int
    amount: int
    sender_address: str = pydantic.Field(alias="senderAddress")
    sender_account_type: str = pydantic.Field(alias="senderAccountType")
    sender_account_balance: int = pydantic.Field(alias="senderAccountBalance")
    sender_account_interest_rate: int = pydantic.Field(
        alias="senderAccountInterestRate"
    )
    sender_account_transaction_count: int = pydantic.Field(
        alias="senderAccountTransactionCount"
    )
    recipient_amount: int = pydantic.Field(alias="recipientAmount")
    recipient_address: str = pydantic.Field(alias="recipientAddress")
    recipient_account_type: str = pydantic.Field(alias="recipientAccountType")
    recipient_account_balance: int = pydantic.Field(alias="recipientAccountBalance")
    recipient_account_interest_rate: int = pydantic.Field(
        alias="recipientAccountInterestRate"
    )
    recipient_account_transaction_count: int = pydantic.Field(
        alias="recipientAccountTransactionCount"
    )
    timestamp: str


class StatsTransaction(pydantic.BaseModel):
    height: int
    block_timestamp: str
    block_height: int
    block_transaction_index: int | None
    hash: str
    type: str
    version: int
    amount: int | None

    sender_address: str
    sender_account_type: str
    sender_account_balance: int | None
    sender_account_interest_rate: int | None
    sender_account_transaction_count: int
    recipient_amount: int | None
    recipient_address: str
    recipient_account_type: str
    recipient_account_balance: int | None
    recipient_account_interest_rate: int | None
    recipient_account_transaction_count: int
    fee_amount: int | None = None
    fee_address: str | None = None
    fee_account_balance: str | None = None
    fee_account_interest_rate: int | None
    fee_account_transaction_count: int | None

    # fee_percent
    # nft
    sender: str
    recipient: str
    value: int

    confirmed_at: str

    # block_tx_idx


class TransactionsResponse(pydantic.BaseModel):
    total_count: int = pydantic.Field(
        alias="totalCount", validation_alias=AliasChoices("totalCount", "total_count")
    )
    items: list[Transaction]


class InputTransactionsResponse(pydantic.BaseModel):
    total_count: int = pydantic.Field(
        alias="totalCount", validation_alias=AliasChoices("totalCount", "total_count")
    )
    items: list[StatsTransaction]


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
