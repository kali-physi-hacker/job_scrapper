from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class WorkableAdapter(JobAdapterBase):
    key = "workable"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Public endpoint: https://apply.workable.com/api/v3/accounts/{company}/jobs
        company = (self.config or {}).get("company")
        if not company:
            base_url = (self.config or {}).get("base_url", "")
            if "apply.workable.com" in base_url:
                parts = base_url.rstrip("/").split("/")
                company = parts[-1]
        if not company:
            return []
        api = f"https://apply.workable.com/api/v3/accounts/{company}/jobs"
        params = {"limit": 200}
        with httpx.Client(timeout=20) as client:
            resp = client.get(api, params=params)
            if resp.status_code >= 400:
                return []
            data = resp.json()
            for job in data.get("results", []):
                yield job

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        return {
            "external_id": off.get("shortcode") or off.get("id"),
            "url": off.get("application_url") or off.get("url"),
            "company": (off.get("company_name") or off.get("account", {})).get("name") if isinstance(off.get("account"), dict) else None,
            "title": off.get("title"),
            "description_text": off.get("description") or "",
            "location": (off.get("location") or {}).get("city") or "",
            "posted_at": off.get("published_on") or off.get("created_at"),
        }

