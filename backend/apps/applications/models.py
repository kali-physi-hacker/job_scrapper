from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.jobs.models import JobPosting


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Application(TimeStampedModel):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.ForeignKey("apps.core.Document", on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.ForeignKey("apps.core.Document", on_delete=models.SET_NULL, null=True, blank=True, related_name="applications_cover_letters")
    status = models.CharField(max_length=40, default="prepared")  # prepared/submitted/interviewed/offer/rejected
    portal = models.CharField(max_length=120, blank=True)
    portal_external_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("job", "user")


class ApplicationAttempt(TimeStampedModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="attempts")
    outcome = models.CharField(max_length=40, default="pending")  # success/failure/pending
    logs = models.TextField(blank=True)
    evidence = models.JSONField(default=dict, blank=True)

