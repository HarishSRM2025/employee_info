# pyrefly: ignore [missing-import]
from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
from .views import ActivityLogViewSet

router = DefaultRouter()
router.register(r'logs', ActivityLogViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
