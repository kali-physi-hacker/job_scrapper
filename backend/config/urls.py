from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/core/", include("apps.core.urls")),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/applications/", include("apps.applications.urls")),
    path("api/automation/", include("apps.automation.urls")),
    path("api/health/", lambda r: JsonResponse({"ok": True})),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
