"""
Orbital URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrbitalElementsViewSet, TrajectoryViewSet

router = DefaultRouter()
router.register(r'elements', OrbitalElementsViewSet, basename='orbital-elements')
router.register(r'trajectories', TrajectoryViewSet, basename='trajectory')

urlpatterns = [
    path('', include(router.urls)),
]

