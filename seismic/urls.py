"""
Seismic URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeismicImpactAnalysisViewSet

router = DefaultRouter()
router.register(r'analyses', SeismicImpactAnalysisViewSet, basename='seismic-analysis')

urlpatterns = [
    path('', include(router.urls)),
]

