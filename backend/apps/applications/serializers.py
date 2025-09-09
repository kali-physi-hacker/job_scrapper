from rest_framework import serializers
from .models import Application, ApplicationAttempt
from apps.jobs.serializers import JobPostingSerializer
from apps.core.serializers import DocumentSerializer


class ApplicationAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAttempt
        fields = ["id", "outcome", "logs", "evidence", "created_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)
    resume = DocumentSerializer(read_only=True)
    cover_letter = DocumentSerializer(read_only=True)
    attempts = ApplicationAttemptSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "status",
            "portal",
            "portal_external_id",
            "metadata",
            "created_at",
            "job",
            "resume",
            "cover_letter",
            "attempts",
        ]

