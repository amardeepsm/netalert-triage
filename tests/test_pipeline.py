from netalert.ingest.alerts import load_alerts
from netalert.ingest.gateway import load_gateway_logs
from netalert.correlate import correlate_events
from netalert.decision import score_events

def test_demo_pipeline():
    alerts = load_alerts("sample_data/sample_alerts.json")
    logs = load_gateway_logs("sample_data/sample_gateway_logs.json")
    joined = correlate_events(alerts, logs)
    results = score_events(joined)
    assert len(results) == 2
    labels = {r["label"] for r in results}
    assert "LIKELY_FALSE_POSITIVE" in labels or "NEEDS_ANALYST" in labels
