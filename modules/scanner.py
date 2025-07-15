import requests
import subprocess

def perform_scan(url, scan_type):
    findings = []
    if scan_type in ["sqli", "all"]:
        # SQLMap integration
        try:
            output = subprocess.check_output(["sqlmap", "-u", url, "--batch", "--risk=3"]).decode()
            if "vulnerable" in output:
                findings.append({"type": "sqli", "url": url, "cvss": 9.8})
        except:
            pass
    if scan_type in ["xss", "all"]:
        payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
        for p in payloads:
            response = requests.get(url, params={"q": p})
            if p in response.text:
                findings.append({"type": "xss", "url": url, "payload": p, "cvss": 6.1})
    return findings
