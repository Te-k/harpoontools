# Harpoon Tools

CLI tools using [Harpoon](https://github.com/Te-k/harpoon) features

[![PyPI](https://img.shields.io/pypi/v/harpoontools)](https://pypi.org/project/harpoontools/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/harpoontools)](https://pypistats.org/packages/harpoontools) [![PyPI - License](https://img.shields.io/pypi/l/harpoontools)](LICENSE) [![GitHub issues](https://img.shields.io/github/issues/te-k/harpoontools)](https://github.com/Te-k/harpoontools/issues)

## Tools

* **ipinfo** : provides information on an IP address (ASN and location)
* **asninfo** : provides information on an ASN number
* **dns** : provides DNS information on a domain or IP
* **dnsresolve** : provinde IP information on a list of domains
* **asncount** : count IP addresses by ASN numbers
* **countrycount** : count IP addresses by countries
* **htraceroute**: traceroute adding AS and geolocation of IPs (you need to have traceroute installed)
* **myip**: get your public IP and location from ipinfo.io

## Install

Install [Harpoon](https://github.com/Te-k/harpoon) and then harpoontools :

```
pip install harpoon
pip install harpoontools
```

Configure Harpoon and download static files:
```
harpoon config -u
harpoon config
```

## Licence

This code is licensed under GPLv3
