from rest_framework import viewsets, permissions
from .models import ProxyProfile, BrowserSession
from .serializers import ProxyProfileSerializer, BrowserSessionSerializer


class ProxyProfileViewSet(viewsets.ModelViewSet):
    queryset = ProxyProfile.objects.all()
    serializer_class = ProxyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrowserSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrowserSession.objects.all().order_by("-created_at")
    serializer_class = BrowserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

