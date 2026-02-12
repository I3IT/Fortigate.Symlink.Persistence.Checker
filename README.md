# Fortigate Symlink Persistence Method Checker

# Writeup

The following blog posts are available with the information of the research.

- [https://pgj11.com/posts/FortiGate-Symlink-Attack/](https://pgj11.com/posts/FortiGate-Symlink-Attack/)
- [https://labs.itresit.es/2026/02/11/fortigate-symlink-persistence-method-patch-bypass-cve-2025-68686/](https://labs.itresit.es/2026/02/11/fortigate-symlink-persistence-method-patch-bypass-cve-2025-68686/)

# Description

The following script checks remotely if a Fortigate unit has been fixed vs the persistence method leveraging a symlink in the VPN-SSL used by TA. It also detects if it is compromised unless using only check option (--check).

```
$ python3 -m venv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

# Usage

```
$ python3 check_fix.py -h

  _____ _______ _____  ______  _____ _____ _______ 
 |_   _|__   __|  __ \|  ____|/ ____|_   _|__   __|
   | |    | |  | |__) | |__  | (___   | |    | |   
   | |    | |  |  _  /|  __|  \___ \  | |    | |   
  _| |_   | |  | | \ \| |____ ____) |_| |_   | |   
 |_____|  |_|  |_|  \_\______|_____/|_____|  |_|   
                                                   
                                                   

https://itresit.es/en/home-en/

Author: Peter Gabaldon (https://x.com/PedroGabaldon)

usage: check_fix.py [-h] (-j JSON_FILE | -t TARGET | -i IP_FILE) [--check] [--try-bypass]

Check FIXED/NOT FIXED status and optionally compromised state on devices.

options:
  -h, --help            show this help message and exit
  -j, --json-file JSON_FILE
                        Path to SHODAN JSON file of devices
  -t, --target TARGET   Single IP:port
  -i, --ip-file IP_FILE
                        Text file with IP:port per line
  --check               If specified, run sys_global.conf.gz compromised check
  --try-bypass          If specified, try bypassing the patch using double slash technique (CVE-2025-68686 - FG-IR-25-934)
```

# Examples

```
(.venv) $ python3 check_fix.py -j ../Fortigates.Shodan/fortigate.json
(.venv) $ python3 check_fix.py -t IP.IP.IP.IP:10443
```

![Sample Execution](screenshot.png)
