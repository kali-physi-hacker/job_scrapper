from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class LeverAdapter(JobAdapterBase):
    key = "lever"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Expects base_url like https://jobs.lever.co/<company>
        base_url = (self.config or {}).get("base_url")
        if not base_url:
            return []
        api = base_url.rstrip("/") + "?mode=json"
        with httpx.Client(timeout=15) as client:
            resp = client.get(api)
            resp.raise_for_status()
            data = resp.json()
            for job in data:
                yield job

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        return {
            "external_id": off.get("id"),
            "url": off.get("hostedUrl") or off.get("applyUrl"),
            "company": off.get("categories", {}).get("team"),
            "title": off.get("text") or off.get("title"),
            "description_text": off.get("descriptionPlain") or off.get("description") or "",
            "location": (off.get("categories") or {}).get("location"),
            "posted_at": off.get("createdAt") or off.get("createdAtISO"),
        }

