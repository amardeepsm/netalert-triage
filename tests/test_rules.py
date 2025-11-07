from netalert.rules.incomplete_transfer import apply as inc
from netalert.rules.blocked_category import apply as block
from netalert.rules.filetype_anomaly import apply as ftype

def test_incomplete_transfer_ratio():
    ev = {"matches": [type("X", (), {"status": "HIT", "bytes_sent": 100, "expected_size": 1000})()]}
    cfg = {"min_completion_ratio": 0.5, "label": "LIKELY_FALSE_POSITIVE"}
    hit = inc(ev, cfg)
    assert hit and hit["rule"] == "incomplete_transfer"

def test_blocked_category():
    ev = {"matches": [type("X", (), {"category": "malware"})()]}
    cfg = {"blocked_categories": ["malware"], "label": "LIKELY_FALSE_POSITIVE"}
    hit = block(ev, cfg)
    assert hit and hit["rule"] == "blocked_category"

def test_filetype_anomaly_warn():
    ev = {"matches": [type("X", (), {"mime_type": "application/octet-stream"})()]}
    cfg = {"warn_mime_types": ["application/octet-stream"], "label": "NEEDS_ANALYST"}
    hit = ftype(ev, cfg)
    assert hit and hit["label"] == "NEEDS_ANALYST"
