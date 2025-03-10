from umipy import bech32
from umipy.constants import (
    BASE_URL_ORIGINAL_MAINNET,
    BASE_URL_LEGEND_TESTNET,
    BASE_URL_LEGEND_MAINNET,
    BASE_URL_ORIGINAL_TESTNET,
)
from umipy.enums import Prefix, SendVersion


def get_api_url(is_testnet: bool, is_legend: bool) -> str:
    match (is_legend, is_testnet):
        case (True, False):
            return BASE_URL_LEGEND_MAINNET
        case (True, True):
            return BASE_URL_LEGEND_TESTNET
        case (False, True):
            return BASE_URL_ORIGINAL_TESTNET
        case (False, False):
            return BASE_URL_ORIGINAL_MAINNET
        case _:
            raise ValueError(
                f"Invalid combination of is_testnet and is_legend {is_testnet=}, {is_legend=}"
            )


def get_send_version(is_legend: bool) -> int:
    # if is_legend:
    #     return SendVersion.LEGEND_DEFAULT  # 100 для не-микротранзакций
    if is_legend:
        return SendVersion.LEGEND_MICRO
    else:
        return SendVersion.ROD


def get_address_prefix(address: str) -> Prefix | None:
    prefix, _, _ = bech32.bech32_decode(address=address)
    if prefix is None:
        return None
    return Prefix(prefix)
