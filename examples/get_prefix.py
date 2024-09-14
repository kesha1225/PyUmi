from umipy import get_address_prefix


def main():
    address1 = "rod1t6q9zdg9wnmet3hc9fwulsqa4qhd52fg53eqdwnx2wccp2czmllq3t302y"
    print(get_address_prefix(address1))
    address2 = "umi1570tt8sq40k3cahxt0xleaw4l20rwwnzvvupmlu6pcue4mhgm9cslgwvqk"
    print(get_address_prefix(address2))
    address3 = "rod371xhgwhyczqwphzh3zzluqch9j4uxargp6pnnn0fd9wgy7hq79jyls3c6kpn"
    print(get_address_prefix(address3))


main()
