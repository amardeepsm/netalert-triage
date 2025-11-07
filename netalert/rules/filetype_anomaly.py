from typing import Dict, Any

def apply(event: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any] | None:
    """Highlight suspicious MIME types for analyst review."""
    matches = event.get("matches", [])
    if not matches:
        return None

    deny = set([t.lower() for t in cfg.get("deny_mime_types", [])])
    warn = set([t.lower() for t in cfg.get("warn_mime_types", [])])

    for m in matches:
        mt = (m.mime_type or "").lower()
        if mt in deny:
            return {"rule": "filetype_anomaly", "severity": "high",
                    "label": cfg.get("label", "NEEDS_ANALYST"),
                    "reason": f"MIME type '{mt}' is deny-listed."}
        if mt in warn:
            return {"rule": "filetype_anomaly", "severity": "medium",
                    "label": cfg.get("label", "NEEDS_ANALYST"),
                    "reason": f"MIME type '{mt}' warrants review."}
    return None
