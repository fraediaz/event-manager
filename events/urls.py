from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet, EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'attendances', AttendanceViewSet, basename='attendance')

urlpatterns = router.urls
