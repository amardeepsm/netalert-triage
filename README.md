# NetAlert Triage

An automated incident-triage framework that correlates **security alerts** with **network-gateway download logs**, applies **contextual heuristics**, and flags **likely false positives**. Ships with a full **demo mode** (no secrets), sample data, CI, and docs.

> *Inspired by real-world incident-response automation challenges at Capgemini (public-safe, open-source version).*

## Features
- Correlates alert feed ↔ gateway logs (user/IP/time/URL)
- Heuristic rules (aborted/incomplete download, blocked category, file-type anomalies)
- Scores events: `LIKELY_FALSE_POSITIVE`, `NEEDS_ANALYST`, `LIKELY_MALICIOUS`
- Generates a Markdown triage report (artifact in CI)
- Optional incident system integration (generic REST client, disabled by default)

## Quickstart (demo mode)
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python -m netalert.run --alerts sample_data/sample_alerts.json --logs sample_data/sample_gateway_logs.json --out artifacts/report.md
```
## How It Works
A[🔔 Alert Triggered] --> B[📥 Alert Data Ingested<br>(sample_alerts.json)]
B --> C[🌐 Proxy Log Fetched<br>(sample_gateway_logs.json)]
C --> D[⚖️ Correlation<br>Match alert ↔ log (user, URL)]
D --> E[🧮 Heuristic Rules<br>incomplete_transfer<br>blocked_category<br>filetype_anomaly]
E --> F[🏷️ Label & Score<br>LIKELY_FALSE_POSITIVE or NEEDS_ANALYST]
F --> G[🧾 Markdown Report<br>(artifacts/report.md)]
G --> H[(🧰 Optional Integration<br>ServiceNow / Jira Update)]

## Summary

## Ingests alert feed:
  Reads mock security alerts from sample_alerts.json.
## Loads gateway logs:
  Simulates real network logs from sample_gateway_logs.json.
## Correlates events:
  Matches alerts and logs by user, URL, and timestamp proximity.
## Applies rule-based logic:
    - incomplete_transfer: detects aborted or partial downloads
    - blocked_category: flags URLs blocked by policy
    - filetype_anomaly: surfaces suspicious MIME types
## Generates a triage report:
  Summarizes findings in a clear Markdown format (artifacts/report.md).
## Optional integrations:
  Can safely connect to ServiceNow or Jira (disabled by default).

## Example Output
# NetAlert Triage Report

## Alert INC-1001 — LIKELY_FALSE_POSITIVE
- user: alice
- src_ip: 10.0.0.15
- url: http://downloads.example.com/tool.exe
- score: 3

### Rule hits
- **incomplete_transfer** (low): Client aborted or reset the stream before completion.
- **blocked_category** (low): Category 'malware' blocked prior to body delivery.
- 
Open the generated report at `artifacts/report.md`.

## Production hooks (optional)
- Provide environment variables to enable the incident client and live log adapters (see `docs/production.md`).

## Repo layout
```
netalert-triage/
├─ netalert/
│  ├─ ingest/
│  │  ├─ alerts.py
│  │  └─ gateway.py
│  ├─ rules/
│  │  ├─ incomplete_transfer.py
│  │  ├─ blocked_category.py
│  │  └─ filetype_anomaly.py
│  ├─ correlate.py
│  ├─ decision.py
│  ├─ reporting.py
│  ├─ integrations/
│  │  └─ incident_api.py
│  └─ run.py
├─ configs/
│  └─ rules.yml
├─ sample_data/
│  ├─ sample_alerts.json
│  └─ sample_gateway_logs.json
├─ artifacts/                # report output (gitignored in real use)
├─ docs/
│  ├─ heuristics.md
│  └─ production.md
├─ tests/
│  ├─ test_rules.py
│  └─ test_pipeline.py
├─ .github/workflows/ci.yml
├─ requirements.txt
└─ README.md
```

## Why this matters
Reduces alert fatigue and MTTR by automatically providing **evidence-based triage**. Designed to be extended with real adapters (CloudWatch, Elasticsearch, Splunk) and incident systems (ServiceNow, Jira) without exposing proprietary details.
