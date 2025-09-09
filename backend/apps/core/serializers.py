from rest_framework import serializers
from .models import Profile, Document


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "full_name", "headline", "location", "website", "created_at", "updated_at"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "kind", "title", "file", "ats_score", "metadata", "created_at"]

