from __future__ import annotations
from typing import Dict, Tuple
from .models import JobPosting, MatchScore
from apps.core.models import Document
from .utils import tokenize


def score_job_for_user(job: JobPosting, user) -> Tuple[float, Dict]:
    # Naive baseline: token overlap between job description and user's declared keywords
    # Expect user to store keywords in a resume Document.metadata["keywords"] or profile headline.
    user_keywords = set()
    docs = Document.objects.filter(owner=user, kind="resume").order_by("-created_at")
    if docs:
        md = docs.first().metadata or {}
        kws = md.get("keywords") or []
        user_keywords |= {str(k).lower() for k in kws}
    if not user_keywords:
        # fall back to job skills vs job tokens (weak)
        user_keywords = set(job.skills or [])

    job_tokens = set(tokenize(job.description_text)) | {t.lower() for t in (job.skills or [])}
    overlap = user_keywords & job_tokens
    if not job_tokens:
        return 0.0, {"overlap": []}

    score = (len(overlap) / max(1, len(user_keywords))) * 0.7 + (len(overlap) / len(job_tokens)) * 0.3
    return float(round(score, 4)), {"overlap": sorted(list(overlap)), "keywords": sorted(list(user_keywords))}


def upsert_score(job: JobPosting, user) -> MatchScore:
    s, feats = score_job_for_user(job, user)
    ms, _ = MatchScore.objects.update_or_create(job=job, user=user, defaults={"score": s, "features": feats})
    return ms

