from celery import shared_task
from tenacity import retry, stop_after_attempt, wait_exponential


@shared_task
@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(3))
def crawl_source_task(source_id: int, query: str = "", location: str = "") -> dict:
    # Placeholder for crawling logic (e.g., httpx/Playwright)
    # Return stats for observability.
    return {"source_id": source_id, "fetched": 0, "normalized": 0}


@shared_task
@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(3))
def apply_to_job_task(application_id: int) -> dict:
    # Placeholder for auto‑apply logic.
    return {"application_id": application_id, "status": "queued"}

