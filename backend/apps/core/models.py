from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    headline = models.CharField(max_length=280, blank=True)
    location = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.full_name or self.user.get_username()


class CredentialVault(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    portal = models.CharField(max_length=120)  # e.g., 'greenhouse', 'lever', 'workday', 'custom'
    username = models.CharField(max_length=255)
    secret_enc = models.BinaryField()  # encrypted secret material
    note = models.CharField(max_length=280, blank=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "portal"])]


class Document(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.CharField(max_length=50)  # 'resume', 'cover_letter', 'portfolio'
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    ats_score = models.FloatField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "kind"])]

