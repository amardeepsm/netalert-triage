# NetAlert Triage

[![CI](https://github.com/amardeepsm/netalert-triage/actions/workflows/ci.yml/badge.svg)](https://github.com/amardeepsm/netalert-triage/actions/workflows/ci.yml)

An automated **incident triage framework** that correlates **security alerts** with **network-gateway logs**, applies contextual **heuristics**, and flags **likely false positives** before they wake an on-call engineer.

> *Inspired by real-world incident-response automation challenges at **Capgemini** (public-safe, open-source adaptation).*

---
## ⚙️ Prerequisites & Dependencies

Before running NetAlert Triage, ensure you have the following installed on your system:

## 🧰 System Requirements
| Component              | Version        | Description                                      |
| ---------------------- | -------------- | ------------------------------------------------ |
| **Python**             | 3.11 or higher | Required for running the project and tests       |
| **pip**                | Latest         | Python package manager for dependencies          |
| **Git**                | Latest         | For cloning the repository and version control   |
| **VS Code / Terminal** | Optional       | Recommended for development and running commands |

## 🔒 Optional Tools
| Tool                                  | Purpose                                             | Required |
| ------------------------------------- | --------------------------------------------------- | -------- |
| **Make**                              | Runs setup/test/report shortcuts                    | Optional |
| **ServiceNow / Jira API credentials** | For live incident integration (disabled by default) | Optional |
| **GitHub Actions**                    | CI/CD automation (already configured)               | Optional |

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
## 🧩 System Flow Diagram
flowchart LR
    A[🔔 Alerts Feed<br/>sample_alerts.json] -->|ingest.alerts| B[📥 Ingest Module]
    B --> C[🌐 Gateway Logs<br/>sample_gateway_logs.json]
    C -->|ingest.gateway| D[🔗 Correlate<br/>alerts ↔ logs]
    D --> E[🧮 Apply Rules<br/>netalert/rules/]
    E --> F[⚖️ Decision Engine<br/>netalert/decision.py]
    F --> G[🪶 Report Generator<br/>reporting.py]
    G --> H[🧾 Markdown Report<br/>artifacts/report.md]

    subgraph Rules
      R1[incomplete_transfer.py]
      R2[blocked_category.py]
      R3[filetype_anomaly.py]
    end
    E --> R1
    E --> R2
    E --> R3

    subgraph Optional Integrations
      I1[Jira / ServiceNow<br/>incident_api.py]
    end
    F --> I1

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
├─ netalert/                         # Core application package
│  ├─ ingest/                        # Data ingestion modules
│  │  ├─ alerts.py                   # Parses and validates alert feeds (JSON input)
│  │  └─ gateway.py                  # Processes simulated network gateway logs
│  ├─ rules/                         # Heuristic rule definitions for triage logic
│  │  ├─ incomplete_transfer.py      # Detects aborted or partial downloads
│  │  ├─ blocked_category.py         # Flags URLs blocked by proxy/security policy
│  │  └─ filetype_anomaly.py         # Identifies suspicious or executable file types
│  ├─ integrations/                  # Optional system integrations
│  │  └─ incident_api.py             # Stub for ServiceNow / Jira REST client integration
│  ├─ correlate.py                   # Matches alerts ↔ logs by user/IP/timestamp
│  ├─ decision.py                    # Scoring engine combining rule hits into final verdict
│  ├─ reporting.py                   # Generates Markdown triage report output
│  └─ run.py                         # CLI entrypoint — orchestrates the full triage flow
│
├─ sample_data/                      # Mock datasets for local demo mode
│  ├─ sample_alerts.json             # Simulated alert feed (e.g., malware detections)
│  └─ sample_gateway_logs.json       # Simulated proxy/gateway logs for correlation
│
├─ artifacts/                        # Output folder (contains generated report.md)
│                                    # Ignored in version control during real use
│
├─ tests/                            # Unit tests for validation and CI pipeline
│  ├─ test_rules.py                  # Tests heuristic rule behavior and scoring logic
│  └─ test_pipeline.py               # Verifies end-to-end triage pipeline flow
│
├─ docs/                             # Developer and reference documentation
│  ├─ heuristics.md                  # Explains the rule design and scoring strategy
│  └─ production.md                  # Outlines integration options for real systems
│
├─ .github/workflows/ci.yml          # GitHub Actions CI/CD workflow (setup, test, report)
│
├─ requirements.txt                  # Python dependencies for setup and testing
├─ pyproject.toml                    # Package metadata and build configuration
├─ Makefile                          # Optional automation for setup/test/report tasks
└─ README.md                         # Full documentation and usage instructions
```
---

## 🧰 Optional: Using the Makefile

A lightweight Makefile is included for convenience, it supports both Windows and UNIX systems and it will detect your OS automatically. Makefile automates common tasks like environment setup, testing, and generating the demo report.

This is completely optional; all commands can be run manually using standard Python tooling (as shown in the Quickstart section).

You’ll only need make if you want one-line shortcuts such as:

```bash
make setup     # create virtual environment + install dependencies
make test      # run unit tests
make report    # generate the sample triage report
make clean     # remove cached files and artifacts
```

The Makefile is simply a developer-experience tool, it isn’t required to run or evaluate this project.
It reflects how automation tasks could be structured in a real CI/CD environment.

---

## 💡 Why This Matters

Modern platform and security engineers face **alert fatigue** and rising on-call overhead.
NetAlert Triage demonstrates how simple, open-source automation can reduce noise and improve response time by turning raw logs into contextual insights.

It’s built for clarity, modularity, and safe public demonstration — a reproducible example of how DevOps automation translates real operational pain into elegant, testable code.

---
