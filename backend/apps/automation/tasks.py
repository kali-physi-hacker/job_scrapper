from celery import shared_task
from tenacity import retry, stop_after_attempt, wait_exponential
from django.utils import timezone
from django.db import transaction

from apps.jobs.models import JobSource, CrawlJob, RawJobPosting, JobPosting, Company
from apps.jobs.adapter_registry import get_adapter
from apps.jobs.utils import extract_basic_skills
from apps.applications.connectors import get_connector
from apps.applications.models import Application, ApplicationAttempt
from django.conf import settings


@shared_task
@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(3))
def crawl_source_task(source_id: int, query: str = "", location: str = "") -> dict:
    source = JobSource.objects.get(id=source_id)
    job = CrawlJob.objects.create(source=source, query=query, location=location, state="running", started_at=timezone.now())
    fetched = 0
    normalized = 0
    adapter = get_adapter(source.key, {"base_url": source.base_url, **(source.auth_config or {})})
    try:
        for payload in adapter.fetch(query=query, location=location) or []:
            fetched += 1
            external_id = str(payload.get("id") or payload.get("external_id") or payload.get("url"))
            if not external_id:
                continue
            raw, _ = RawJobPosting.objects.get_or_create(
                source=source,
                external_id=external_id,
                defaults={"url": payload.get("absolute_url") or payload.get("url") or source.base_url, "payload": payload},
            )
            if not _:
                # update payload if changed
                raw.payload = payload
                raw.url = payload.get("absolute_url") or payload.get("url") or raw.url
                raw.save(update_fields=["payload", "url", "updated_at"])

            norm = adapter.normalize(payload)
            if not norm.get("title"):
                continue
            with transaction.atomic():
                company_name = (norm.get("company") or "").strip() or "Unknown"
                company, _c = Company.objects.get_or_create(name=company_name)
                job_posting, _j = JobPosting.objects.update_or_create(
                    raw=raw,
                    defaults={
                        "company": company,
                        "title": norm.get("title") or "Untitled",
                        "location": norm.get("location") or "",
                        "remote": bool(norm.get("remote", False)),
                        "description_text": norm.get("description_text") or "",
                        "posted_at": norm.get("posted_at"),
                        "tags": norm.get("tags") or [],
                    },
                )
                # naive skill extraction
                job_posting.skills = list(sorted(extract_basic_skills(job_posting.description_text)))
                job_posting.save(update_fields=["skills", "updated_at"])
                normalized += 1

        job.state = "success"
        job.finished_at = timezone.now()
        job.stats = {"fetched": fetched, "normalized": normalized}
        job.save(update_fields=["state", "finished_at", "stats", "updated_at"])
        return {"source_id": source_id, "fetched": fetched, "normalized": normalized}
    except Exception as e:  # pragma: no cover
        job.state = "failed"
        job.finished_at = timezone.now()
        job.stats = {"error": str(e), "fetched": fetched, "normalized": normalized}
        job.save(update_fields=["state", "finished_at", "stats", "updated_at"])
        raise


@shared_task
@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(3))
def apply_to_job_task(application_id: int) -> dict:
    app = Application.objects.select_related("job", "job__raw", "user").get(id=application_id)
    attempt = ApplicationAttempt.objects.create(application=app, outcome="pending", logs="starting")
    source = app.job.raw.source if app.job and app.job.raw else None
    portal_key = (source.key if source else app.portal or "").lower()
    Connector = get_connector(portal_key)
    if not Connector:
        attempt.outcome = "failure"
        attempt.logs = f"No connector for portal '{portal_key}'"
        attempt.evidence = {"portal": portal_key}
        attempt.save(update_fields=["outcome", "logs", "evidence", "updated_at"])
        return {"application_id": application_id, "status": "no-connector"}

    connector = Connector({"real": settings.APPLY_REAL})
    result = connector.submit(app)
    ok = bool(result.get("error") is None)
    attempt.outcome = "success" if ok else "failure"
    attempt.logs = "applied" if ok else f"error: {result.get('error')}"
    attempt.evidence = result
    attempt.save(update_fields=["outcome", "logs", "evidence", "updated_at"])
    if ok:
        app.status = "submitted"
        app.portal = portal_key
        app.save(update_fields=["status", "portal", "updated_at"])
    return {"application_id": application_id, "status": attempt.outcome}
