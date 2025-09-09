from django.db import models
from django.utils import timezone
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    domains = models.JSONField(default=list, blank=True)

    def __str__(self):  # pragma: no cover
        return self.name


class JobSource(TimeStampedModel):
    key = models.CharField(max_length=64, unique=True)  # 'greenhouse', 'lever', 'workday', 'custom'
    base_url = models.URLField(blank=True)
    auth_config = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)


class CrawlJob(TimeStampedModel):
    source = models.ForeignKey(JobSource, on_delete=models.CASCADE)
    query = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=32, default="pending")  # pending/running/success/failed
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    stats = models.JSONField(default=dict, blank=True)


class RawJobPosting(TimeStampedModel):
    source = models.ForeignKey(JobSource, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255)
    url = models.URLField()
    payload = models.JSONField(default=dict)

    class Meta:
        unique_together = ("source", "external_id")


class JobPosting(TimeStampedModel):
    raw = models.ForeignKey(RawJobPosting, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    remote = models.BooleanField(default=False)
    description_text = models.TextField()
    requirements = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    seniority = models.CharField(max_length=64, blank=True)
    employment_type = models.CharField(max_length=64, blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    closing_at = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        indexes = [models.Index(fields=["title", "location"])]


class MatchScore(TimeStampedModel):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    features = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("job", "user")

