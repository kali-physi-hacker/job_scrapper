from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application, ApplicationAttempt
from .serializers import ApplicationSerializer, ApplicationAttemptSerializer
from apps.jobs.models import JobPosting
from apps.automation.tasks import apply_to_job_task
from .services import tailor_cover_letter, attach_documents_to_application
from .services import tailor_resume


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=False, methods=["post"], url_path="prepare")
    def prepare(self, request):
        job_id = request.data.get("job_id")
        resume_id = request.data.get("resume_id")
        cover_id = request.data.get("cover_id")
        if not job_id:
            return Response({"detail": "job_id required"}, status=status.HTTP_400_BAD_REQUEST)
        job = JobPosting.objects.get(id=job_id)
        app, _ = Application.objects.get_or_create(job=job, user=request.user, defaults={
            "resume_id": resume_id,
            "cover_letter_id": cover_id,
            "status": "prepared",
        })
        attach_documents_to_application(app, resume_id, cover_id)
        return Response(ApplicationSerializer(app).data)

    @action(detail=True, methods=["post"], url_path="apply")
    def apply(self, request, pk=None):
        app = Application.objects.get(id=pk, user=request.user)
        attempt = ApplicationAttempt.objects.create(application=app, outcome="pending", logs="queued")
        task = apply_to_job_task.delay(app.id)
        return Response({"status": "queued", "task_id": task.id, "attempt_id": attempt.id})

    @action(detail=True, methods=["post"], url_path="tailor-cover")
    def tailor_cover(self, request, pk=None):
        app = Application.objects.get(id=pk, user=request.user)
        doc = tailor_cover_letter(request.user, app.job, tone=request.data.get("tone", "professional"))
        app.cover_letter = doc
        app.save(update_fields=["cover_letter", "updated_at"])
        return Response(ApplicationSerializer(app).data)

    @action(detail=True, methods=["post"], url_path="tailor-resume")
    def tailor_resume(self, request, pk=None):
        app = Application.objects.get(id=pk, user=request.user)
        doc = tailor_resume(request.user, app.job)
        app.resume = doc
        app.save(update_fields=["resume", "updated_at"])
        return Response(ApplicationSerializer(app).data)


class ApplicationAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApplicationAttempt.objects.filter(application__user=self.request.user).order_by("-created_at")
