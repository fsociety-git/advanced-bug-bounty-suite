import argparse
import concurrent.futures
import yaml
from modules.recon import perform_recon
from modules.scanner import perform_scan
from modules.fuzzer import perform_fuzz
from modules.ai_prioritizer import prioritize_findings, train_model
from modules.agent import run_agent, tools
from utils.reporter import generate_report

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Advanced Bug Bounty Suite")
    subparsers = parser.add_subparsers(dest="command")

    full_parser = subparsers.add_parser("full", help="Run full workflow")
    full_parser.add_argument("--config", default="configs/workflow.yaml")
    full_parser.add_argument("--threads", default=5, type=int)
    full_parser.add_argument("--report-format", default="json", help="html,pdf,json")

    recon_parser = subparsers.add_parser("recon", help="Recon only")
    recon_parser.add_argument("--target", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan only")
    scan_parser.add_argument("--url", required=True)
    scan_parser.add_argument("--type", default="all")

    fuzz_parser = subparsers.add_parser("fuzz", help="Fuzz only")
    fuzz_parser.add_argument("--endpoint", required=True)
    fuzz_parser.add_argument("--payloads", default="payloads/fuzz.txt")

    pri_parser = subparsers.add_parser("prioritize", help="Prioritize findings")
    pri_parser.add_argument("--findings", required=True)

    train_ai_parser = subparsers.add_parser("train_ai", help="Train AI prioritizer")
    train_ai_parser.add_argument("--dataset", default="data/cve_dataset.csv")

    agent_parser = subparsers.add_parser("agent", help="Run CAI agent")
    agent_parser.add_argument("--query", required=True, help="Agent task query")

    args = parser.parse_args()

    findings = []
    if args.command == "full":
        config = load_config(args.config)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            recon_future = executor.submit(perform_recon, config['target'])
            scan_future = executor.submit(perform_scan, config['url'], "all")
            fuzz_future = executor.submit(perform_fuzz, config['endpoint'], config['payloads'])
            for future in concurrent.futures.as_completed([recon_future, scan_future, fuzz_future]):
                findings.extend(future.result())
        prioritized = prioritize_findings(findings)
        formats = args.report_format.split(',')
        generate_report(prioritized, formats)
    elif args.command == "recon":
        findings = perform_recon(args.target)
    elif args.command == "scan":
        findings = perform_scan(args.url, args.type)
    elif args.command == "fuzz":
        findings = perform_fuzz(args.endpoint, args.payloads)
    elif args.command == "prioritize":
        findings = prioritize_findings(args.findings)  # Load from file if needed
    elif args.command == "train_ai":
        model = train_model(args.dataset)
        print("AI model trained and saved.")
    elif args.command == "agent":
        result = run_agent(args.query, tools)
        print(result)
    print("Operation complete.")

if __name__ == "__main__":
    main()