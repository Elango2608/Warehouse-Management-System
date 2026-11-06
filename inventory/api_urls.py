from rest_framework.routers import DefaultRouter # type: ignore
from .api_views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls