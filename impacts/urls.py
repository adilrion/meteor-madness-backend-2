"""
Impacts URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImpactEventViewSet, EarthquakeViewSet

router = DefaultRouter()
router.register(r'events', ImpactEventViewSet, basename='impact-event')
router.register(r'earthquakes', EarthquakeViewSet, basename='earthquake')

urlpatterns = [
    path('', include(router.urls)),
]

