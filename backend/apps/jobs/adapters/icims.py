from typing import Iterable, Dict, Any
from .base import JobAdapterBase


class ICIMSAdapter(JobAdapterBase):
    key = "icims"

    def fetch(self, query: str = "", location: str = "") -> Iterable[Dict[str, Any]]:
        # iCIMS varies per tenant; add targeted implementations as needed.
        return []

    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

