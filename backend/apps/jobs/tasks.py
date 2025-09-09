from celery import shared_task
from django.contrib.auth import get_user_model
from .models import JobPosting
from .scoring import upsert_score
from django.db import transaction
from .discovery import discover_all
from .models import JobSource


@shared_task
def score_all_jobs_for_user(user_id: int) -> int:
    User = get_user_model()
    user = User.objects.get(id=user_id)
    count = 0
    for job in JobPosting.objects.all().only("id", "description_text"):
        upsert_score(job, user)
        count += 1
    return count


@shared_task
def discover_sources_task(slugs: list[str], concurrency: int = 20) -> dict:
    results = asyncio.run(discover_all(slugs, concurrency=concurrency))
    created = 0
    with transaction.atomic():
        for base_url, key in results:
            JobSource.objects.get_or_create(key=key, base_url=base_url, defaults={"enabled": True, "auth_config": {}})
            created += 1
    return {"created": created, "results": results}
