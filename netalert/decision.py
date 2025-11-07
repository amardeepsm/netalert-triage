from typing import List, Dict, Any
import yaml
from .rules import incomplete_transfer, blocked_category, filetype_anomaly

def score_events(joined: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cfg = yaml.safe_load(open("configs/rules.yml", "r", encoding="utf-8"))
    rules_cfg = cfg.get("rules", {})

    results = []
    for ev in joined:
        hits = []
        total_weight = 0
        label = None

        for mod, key in [
            (incomplete_transfer, "incomplete_transfer"),
            (blocked_category, "blocked_category"),
            (filetype_anomaly, "filetype_anomaly"),
        ]:
            rule_cfg = rules_cfg.get(key, {})
            hit = mod.apply(ev, rule_cfg)
            if hit:
                hits.append(hit)
                total_weight += int(rule_cfg.get("weight", 1))
                label = hit.get("label", label)

        results.append({
            "alert": ev["alert"],
            "matches": ev.get("matches", []),
            "hits": hits,
            "score": total_weight,
            "label": label or "NEEDS_ANALYST"
        })
    return results
