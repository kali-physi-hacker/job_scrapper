from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company, JobSource, JobPosting, MatchScore
from .serializers import CompanySerializer, JobSourceSerializer, JobPostingSerializer, MatchScoreSerializer
from apps.automation.tasks import crawl_source_task
from .tasks import score_all_jobs_for_user
from .scoring import upsert_score
from .detect import detect_platform_and_config
from .tasks import discover_sources_task


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class JobSourceViewSet(viewsets.ModelViewSet):
    queryset = JobSource.objects.all()
    serializer_class = JobSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def crawl(self, request, pk=None):
        source = self.get_object()
        query = request.data.get("query", "")
        location = request.data.get("location", "")
        task = crawl_source_task.delay(source.id, query=query, location=location)
        return Response({"status": "queued", "task_id": task.id})

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request):
        # Accepts { urls: string[] } or { sources: {url, key?}[] }
        urls = request.data.get("urls") or []
        sources_in = request.data.get("sources") or []
        created = []
        for item in urls:
            conf = detect_platform_and_config(item)
            src = JobSource.objects.create(
                key=conf["key"],
                base_url=conf["base_url"],
                auth_config=conf.get("auth_config", {}),
                enabled=True,
            )
            created.append(src.id)
        for s in sources_in:
            if isinstance(s, dict) and s.get("base_url"):
                key = s.get("key") or detect_platform_and_config(s["base_url"]).get("key", "greenhouse")
                src = JobSource.objects.create(
                    key=key,
                    base_url=s["base_url"],
                    auth_config=s.get("auth_config") or {},
                    enabled=True,
                )
                created.append(src.id)
        return Response({"created": created, "count": len(created)})

    @action(detail=False, methods=["post"], url_path="discover")
    def discover(self, request):
        slugs = request.data.get("slugs") or []
        concurrency = int(request.data.get("concurrency", 20))
        if not isinstance(slugs, list) or not slugs:
            return Response({"detail": "slugs must be a non-empty list"}, status=400)
        task = discover_sources_task.delay(slugs, concurrency)
        return Response({"status": "queued", "task_id": task.id, "count": len(slugs)})


class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobPosting.objects.all().order_by("-created_at")
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="score-all")
    def score_all(self, request):
        task = score_all_jobs_for_user.delay(request.user.id)
        return Response({"status": "queued", "task_id": task.id})

    @action(detail=True, methods=["get"], url_path="my-score")
    def my_score(self, request, pk=None):
        job = self.get_object()
        ms = upsert_score(job, request.user)
        return Response({"score": ms.score, "features": ms.features})

    @action(detail=False, methods=["get"], url_path="top-matches")
    def top_matches(self, request):
        # optional filters
        title_q = request.query_params.get("q", "").lower()
        location_q = request.query_params.get("location", "").lower()
        remote = request.query_params.get("remote")
        min_score = float(request.query_params.get("min_score", 0.0))

        jobs = self.get_queryset()
        if title_q:
            jobs = jobs.filter(title__icontains=title_q)
        if location_q:
            jobs = jobs.filter(location__icontains=location_q)
        if remote in ("true", "false"):
            jobs = jobs.filter(remote=(remote == "true"))

        # ensure scores exist
        data = []
        for j in jobs[:200]:  # cap for performance
            ms = upsert_score(j, request.user)
            if ms.score >= min_score:
                data.append((ms.score, j))
        data.sort(key=lambda t: t[0], reverse=True)
        top = [self.get_serializer(j).data | {"_score": s} for s, j in data[:50]]
        return Response(top)


class MatchScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MatchScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MatchScore.objects.filter(user=self.request.user).order_by("-created_at")
