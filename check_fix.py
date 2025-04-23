#!/usr/bin/env python3
import argparse
import requests
import urllib3

def check_host(host):
    """
    Connects via HTTPS to host + URI and prints FIXED if 403, otherwise NOT FIXED.
    """
    url = f"https://{host}/lang/custom/blabla"
    try:
        # disable certificate verification (adjust verify=True in production)
        resp = requests.get(url, verify=False, timeout=5)
        if resp.status_code == 403:
            print(f"{host} FIXED")
        else:
            print(f"{host} NOT FIXED")
    except requests.exceptions.RequestException as e:
        print(f"{host} ERROR: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Check /blabla/lang/custom/blabla on one or many hosts for HTTP 403"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--target",
        help="Single IP:port to check (e.g. 10.0.0.1:443)"
    )
    group.add_argument(
        "-f", "--file",
        help="Path to file with IP:port on each line"
    )
    args = parser.parse_args()

    # suppress InsecureRequestWarning when verify=False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if args.target:
        check_host(args.target)
    else:
        with open(args.file, 'r') as fh:
            for line in fh:
                host = line.strip()
                if host:
                    check_host(host)

if __name__ == "__main__":
    main()

