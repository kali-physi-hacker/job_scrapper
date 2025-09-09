from rest_framework import viewsets, permissions
from .models import Company, JobSource, JobPosting, MatchScore
from .serializers import CompanySerializer, JobSourceSerializer, JobPostingSerializer, MatchScoreSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class JobSourceViewSet(viewsets.ModelViewSet):
    queryset = JobSource.objects.all()
    serializer_class = JobSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobPosting.objects.all().order_by("-created_at")
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MatchScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MatchScore.objects.filter(user=self.request.user).order_by("-created_at")

