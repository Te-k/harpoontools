import argparse
import sys
from harpoon.lib.utils import bracket, unbracket
from harpoon.commands.ip import CommandIP
import geoip2.database


def ipinfo():
    usage = """
ipinfo : Give details on an IP address
"""
    ips = sys.argv[1:]
    if not ips:
        with open("/dev/stdin") as f:
            ips = f.read().split()

    c = CommandIP()

    for ip in ips:
        print(c.ipinfo(ip))

