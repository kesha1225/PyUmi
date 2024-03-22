import enum


class BalanceType(str, enum.Enum):
    confirmed = "confirmedBalance"
    unconfirmed = "unconfirmedBalance"
