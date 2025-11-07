# NetAlert Triage

[![CI](https://github.com/amardeepsm/netalert-triage/actions/workflows/ci.yml/badge.svg)](https://github.com/amardeepsm/netalert-triage/actions/workflows/ci.yml)

An automated **incident triage framework** that correlates **security alerts** with **network-gateway logs**, applies contextual **heuristics**, and flags **likely false positives** before they wake an on-call engineer.

> *Inspired by real-world incident-response automation challenges at **Capgemini** (public-safe, open-source adaptation).*

---

## ⚙️ Features

* Correlates alerts ↔ gateway logs by user, IP, timestamp, and URL
* Applies rule-based heuristics for incomplete downloads, blocked categories, and suspicious file types
* Scores events as `LIKELY_FALSE_POSITIVE`, `NEEDS_ANALYST_REVIEW`, or `LIKELY_MALICIOUS`
* Generates an evidence-based Markdown triage report (`artifacts/report.md`)
* Includes optional ServiceNow / Jira hooks (disabled by default)
* Fully automated CI/CD pipeline via GitHub Actions

---

## 🚀 Quickstart (Demo Mode)

```bash
# 1. Create virtual environment
python -m venv .venv && source .venv/Scripts/activate  # (PowerShell: .venv\Scripts\Activate.ps1)

# 2. Install dependencies
pip install -r requirements.txt
pip install -e .
pip install pytest

# 3. Run tests
pytest -q

# 4. Generate a demo triage report
mkdir -p artifacts
python -m netalert.run --alerts sample_data/sample_alerts.json --logs sample_data/sample_gateway_logs.json --out artifacts/report.md
```

Then open `artifacts/report.md` to view the sample output.

---

## 🧠 How It Works

**NetAlert Triage** automates the manual process of investigating suspicious download alerts — the kind that often turn out to be false positives during out-of-hours shifts.

It operates in four simple stages:

### 1️⃣ Collect

Reads simulated alert data (`sample_alerts.json`) and gateway logs (`sample_gateway_logs.json`) — representing real signals from monitoring tools.

### 2️⃣ Correlate

Automatically matches alerts and log entries based on user, URL, and timestamp proximity to form unified investigation events.

### 3️⃣ Analyze

Applies lightweight heuristic rules from `netalert/rules/`:

* **incomplete_transfer** → download aborted or never finished
* **blocked_category** → URL blocked by policy before payload
* **filetype_anomaly** → executable or unusual file type

Each rule contributes to a score and a confidence label such as `LIKELY_FALSE_POSITIVE`.

### 4️⃣ Report

Produces a clear Markdown triage summary showing matched alerts, rule hits, and reasoning.
In production, this could feed into systems like **ServiceNow**, **Jira**, or **Slack**.

---

## 🧾 Example Output

```markdown
# NetAlert Triage Report

## Alert INC-1001 — LIKELY_FALSE_POSITIVE
- user: alice
- url: http://downloads.example.com/tool.exe
- score: 3

### Rule hits
- incomplete_transfer → client aborted before completion
- blocked_category → URL already blocked by policy
```

---

## 📁 Repository Structure

```
netalert-triage/
├─ netalert/                 # Core ingestion, correlation, and rule logic
│  ├─ ingest/
│  ├─ rules/
│  ├─ integrations/
│  └─ run.py
├─ sample_data/              # Demo alerts and gateway logs
├─ artifacts/                # Output folder (ignored in real use)
├─ tests/                    # Unit tests (pytest)
├─ docs/                     # Reference docs
├─ .github/workflows/ci.yml  # CI pipeline
├─ requirements.txt
└─ pyproject.toml
```

---

## 💡 Why This Matters

Modern platform and security engineers face **alert fatigue** and rising on-call overhead.
NetAlert Triage demonstrates how simple, open-source automation can reduce noise and improve response time by turning raw logs into contextual insights.

It’s built for clarity, modularity, and safe public demonstration — a reproducible example of how DevOps automation translates real operational pain into elegant, testable code.

---
