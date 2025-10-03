"""
NEO URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NEOViewSet, CloseApproachViewSet, NEOStatisticsViewSet

router = DefaultRouter()
router.register(r'objects', NEOViewSet, basename='neo')
router.register(r'close-approaches', CloseApproachViewSet, basename='close-approach')
router.register(r'statistics', NEOStatisticsViewSet, basename='neo-statistics')

urlpatterns = [
    path('', include(router.urls)),
]

