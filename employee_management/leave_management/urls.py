# pyrefly: ignore [missing-import]
from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet

router = DefaultRouter()
router.register(r'requests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
