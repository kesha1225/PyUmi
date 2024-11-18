import time
from base64 import b64encode
from random import random
from nacl.bindings.crypto_sign import crypto_sign

from umipy import bech32
from umipy.enums import Prefix


class Transaction(list):
    def set_version(self, version: int) -> None:
        self.append(version)

    def set_list(self, address: list[int]) -> None:
        self.extend(address)

    def set_amount(self, amount: int | float) -> None:
        amount_to_bytes: bytes = int(amount).to_bytes(8, "big")
        to_list: list[int] = [int(i) for i in amount_to_bytes]
        self.extend(to_list)

    def sign(self, sk: list[int]) -> None:
        signature = crypto_sign(bytes(self), bytes(sk))
        self.extend(signature[:64])

    def sign_transaction(self, sk: list[int]) -> None:
        seconds = int(time.time()) - 10
        self.extend(to_4(seconds))
        self.extend(to_4(int(random() * 9999)))
        self.append(0)
        self.sign(sk=sk)


def to_public_key(address: str) -> list[int]:
    prefix, list_int, _ = bech32.bech32_decode(address)
    if list_int is None:
        raise ValueError(f"Invalid address, prefix is None {address=}")
    public_key = bech32.convertbits(list_int, 5, 8, False)
    return public_key


def prefix_to_version(prefix: Prefix) -> int | None:
    if prefix == "genesis":
        return 0

    if prefix == Prefix.UMI_TRADING:
        return 1

    if prefix == Prefix.UMI_STAKING:
        return 2

    if len(prefix) not in (3, 5):
        return None

    to_check = []
    for i in range(len(prefix)):
        modifier = 47 if any(char.isdigit() for char in prefix[i]) else 96
        to_check.append(ord(prefix[i]) - modifier)

    if len(to_check) > 3:
        return 32768 + ((to_check[3] << 5) + to_check[4])

    return (to_check[0] << 10) + (to_check[1] << 5) + to_check[2]


def to_2(value: int) -> list[int]:
    return [(value >> 8) & 0xFF, value & 0xFF]


def to_4(value: int) -> list[int]:
    return [
        (value & 0xFF000000) >> 24,
        (value & 0x00FF0000) >> 16,
        (value & 0x0000FF00) >> 8,
        (value & 0x000000FF) >> 0,
    ]


def transfer_addresses(
    private_key: list[int],
    from_address: str,
    to_address: str,
    amount: int | float,
    send_version: int,
) -> str:
    trx = Transaction()
    trx.set_version(send_version)

    if len(to_address) == 62:
        slicer_to = 3
    elif len(to_address) == 67:  # umistake | umitrade
        slicer_to = 8
    else:
        slicer_to = 5

    token_to = to_address[:slicer_to]

    if len(from_address) == 62:
        slicer_from = 3
    elif len(to_address) == 67:  # umistake | umitrade
        slicer_from = 8
    else:
        slicer_from = 5

    token_from = from_address[:slicer_from]
    
    version_to = prefix_to_version(prefix=Prefix(token_to))
    version_from = prefix_to_version(prefix=Prefix(token_from))
    
    if version_to is None:
        raise ValueError(f"Invalid address, prefix is None {token_to=}")
    if version_from is None:
        raise ValueError(f"Invalid address, prefix is None {token_from=}")
    
    prefix_binary_to = to_2(version_to)
    prefix_binary_from = to_2(version_from)

    from_pk = to_public_key(from_address)
    from_addr = prefix_binary_from + from_pk
    trx.set_list(from_addr)

    to_pk = to_public_key(to_address)
    to_addr = prefix_binary_to + to_pk
    trx.set_list(to_addr)

    trx.set_amount(amount * 100)

    trx.sign_transaction(private_key)

    return b64encode(bytes(trx)).decode()
