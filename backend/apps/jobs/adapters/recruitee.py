from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class RecruiteeAdapter(JobAdapterBase):
    key = "recruitee"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        base_url = (self.config or {}).get("base_url", "")
        company = (self.config or {}).get("company")
        if not company:
            # https://<company>.recruitee.com
            if base_url:
                host = base_url.split("//")[-1].split("/")[0]
                if host.endswith(".recruitee.com"):
                    company = host.split(".")[0]
        if not company:
            return []
        api = f"https://{company}.recruitee.com/api/offers/"
        with httpx.Client(timeout=20) as client:
            resp = client.get(api)
            if resp.status_code >= 400:
                return []
            data = resp.json()
            for job in data.get("offers", []):
                yield job

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        return {
            "external_id": off.get("id"),
            "url": off.get("careers_url") or off.get("url"),
            "company": (off.get("company") or {}).get("name"),
            "title": off.get("title"),
            "description_text": off.get("description") or off.get("description_text") or "",
            "location": (off.get("location") or {}).get("city") or "",
            "posted_at": off.get("created_at") or off.get("published_at"),
        }

