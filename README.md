# Fortigate Symlink Persistence Method Checker

The following script checks remotely if a Fortigate unit has been fixed vs the persistence method leveraging a symlink in the VPN-SSL used by TA

```
$ python3 -m venv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

# Examples

```
(.venv) $ python3 check_fix.py -j ../Fortigates.Shodan/fortigate.json
(.venv) $ python3 check_fix.py -t IP.IP.IP.IP:10443
```
