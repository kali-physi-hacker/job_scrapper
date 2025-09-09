from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class BreezyAdapter(JobAdapterBase):
    key = "breezy"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        base = (self.config or {}).get("base_url")
        if not base:
            return []
        url = base.rstrip("/") + "/json"
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            r = client.get(url)
            if r.status_code >= 400:
                return []
            data = r.json()
            if isinstance(data, list):
                for item in data:
                    yield item

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        return {
            "external_id": off.get("id") or off.get("position_id"),
            "url": off.get("url") or off.get("absolute_url"),
            "company": off.get("company") or None,
            "title": off.get("title") or off.get("name"),
            "description_text": off.get("description") or off.get("description_text") or "",
            "location": off.get("location") or "",
            "posted_at": off.get("created_date") or off.get("published_date"),
        }

