from rest_framework import serializers
from .models import ProxyProfile, BrowserSession


class ProxyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyProfile
        fields = ["id", "label", "proxy_url", "user_agent", "headers", "enabled", "created_at"]


class BrowserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowserSession
        fields = ["id", "state_path", "last_used_at", "ok", "created_at"]

