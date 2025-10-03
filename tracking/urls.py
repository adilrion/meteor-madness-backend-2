"""
Tracking URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeteorShowerViewSet, LiveTrackingSessionViewSet, MeteorActivityViewSet

router = DefaultRouter()
router.register(r'meteor-showers', MeteorShowerViewSet, basename='meteor-shower')
router.register(r'sessions', LiveTrackingSessionViewSet, basename='tracking-session')
router.register(r'activity', MeteorActivityViewSet, basename='meteor-activity')

urlpatterns = [
    path('', include(router.urls)),
]

