from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class AshbyAdapter(JobAdapterBase):
    key = "ashby"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Public JSON is available behind jobs.ashbyhq.com board via JSON endpoints
        base_url = (self.config or {}).get("base_url", "")
        if not base_url:
            return []
        # best-effort: get HTML and parse embedded JSON? keeping simple: try API path known for public boards
        # Many boards expose /api/non-user-graphql which needs query; skip to avoid complexity here.
        return []

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

