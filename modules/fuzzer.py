import requests
import concurrent.futures

def fuzz_single(endpoint, payload):
    response = requests.get(endpoint, params={"fuzz": payload})
    if response.status_code >= 500 or "error" in response.text.lower():
        return {"type": "fuzz_anomaly", "payload": payload, "status": response.status_code}

def perform_fuzz(endpoint, payloads_file):
    with open(payloads_file, 'r') as f:
        payloads = [p.strip() for p in f.readlines()]
    findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fuzz_single, endpoint, p) for p in payloads]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                findings.append(res)
    return findings
