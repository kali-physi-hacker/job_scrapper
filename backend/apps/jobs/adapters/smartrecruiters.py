from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class SmartRecruitersAdapter(JobAdapterBase):
    key = "smartrecruiters"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # config requires company slug, e.g., careers.smartrecruiters.com/<company>
        company = (self.config or {}).get("company")
        if not company:
            # try to infer from base_url
            base_url = (self.config or {}).get("base_url", "")
            if "smartrecruiters.com" in base_url:
                parts = base_url.rstrip("/").split("/")
                if parts:
                    company = parts[-1]
        if not company:
            return []
        api = f"https://api.smartrecruiters.com/v1/companies/{company}/postings"
        params = {"limit": 200, "offset": 0, "active": True}
        with httpx.Client(timeout=20) as client:
            resp = client.get(api, params=params)
            if resp.status_code >= 400:
                return []
            data = resp.json()
            for job in data.get("content", []):
                yield job

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        off = payload
        company = off.get("company", {}).get("name") if isinstance(off.get("company"), dict) else None
        location = None
        loc = off.get("location")
        if isinstance(loc, dict):
            location = ", ".join(filter(None, [loc.get("city"), loc.get("region"), loc.get("country")]))
        return {
            "external_id": off.get("id"),
            "url": off.get("ref") and off["ref"].get("jobAdPublicUrl"),
            "company": company,
            "title": off.get("name"),
            "description_text": (off.get("jobAd") or {}).get("sections", {}).get("jobDescription", {}).get("text", ""),
            "location": location or "",
            "posted_at": off.get("releasedDate") or off.get("createdOn"),
        }

