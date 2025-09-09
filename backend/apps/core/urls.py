from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, DocumentViewSet


router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"documents", DocumentViewSet, basename="document")

urlpatterns = router.urls

