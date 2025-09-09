from typing import Iterable, Dict, Any


class JobAdapterBase:
    key: str = "base"

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        """Yield raw posting payloads from a source.

        Each item should minimally include: external_id, url, company, title, description, location, posted_at.
        """
        raise NotImplementedError

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Map a raw payload into canonical fields for JobPosting."""
        raise NotImplementedError

