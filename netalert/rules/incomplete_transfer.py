from typing import Dict, Any

def apply(event: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any] | None:
    """Detect incomplete or aborted downloads that are unlikely to represent an actual threat."""
    matches = event.get("matches", [])
    if not matches:
        return None

    min_ratio = cfg.get("min_completion_ratio", 0.5)
    statuses = set(cfg.get("statuses_considered_incomplete", []))
    for m in matches:
        status = (m.status or "").upper()
        if status in statuses:
            return {"rule": "incomplete_transfer", "severity": "low",
                    "label": cfg.get("label", "LIKELY_FALSE_POSITIVE"),
                    "reason": "Client aborted or reset the stream before completion."}

        sent = (m.bytes_sent or 0)
        size = (m.expected_size or 0)
        if size > 0 and (sent / size) < min_ratio:
            return {"rule": "incomplete_transfer", "severity": "low",
                    "label": cfg.get("label", "LIKELY_FALSE_POSITIVE"),
                    "reason": f"Transfer ratio {sent}/{size} below threshold {min_ratio}."}
    return None
