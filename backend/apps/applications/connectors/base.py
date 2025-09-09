from __future__ import annotations
from typing import Dict, Any
from apps.applications.models import Application
from django.core.files.storage import default_storage
from django.core.files.base import File


class ConnectorBase:
    key = "base"

    def __init__(self, settings: Dict[str, Any] | None = None):
        self.settings = settings or {}

    def build_payload(self, app: Application) -> Dict[str, Any]:
        user = app.user
        job = app.job
        return {
            "name": getattr(user, "get_full_name", lambda: user.username)() or user.username,
            "email": user.email,
            "job_title": job.title,
            "company": job.company.name if job.company else None,
        }

    def submit(self, app: Application) -> Dict[str, Any]:
        raise NotImplementedError

    def build_files(self, app: Application) -> Dict[str, Any]:
        files: Dict[str, Any] = {}
        # Heuristics for common resume/cover field names
        resume_names = [
            'resume', 'cv', 'file', 'attachment', 'application[resume]', 'candidate[resume]'
        ]
        cover_names = [
            'cover_letter', 'cover-letter', 'application[cover_letter]'
        ]
        if app.resume and app.resume.file:
            path = app.resume.file.path
            with open(path, 'rb') as f:  # type: ignore[arg-type]
                content = f.read()
            for n in resume_names:
                files[n] = (app.resume.file.name.split('/')[-1], content, 'application/octet-stream')
        if app.cover_letter and app.cover_letter.file:
            path = app.cover_letter.file.path
            with open(path, 'rb') as f:  # type: ignore[arg-type]
                content = f.read()
            for n in cover_names:
                files[n] = (app.cover_letter.file.name.split('/')[-1], content, 'application/octet-stream')
        return files
