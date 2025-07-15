# Advanced Bug Bounty Automation and Reporting Suite

## Overview
Integrated toolkit for automating bug bounty workflows with AI prioritization and multi-format reporting.

## Features
- Recon: Subdomain enum, port scanning.
- Scanning: SQLi, XSS, etc., with tool integrations.
- Fuzzing: Parameter/API fuzzing.
- AI Prioritization: ML scoring of findings.
- Reporting: HTML/PDF/JSON with CVSS, screenshots.
- Concurrent execution, YAML configs.

## Installation
```bash
git clone https://github.com/yourusername/advanced-bug-bounty-suite.git
cd advanced-bug-bounty-suite
pip install -r requirements.txt
# Install nmap, sqlmap if needed
```

## Usage
- Full: python main.py full --config configs/workflow.yaml
- Report: Generated in reports/ folder.

## Contributing
See CONTRIBUTING.md.

## License
MIT