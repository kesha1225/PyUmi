import typing

from umipy.constants import BECH32M_CONST, CHARSET
from umipy.enums import Encoding


def bech32_polymod(values: list[int]) -> int:
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp: str) -> list[int]:
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp: str, data: list[int]) -> Encoding | None:
    """Verify a checksum given HRP and converted data characters."""
    const = bech32_polymod(bech32_hrp_expand(hrp) + data)
    if const == 1:
        return Encoding.BECH32
    if const == BECH32M_CONST:
        return Encoding.BECH32M
    return None


def bech32_create_checksum(hrp: str, data: list[int], spec: int) -> list[int]:
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + data
    const = BECH32M_CONST if spec == Encoding.BECH32M else 1
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ const
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode(hrp: str, data: list[int], spec: int) -> str:
    """Compute a Bech32 string given HRP and data values."""
    combined = data + bech32_create_checksum(hrp, data, spec)
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def bech32_decode(
    address: str,
) -> tuple[str | None, list[int] | None, Encoding | None]:
    """Validate a Bech32/Bech32m string, and determine HRP and data."""

    # проверяем точно ли в строке символы с аски кодами от 33 до 126, исключаем пробелы и хуйню
    if any(ord(x) < 33 or ord(x) > 126 for x in address):
        return None, None, None

    # проверяем точно ли в строке все в только нижем или только венрхнем регистре
    if address.lower() != address and address.upper() != address:
        return None, None, None

    address = address.lower()

    pos = address.rfind("1")

    # если разделитель в самом начале или слишком близко к концу значит чета не то ну и адрес не больше 90
    if pos < 1 or pos + 7 > len(address) or len(address) > 90:
        return None, None, None

    # Каждый символ после разделителя должен быть одним из символов из набора, определённого в CHARSET
    if not all(x in CHARSET for x in address[pos + 1 :]):
        return None, None, None

    # все что до 1 это хрп все что после это адрес
    hrp = address[:pos]
    data = [CHARSET.find(x) for x in address[pos + 1 :]]
    spec = bech32_verify_checksum(hrp, data)
    if spec is None:
        return None, None, None
    return hrp, data[:-6], spec


def convertbits(
    data: list[int], frombits: int, tobits: int, pad: bool = True
) -> list[int] | typing.NoReturn:
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError(
                f"Bad convertbits {data=}, {frombits=}, {tobits=}, "
                f"value < 0 or (value >> frombits)"
            )
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError(
            f"Bad convertbits {data=}, {frombits=}, {tobits=}, "
            f"bits >= frombits or ((acc << (tobits - bits)) & maxv)"
        )
    return ret
