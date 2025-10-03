"""
Safety URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmergencyChecklistViewSet,
    ResourceAllocationViewSet,
    SafetyPlanViewSet,
    MentalHealthResourceViewSet,
    ChatbotViewSet,
    ClimateImpactModelViewSet
)

router = DefaultRouter()
router.register(r'checklists', EmergencyChecklistViewSet, basename='checklist')
router.register(r'resources', ResourceAllocationViewSet, basename='resource-allocation')
router.register(r'plans', SafetyPlanViewSet, basename='safety-plan')
router.register(r'mental-health', MentalHealthResourceViewSet, basename='mental-health')
router.register(r'chatbot', ChatbotViewSet, basename='chatbot')
router.register(r'climate-models', ClimateImpactModelViewSet, basename='climate-model')

urlpatterns = [
    path('', include(router.urls)),
]

