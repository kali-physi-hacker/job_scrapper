from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class GreenhouseAdapter(JobAdapterBase):
    key = "greenhouse"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Minimal example: expects base_url pointing to a Greenhouse board
        base_url = (self.config or {}).get("base_url")
        if not base_url:
            return []
        api = base_url.rstrip("/") + "/api/public/jobs"
        with httpx.Client(timeout=15) as client:
            resp = client.get(api)
            resp.raise_for_status()
            data = resp.json()
            for job in data.get("jobs", []):
                yield job

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        return {
            "external_id": off.get("id"),
            "url": off.get("absolute_url"),
            "company": off.get("company", {}).get("name") if isinstance(off.get("company"), dict) else None,
            "title": off.get("title"),
            "description_text": off.get("content"),
            "location": (off.get("location") or {}).get("name") if isinstance(off.get("location"), dict) else None,
            "posted_at": off.get("updated_at") or off.get("created_at"),
        }

