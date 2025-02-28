from hashlib import pbkdf2_hmac, sha256
from mnemonic import Mnemonic

from nacl.bindings import crypto_sign_seed_keypair

from umipy import bech32
from umipy.enums import Prefix


def generate_mnemo_words() -> str:
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=256)


def to_seed(words: str) -> bytes:
    return pbkdf2_hmac("sha512", words.encode(), "mnemonic".encode(), 2048)


def to_unsigned_list_int(seed: bytes) -> list[int]:
    to_sha256 = sha256(seed).hexdigest()
    return [int(to_sha256[i : i + 2], 16) for i in range(0, len(to_sha256), 2)]


def generate_pk_sk(unsigned_list_int: list[int]) -> tuple[list[int], list[int]]:
    public_key, secret_key = crypto_sign_seed_keypair(bytes(unsigned_list_int))
    return [int(i) for i in public_key], [int(i) for i in secret_key]


def generate_wallet_address(public_key: list[int], prefix: Prefix) -> str:
    convert_bits = bech32.convertbits(public_key, 8, 5, True)
    return bech32.bech32_encode(prefix, convert_bits, 0)


def generate_wallet(prefix: Prefix) -> tuple[str, str, list[int], list[int]]:
    mnemo = generate_mnemo_words()
    seed = to_seed(mnemo)
    unsigned_int = to_unsigned_list_int(seed)
    pk, sk = generate_pk_sk(unsigned_int)
    address = generate_wallet_address(pk, prefix=prefix)
    return address, mnemo, pk, sk


def restore_wallet(
    mnemonic: str, prefix: Prefix
) -> tuple[str, str, list[int], list[int]]:
    seed = to_seed(mnemonic)
    unsigned_int = to_unsigned_list_int(seed)
    pk, sk = generate_pk_sk(unsigned_int)
    address = generate_wallet_address(pk, prefix=prefix)
    return address, mnemonic, pk, sk
