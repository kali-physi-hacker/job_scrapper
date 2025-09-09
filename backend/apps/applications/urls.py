from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, ApplicationAttemptViewSet


router = DefaultRouter()
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"attempts", ApplicationAttemptViewSet, basename="applicationattempt")

urlpatterns = router.urls

