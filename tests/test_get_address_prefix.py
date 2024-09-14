import pytest

from umipy import Prefix, get_address_prefix


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "address, expected_prefix",
    [
        (
            "rod1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls547jk6",
            Prefix.ROD_TRADING,
        ),
        (
            "rod051xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls9rc78m",
            Prefix.KOSTENKO,
        ),
        (
            "rod131xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls5vae0x",
            Prefix.GUZMAN,
        ),
        (
            "rod191xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsdsejz4",
            Prefix.NEKRASOV,
        ),
        (
            "rod301xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls7q3dqm",
            Prefix.STAROSTENKO,
        ),
        (
            "rod361xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylswn2nud",
            Prefix.ROD_WALK,
        ),
        (
            "rod991xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls7q3dqm",
            Prefix.ROD_99,
        ),
        (
            "rod651xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls7q3dqm",
            Prefix.ROD_65,
        ),
        (
            "gls1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls3cmu2c",
            Prefix.GLIZE_STAKING,
        ),
        (
            "glz1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsqexcfq",
            Prefix.GLIZE,
        ),
        (
            "umi1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls83w7zj",
            Prefix.UMI,
        ),
        (
            "umi1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls83w7zj",
            Prefix.UMI,
        ),
        (
            "umistake1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylswu0l6g",
            Prefix.UMI_STAKING,
        ),
        (
            "umitrade1xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jylsz49rj7",
            Prefix.UMI_TRADING,
        ),
    ],
)
async def test_get_address_prefix(address: str, expected_prefix: Prefix):
    got_prefix = get_address_prefix(address)
    assert got_prefix == expected_prefix
