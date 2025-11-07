from typing import Dict, Any

def apply(event: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any] | None:
    """Treat policy-blocked categories as false positives when no payload body is delivered."""
    matches = event.get("matches", [])
    if not matches:
        return None

    blocked = set([c.lower() for c in cfg.get("blocked_categories", [])])
    for m in matches:
        cat = (m.category or "").lower()
        if cat in blocked:
            return {"rule": "blocked_category", "severity": "low",
                    "label": cfg.get("label", "LIKELY_FALSE_POSITIVE"),
                    "reason": f"Category '{cat}' blocked prior to body delivery."}
    return None
