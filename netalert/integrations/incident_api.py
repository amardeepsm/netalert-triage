import os
from typing import Dict, Any

def maybe_update_incident(incident_id: str, summary: Dict[str, Any]) -> None:
    """No-op unless INCIDENT_API_URL/TOKEN are set. Safe for public demo."""
    url = os.getenv("INCIDENT_API_URL")
    token = os.getenv("INCIDENT_API_TOKEN")
    if not (url and token):
        return
    # In real use: POST summary as JSON to url with bearer token.
