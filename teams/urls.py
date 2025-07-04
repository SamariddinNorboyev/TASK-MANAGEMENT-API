from .views import TeamViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TeamViewSet, basename='user')
urlpatterns = router.urls