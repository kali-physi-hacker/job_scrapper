from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class WorkdayAdapter(JobAdapterBase):
    key = "workday"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Workday has JSON endpoints under myworkdayjobs.com; but per-tenant. This is a best-effort placeholder.
        base_url = (self.config or {}).get("base_url", "")
        if not base_url or "myworkdayjobs.com" not in base_url:
            return []
        # We will not implement generic fetching to avoid brittle code; leave for targeted setup.
        return []

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

