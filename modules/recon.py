import nmap
import subprocess

def perform_recon(target):
    findings = []
    # Subdomain enum (using sublist3r or similar; placeholder subprocess)
    try:
        subs = subprocess.check_output(["sublist3r", "-d", target]).decode().splitlines()
        findings.extend([{"type": "subdomain", "value": s} for s in subs])
    except:
        pass
    # Port scan
    scanner = nmap.PortScanner()
    scanner.scan(target, '1-1024')
    for host in scanner.all_hosts():
        for port in scanner[host]['tcp']:
            findings.append({"type": "open_port", "host": host, "port": port})
    return findings
