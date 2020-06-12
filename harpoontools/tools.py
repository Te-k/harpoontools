import argparse
import re
import subprocess
import json
import requests
from harpoon.lib.utils import unbracket, is_ip
from harpoon.commands.ip import CommandIp
from harpoon.commands.asn import CommandAsn
from harpoon.commands.dnsc import CommandDns


def ipinfo():
    parser = argparse.ArgumentParser(description='Give information on an IP')
    parser.add_argument('IP', type=str, nargs='*', default=[], help="IP addresses")
    parser.add_argument('--format', '-f', help='Output format',
            choices=["json", "csv", "txt"], default="txt")
    parser.add_argument('--no-dns', '-n', help='No reverse DNS query', action='store_true')
    args = parser.parse_args()

    if len(args.IP):
        ips = args.IP
    else:
        with open("/dev/stdin") as f:
            ips = f.read().split()

    command = CommandIp()

    if len(ips) == 1:
        if is_ip(unbracket(ips[0])):
            r = command.ipinfo(unbracket(ips[0]), dns=not args.no_dns)
            if args.format == "txt":
                if r['asn'] == "":
                    print("IP not found")
                else:
                    print("Information on IP %s" % unbracket(ips[0]))
                    print("ASN: AS%i - %s - %s" % (r['asn'], r['asn_name'], r['asn_type']))
                    print("Location: %s - %s" % (r['city'], r['country']))
                    if not args.no_dns:
                        if r['hostname'] != '':
                            print('Hostname: %s' % r['hostname'])
                    if r['specific'] != '':
                        print("Specific: %s" % r['specific'])
            elif args.format == "csv":
                if r['asn'] == "":
                    print('%s;;;;;' % unbracket(ips[0]))
                else:
                    if args.no_dns:
                        print('%s;AS%i;%s;%s;%s;%s;%s' % (
                                unbracket(ips[0]),
                                r['asn'],
                                r['asn_name'],
                                r['asn_type'],
                                r['city'],
                                r['country'],
                                r['specific']
                            )
                        )
                    else:
                        print('%s;AS%i;%s;%s;%s;%s;%s' % (
                                unbracket(ips[0]),
                                r['asn'],
                                r['asn_name'],
                                r['asn_type'],
                                r['city'],
                                r['country'],
                                r['hostname'],
                                r['specific']
                            )
                        )
            else:
                print(json.dumps(r, sort_keys=True, indent=4))
        else:
            print("Invalid IP address")
    else:
        for ip in ips:
            if is_ip(unbracket(ip)):
                r = command.ipinfo(unbracket(ip), dns=not args.no_dns)
                if args.format in ["txt", "csv"]:
                    if r['asn'] == "":
                        print('%s ; ; ; ; ; ;' % unbracket(ip))
                    else:
                        if args.no_dns:
                            print('%s ; AS%i ; %s ; %s ; %s ; %s ; %s ' % (
                                    unbracket(ip),
                                    r['asn'],
                                    r['asn_name'],
                                    r['asn_type'],
                                    r['city'],
                                    r['country'],
                                    r['specific']
                                )
                            )
                        else:
                            print('%s ; AS%i ; %s ; %s ; %s ; %s ; %s ; %s' % (
                                    unbracket(ip),
                                    r['asn'],
                                    r['asn_name'],
                                    r['asn_type'],
                                    r['city'],
                                    r['country'],
                                    r['hostname'],
                                    r['specific']
                                )
                            )
                else:
                    # JSON
                    print(json.dumps({unbracket(ip): r}, sort_keys=True, indent=4))
            else:
                print("%s ; ; ; ; ; ; Invalid IP" % unbracket(ip))


def clean_asn(asn):
    """
    Take something either as 18345, ASn17839 or AS2893
    And returns just the number as a number
    """
    if asn.lower().startswith("asn"):
        return int(asn[3:])
    elif asn.lower().startswith("as"):
        return int(asn[2:])
    else:
        return int(asn)


