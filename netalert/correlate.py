from typing import List, Dict
from .ingest.alerts import Alert
from .ingest.gateway import GatewayLog

def correlate_events(alerts: List[Alert], logs: List[GatewayLog]) -> List[Dict]:
    results = []
    # Naive correlation: match on user + url; in real usage also consider time windows & IP
    index = {}
    for g in logs:
        index.setdefault((g.user, str(g.url)), []).append(g)

    for a in alerts:
        matches = index.get((a.user, str(a.url)), [])
        if not matches:
            results.append({"alert": a, "matches": [], "notes": ["no_log_match"]})
        else:
            results.append({"alert": a, "matches": matches, "notes": []})
    return results
