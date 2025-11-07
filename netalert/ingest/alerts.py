from pydantic import BaseModel, HttpUrl
from typing import List
import json

class Alert(BaseModel):
    id: str
    timestamp: str
    user: str
    src_ip: str
    url: HttpUrl

def load_alerts(path: str) -> List[Alert]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Alert(**a) for a in data]
