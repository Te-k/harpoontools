import argparse
import json
from harpoon.lib.utils import bracket, unbracket
from harpoon.commands.ip import CommandIp
import geoip2.database


def ipinfo():
    parser = argparse.ArgumentParser(description='Give information on an IP')
    parser.add_argument('IP', type=str, nargs='*', default=[], help="IP addresses")
    parser.add_argument('--format', '-f', help='Output format',
            choices=["json", "csv", "txt"], default="txt")
    args = parser.parse_args()

    if len(args.IP):
        ips = args.IP
    else:
        with open("/dev/stdin") as f:
            ips = f.read().split()

    command = CommandIp()

    if len(ips) == 1:
        r = command.ipinfo(ips[0])
        if args.format == "txt":
            print("Information on IP %s" % ips[0])
            print("ASN: ASN%i - %s" % (r['asn'], r['asn_name'],))
            print("Location: %s - %s" % (r['city'], r['country']))
        elif args.format == "csv":
            print('%s;ASN%i;%s;%s;%s' % (
                    ips[0],
                    r['asn'],
                    r['asn_name'],
                    r['city'],
                    r['country']
                )
            )
        else:
            print(json.dumps(r, sort_keys=True, indent=4))
    else:
        for ip in ips:
            r = command.ipinfo(ip)
            if args.format == "txt":
                print('%s ASN%i %s %s %s' % (
                        ip,
                        r['asn'],
                        r['asn_name'],
                        r['city'],
                        r['country']
                    )
                )
            elif args.format == "csv":
                print('%s;ASN%i;%s;%s;%s' % (
                        ip,
                        r['asn'],
                        r['asn_name'],
                        r['city'],
                        r['country']
                    )
                )
            else:
                # JSON
                print(json.dumps({ip: r}, sort_keys=True, indent=4))
