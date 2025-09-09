from __future__ import annotations
from typing import Dict, Any
import httpx
from django.conf import settings
from .base import ConnectorBase
from apps.applications.models import Application
from apps.applications.html_submit import submit_with_documents


class LeverConnector(ConnectorBase):
    key = "lever"

    def submit(self, app: Application) -> Dict[str, Any]:
        payload = self.build_payload(app)
        url = (app.job.raw and app.job.raw.url) or None
        dry_run = not getattr(settings, "APPLY_REAL", False)
        if dry_run or not url:
            return {"dry_run": True, "url": url, "payload": payload}
        try:
            files = self.build_files(app)
            result = submit_with_documents(url, payload, files)
            return result | {"url": url}
        except Exception as e:  # pragma: no cover
            return {"error": str(e), "url": url}
