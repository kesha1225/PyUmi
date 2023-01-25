import pydantic


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


class TransactionsResponse(pydantic.BaseModel):
    total_count: int = pydantic.Field(alias="totalCount")
    items: list[Transaction]


class Keys(pydantic.BaseModel):
    public_key: list[int] = pydantic.Field(alias="publicKey")
    private_key: list[int] = pydantic.Field(alias="privateKey")
    key_type: str = pydantic.Field(alias="keyType")


class WalletResponse(pydantic.BaseModel):
    mnemonic: str
    keys: Keys
    address: str
