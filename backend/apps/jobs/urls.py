from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, JobSourceViewSet, JobPostingViewSet, MatchScoreViewSet


router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"sources", JobSourceViewSet)
router.register(r"postings", JobPostingViewSet)
router.register(r"scores", MatchScoreViewSet, basename="matchscore")

urlpatterns = router.urls

