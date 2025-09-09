from rest_framework.routers import DefaultRouter
from .views import ProxyProfileViewSet, BrowserSessionViewSet


router = DefaultRouter()
router.register(r"proxies", ProxyProfileViewSet)
router.register(r"sessions", BrowserSessionViewSet)

urlpatterns = router.urls

