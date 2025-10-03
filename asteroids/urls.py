"""
Asteroid URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThreatScenarioViewSet, ThreatAssessmentViewSet

router = DefaultRouter()
router.register(r'scenarios', ThreatScenarioViewSet, basename='threat-scenario')
router.register(r'assessments', ThreatAssessmentViewSet, basename='threat-assessment')

urlpatterns = [
    path('', include(router.urls)),
]

