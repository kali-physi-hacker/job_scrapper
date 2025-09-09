from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProfileViewSet, DocumentViewSet, csrf_ping


router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"documents", DocumentViewSet, basename="document")

urlpatterns = [
    path("csrf/", csrf_ping),
]
urlpatterns += router.urls
