from typing import List, Dict, Any

def write_report(items: List[Dict[str, Any]], path: str) -> None:
    lines = ["# NetAlert Triage Report", ""]
    for it in items:
        a = it["alert"]
        label = it["label"]
        lines.append(f"## Alert {a.id} — {label}")
        lines.append(f"- user: {a.user}")
        lines.append(f"- src_ip: {a.src_ip}")
        lines.append(f"- url: {a.url}")
        lines.append(f"- score: {it['score']}")
        if it["hits"]:
            lines.append("### Rule hits")
            for h in it["hits"]:
                lines.append(f"- **{h['rule']}** ({h['severity']}): {h['reason']}")
        else:
            lines.append("_No rule hits_")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
