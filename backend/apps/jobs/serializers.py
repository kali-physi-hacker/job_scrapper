from rest_framework import serializers
from .models import Company, JobSource, JobPosting, MatchScore


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "website", "domains"]


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = ["id", "key", "base_url", "enabled", "auth_config"]


class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "location",
            "remote",
            "description_text",
            "requirements",
            "skills",
            "seniority",
            "employment_type",
            "posted_at",
            "closing_at",
            "tags",
            "company",
        ]


class MatchScoreSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)

    class Meta:
        model = MatchScore
        fields = ["id", "score", "features", "created_at", "job"]

