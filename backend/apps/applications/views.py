from rest_framework import viewsets, permissions
from .models import Application, ApplicationAttempt
from .serializers import ApplicationSerializer, ApplicationAttemptSerializer


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by("-created_at")


class ApplicationAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApplicationAttempt.objects.filter(application__user=self.request.user).order_by("-created_at")

