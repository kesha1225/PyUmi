from umipy.constants import (
    BASE_URL_ORIGINAL_MAINNET,
    BASE_STATS_URL_ORIGINAL_MAINNET,
    BASE_URL_LEGEND_TESTNET,
    BASE_STATS_URL_ORIGINAL_TESTNET,
    BASE_URL_LEGEND_MAINNET,
    BASE_URL_ORIGINAL_TESTNET,
)
from umipy.enums import Prefix


def get_api_urls(is_testnet: bool, is_legend: bool) -> tuple[str, str | None]:
    match (is_legend, is_testnet):
        case (True, False):
            return BASE_URL_LEGEND_MAINNET, None
        case (True, True):
            return BASE_URL_LEGEND_TESTNET, None

        case (False, True):
            return BASE_URL_ORIGINAL_TESTNET, BASE_STATS_URL_ORIGINAL_TESTNET
        case (False, False):
            return BASE_URL_ORIGINAL_MAINNET, BASE_STATS_URL_ORIGINAL_MAINNET


def get_send_version(is_legend: bool) -> int:
    if is_legend:
        return 100
    else:
        return 8


def get_address_prefix(address: str) -> Prefix | None:
    sorted_prefixes = sorted(Prefix, key=len, reverse=True)

    for prefix in sorted_prefixes:
        if address.startswith(prefix):
            return Prefix(prefix)
    return None
