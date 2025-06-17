base_url = "https://ipv4.dynv6.com"

import asyncio
from typing import Tuple
import requests
from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
from loguru import logger


def get_ipv6_addresses():
    res = []
    for ifaceName in interfaces():
        for d in ifaddresses(ifaceName).setdefault(AF_INET6, [{'addr':None}] ):
            address = d['addr']
            if address is None:
                continue
            if address == "::1":
                continue
            if address.startswith("fe80::") and "%" in address:
                continue
            res.append(address)
    return res


def get_ipv4_addresses():
    res = []
    for ifaceName in interfaces():
        for d in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':None}] ):
            address = d['addr']
            if address is None:
                continue
            if address == "127.0.0.1":
                continue
            res.append(address)
    return res


def get_candidate_addresses() -> Tuple[str, str]:
    ipv6_addresses = get_ipv6_addresses()
    ipv4_addresses = get_ipv4_addresses()
    print(f"Get ipv4 address {ipv4_addresses} and ipv6 address {ipv6_addresses}")

    if len(ipv4_addresses) == 0:
        raise ValueError("No available ipv4 address!")
    if len(ipv6_addresses) == 0:
        raise ValueError("No available ipv6 address!")
    
    ipv4 = ipv4_addresses[0]
    ipv6 = ipv6_addresses[0]
    return ipv4, ipv6



async def ddns():
    with open("./config.yaml", mode='r', encoding='utf-8') as file:
        import yaml
        config = yaml.safe_load(file)
    while True:
        try:
           ipv4, ipv6 = get_candidate_addresses()
           response = requests.get(url=base_url, params={
                "zone": config["zone"],
                "token": config["token"],
                "ipv4": ipv4,
                "ipv6": ipv6
            })
           response.raise_for_status()
           logger.info("Updated DDNS.")
        except Exception as e:
            logger.error("Failed to update DDNS!")
            logger.exception(e)
        await asyncio.sleep(60 * 10)


if __name__ == "__main__":
    asyncio.run(ddns())
