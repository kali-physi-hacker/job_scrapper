from __future__ import annotations
from typing import Dict, Any
from urllib.parse import urlparse


def detect_platform_and_config(url: str) -> Dict[str, Any]:
    u = url.strip()
    host = urlparse(u).netloc.lower()
    path = urlparse(u).path.rstrip('/')

    # Greenhouse
    if 'greenhouse.io' in host:
        return {"key": "greenhouse", "base_url": u}

    # Lever
    if 'jobs.lever.co' in host:
        return {"key": "lever", "base_url": u}

    # SmartRecruiters
    if 'smartrecruiters.com' in host:
        # try to infer company slug
        parts = path.split('/')
        company = parts[-1] if parts else None
        return {"key": "smartrecruiters", "base_url": u, "auth_config": {"company": company}}

    # Workable
    if 'apply.workable.com' in host or host.endswith('.workable.com'):
        parts = path.split('/')
        company = parts[-1] if parts else host.split('.')[0]
        return {"key": "workable", "base_url": u, "auth_config": {"company": company}}

    # Recruitee
    if host.endswith('.recruitee.com'):
        company = host.split('.')[0]
        return {"key": "recruitee", "base_url": u, "auth_config": {"company": company}}

    # Ashby
    if 'ashbyhq.com' in host:
        return {"key": "ashby", "base_url": u}

    # Workday
    if 'myworkdayjobs.com' in host:
        return {"key": "workday", "base_url": u}

    # BreezyHR
    if host.endswith('.breezy.hr'):
        return {"key": "breezy", "base_url": u}

    # Teamtailor
    if host.endswith('.teamtailor.com') or host.startswith('careers.') and 'teamtailor.com' in host:
        return {"key": "teamtailor", "base_url": u}

    # iCIMS
    if 'icims.com' in host:
        return {"key": "icims", "base_url": u}

    # Default to greenhouse
    return {"key": "greenhouse", "base_url": u}