def asninfo():
    parser = argparse.ArgumentParser(description='Give information on an ASN')
    parser.add_argument('ASN', type=str, nargs='*', default=[], help="ASN numbers")
    args = parser.parse_args()
    if len(args.ASN):
        asns = args.ASN
    else:
        with open("/dev/stdin") as f:
            asns = f.read().split()

    command = CommandAsn()
    for asn in asns:
        try:
            n = clean_asn(asn)
        except ValueError:
            print("%s : invalid ASN number" % asn)
        else:
            print("ASN%i ; %s" % (n, command.asnname(n)))


def dns():
    """
    Just a wrapper around the harpoon dns command
    """
    parser = argparse.ArgumentParser(description='Map DNS information for a domain or an IP address')
    command = CommandDns()
    command.add_arguments(parser)
    plugins = {'ip': CommandIp()}
    args = parser.parse_args()
    command.run({}, args, plugins)


def asncount():
    """
    Take a list of IP addresses as an IP and count them by ASN
    """
    parser = argparse.ArgumentParser(description='Count IP addresses by ASN')
    parser.add_argument('IP', type=str, nargs='*', default=[], help="IP addresses")
    args = parser.parse_args()

    if len(args.IP):
        ips = args.IP
    else:
        with open("/dev/stdin") as f:
            ips = f.read().split()

    ipc = CommandIp()
    asnc = CommandAsn()

    asns = {}
    error = False
    for ip in ips:
        if is_ip(unbracket(ip)):
            asninfo = ipc.ip_get_asn(unbracket(ip))
            if asninfo['asn'] not in asns:
                asns[asninfo['asn']] = 1
            else:
                asns[asninfo['asn']] += 1
        else:
            print('%s is not a valid IP address' % ip)
            error = True

    if error:
        print('')

    for asnn, nb in sorted(asns.items(), key=lambda x: x[1], reverse=True):
        if asnn == 0:
            name = "Unknown"
        else:
            name = asnc.asnname(asnn)
        print("%i\tASN%-6i\t%s" % (nb, asnn, name))


def countrycount():
    """
    Count country from which IPs are
    """
    parser = argparse.ArgumentParser(description='Count IP addresses by Country')
    parser.add_argument('IP', type=str, nargs='*', default=[], help="IP addresses")
    args = parser.parse_args()

    if len(args.IP):
        ips = args.IP
    else:
        with open("/dev/stdin") as f:
            ips = f.read().split()

    ipc = CommandIp()

    countries = {}
    error = False
    for ip in ips:
        if is_ip(unbracket(ip)):
            info = ipc.ipinfo(unbracket(ip), dns=False)
            if info['country'] not in countries:
                countries[info['country']] = 1
            else:
                countries[info['country']] += 1
        else:
            print('%s is not a valid IP address' % ip)
            error = True

    if error:
        print('')

    for cnn, nb in sorted(countries.items(), key=lambda x: x[1], reverse=True):
        print("%i\t%s" % (nb, cnn))


def traceroute():
    """
    Run traceroute with more information on IP addresses
    """
    parser = argparse.ArgumentParser(description='Run traceroute with more details on IPs')
    parser.add_argument('IP', type=str, help="IP addresses")
    args = parser.parse_args()
    rex = re.compile('\s*(?P<id>\d+)\s+(?P<name>\S+)\s+\((?P<ip>[\d\.]+)\)(\s+[\d\.]+\s+ms(\s+\S+\s\([\d\.]+\))?)+\s*')
    command = CommandIp()

    try:
        res = subprocess.run(
            ['traceroute', args.IP],
            capture_output=True,
            check=True
        )
        for l in res.stdout.decode('utf-8').split('\n'):
            if l.startswith('traceroute'):
                print(l)
            else:
                if len(l.strip()) > 0:
                    res = rex.match(l)
                    if res:
                        r = command.ipinfo(res.group('ip'), dns=False)
                        print(' %s %s\t%s\tAS%i\t%s\t%s\t%s' % (
                            res.group('id'),
                            res.group('ip'),
                            res.group('name'),
                            r['asn'],
                            r['asn_name'],
                            r['country'],
                            r['city']
                            )
                        )
                    else:
                        print(l)
    except subprocess.CalledProcessError:
        print('Something went wrong, do you have traceroute installed?')
    except FileNotFoundError:
        print('You have to install traceroute first')


def myip():
    r = requests.get("https://ipinfo.io/json")
    print(json.dumps(r.json(), sort_keys=True, indent=4))
