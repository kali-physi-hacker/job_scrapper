from typing import Iterable, Dict, Any
import httpx
from .base import JobAdapterBase


class TeamtailorAdapter(JobAdapterBase):
    key = "teamtailor"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # Teamtailor does not expose a stable public API per board w/o API key.
        # As a best-effort placeholder, we return no items (adapter can be extended per target company).
        return []

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

