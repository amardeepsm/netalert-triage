from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
import json

class GatewayLog(BaseModel):
    timestamp: str
    user: str
    src_ip: str
    url: HttpUrl
    status: str
    bytes_sent: Optional[int] = Field(default=None, ge=0)
    expected_size: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None
    mime_type: Optional[str] = None
    http_status: Optional[int] = None

def load_gateway_logs(path: str) -> List[GatewayLog]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [GatewayLog(**a) for a in data]
