#!/usr/bin/env python3

import argparse
import json
import requests
import urllib3
import socket
import struct
from pathlib import Path

def parse_devices(path):
    text = Path(path).read_text()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        devices = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            devices.append(json.loads(line))
        return devices

def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))

def check_path(ip, port, path):
    url = f"https://{ip}:{port}{path}"
    resp = requests.get(url, verify=False, timeout=5)
    return resp.status_code

def load_ip_file(path):
    lines = Path(path).read_text().splitlines()
    targets = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue
        ip, port = line.split(':', 1)
        targets.append((ip, port))
    return targets

def print_banner():
    banner = r"""
  _____ _______ _____  ______  _____ _____ _______ 
 |_   _|__   __|  __ \|  ____|/ ____|_   _|__   __|
   | |    | |  | |__) | |__  | (___   | |    | |   
   | |    | |  |  _  /|  __|  \___ \  | |    | |   
  _| |_   | |  | | \ \| |____ ____) |_| |_   | |   
 |_____|  |_|  |_|  \_\______|_____/|_____|  |_|   
                                                   
                                                   
"""
    print(banner)
    print("https://itresit.es/en/home-en/")
    print()
    print("Author: Peter Gabaldon (https://x.com/PedroGabaldon)\n")

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Check FIXED/NOT FIXED status and optionally compromised state on devices."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-j', '--json-file', help='Path to SHODAN JSON file of devices')
    group.add_argument('-t', '--target', help='Single IP:port')
    group.add_argument('-i', '--ip-file', help='Text file with IP:port per line')
    parser.add_argument('--check', action='store_true',
                        help='If specified, skip the sys_global.conf.gz compromised check')
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    targets = []
    if args.json_file:
        devices = parse_devices(args.json_file)
        for entry in devices:
            ip = entry.get('ip_str') or (int_to_ip(entry['ip']) if 'ip' in entry else None)
            port = entry.get('port')
            if not ip or port is None:
                print(f"Skipping malformed entry: {entry}")
                continue
            targets.append((ip, port))
    elif args.ip_file:
        targets = load_ip_file(args.ip_file)
    else:
        if ':' not in args.target:
            parser.error('Invalid target format, expected IP:port')
        ip, port = args.target.split(':', 1)
        targets.append((ip, port))

    for ip, port in targets:
        # Check /lang/custom/test for FIXED status
        try:
            code = check_path(ip, port, '/lang/custom/test')
            if code == 403:
                print(f"\033[32m{ip}:{port} FIXED\033[0m")
            else:
                print(f"\033[33m{ip}:{port} NOT FIXED (status {code})\033[0m")
        except requests.RequestException as e:
            print(f"{ip}:{port} ERROR on test check: {e}")
            continue

        # Optionally check compromised path
        if not args.check:
            try:
                code2 = check_path(ip, port, '/lang/custom/data/config/sys_global.conf.gz')
                if code2 == 200:
                    print(f"\033[31m{ip}:{port} COMPROMISED\033[0m")
            except requests.RequestException as e:
                print(f"{ip}:{port} ERROR on compromised check: {e}")

if __name__ == '__main__':
    main()
