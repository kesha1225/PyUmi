from typing import Union, Optional
from base64 import b64encode
from datetime import datetime
from random import random
from nacl.bindings.crypto_sign import crypto_sign

from umipy import bech32, Prefix


def to_public_key(address: str) -> list[int]:
    prefix, list_int, encoding = bech32.bech32_decode(address)
    public_key = bech32.convertbits(list_int, 5, 8, False)
    return public_key


def set_version(trx: list[int], version: int) -> None:
    trx.append(version)


def prefix_to_version(prefix: str) -> Optional[int]:
    if prefix == "genesis":
        return 0
    if len(prefix) != 3:
        return None
    a, b, c = tuple([ord(prefix[i]) - 96 for i in range(3)])
    return (a << 10) + (b << 5) + c


def to_2(value: int) -> list[int]:
    return [(value >> 8) & 0xFF, value & 0xFF]


def to_4(value: int) -> list[int]:
    res = [
        (value & 0xFF000000) >> 24,
        (value & 0x00FF0000) >> 16,
        (value & 0x0000FF00) >> 8,
        (value & 0x000000FF) >> 0,
    ]
    return res


def set_list(trx: list[int], address: list[int]) -> None:
    trx += address


def set_amount(trx: list[int], amount: Union[int, float]) -> None:
    amount_to_bytes: bytes = int(amount).to_bytes(8, "big")
    to_list: list[int] = [int(i) for i in amount_to_bytes]
    trx += to_list


def sign(trx: list[int], sk: list[int]) -> None:
    signature = crypto_sign(bytes(trx), bytes(sk))
    trx += signature[:64]


def sign_transaction(trx: list[int], sk: list[int]) -> None:
    seconds = round(datetime.now().timestamp() - 1)
    trx += to_4(seconds)
    trx += to_4(int(random() * 9999))
    trx.append(0)
    sign(trx, sk)


def transfer_coins(
    public_key: list[int],
    private_key: list[int],
    target_address: str,
    amount: Union[int, float],
    prefix: str | Prefix,
) -> str:
    trx: list[int] = []
    set_version(trx, 8)

    prefix_version = prefix_to_version(prefix)
    if prefix_version is None:
        return ""

    prefix_binary = to_2(prefix_version)
    from_addr = prefix_binary + public_key
    set_list(trx, from_addr)

    to_pk = to_public_key(target_address)
    to_addr = prefix_binary + to_pk
    set_list(trx, to_addr)

    set_amount(trx, amount * 100)

    sign_transaction(trx, private_key)

    return b64encode(bytes(trx)).decode()


def transfer_addresses(
    private_key: list[int],
    from_address: str,
    to_address: str,
    amount: Union[int, float],
) -> str:
    trx: list[int] = []
    set_version(trx, 8)

    token_to = to_address[:3]
    token_from = from_address[:3]

    prefix_binary_to = to_2(prefix_to_version(token_to))
    prefix_binary_from = to_2(prefix_to_version(token_from))

    from_pk = to_public_key(from_address)
    from_addr = prefix_binary_from + from_pk
    set_list(trx, from_addr)

    to_pk = to_public_key(to_address)
    to_addr = prefix_binary_to + to_pk
    set_list(trx, to_addr)

    set_amount(trx, amount * 100)

    sign_transaction(trx, private_key)

    return b64encode(bytes(trx)).decode()
