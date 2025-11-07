from .ingest.alerts import load_alerts
from .ingest.gateway import load_gateway_logs
from .correlate import correlate_events
from .decision import score_events
from .reporting import write_report
import argparse, os

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--alerts", required=True)
    p.add_argument("--logs", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    alerts = load_alerts(args.alerts)
    gateway = load_gateway_logs(args.logs)
    joined = correlate_events(alerts, gateway)
    decisions = score_events(joined)
    write_report(decisions, args.out)

if __name__ == "__main__":
    main()
