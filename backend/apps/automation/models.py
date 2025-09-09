from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProxyProfile(TimeStampedModel):
    label = models.CharField(max_length=120)
    proxy_url = models.CharField(max_length=255)  # http://user:pass@host:port
    user_agent = models.CharField(max_length=255, blank=True)
    headers = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)


class BrowserSession(TimeStampedModel):
    profile = models.ForeignKey(ProxyProfile, on_delete=models.SET_NULL, null=True, blank=True)
    state_path = models.CharField(max_length=255, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    ok = models.BooleanField(default=True)

