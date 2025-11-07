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
