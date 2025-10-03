"""
Notifications URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, ThreatAlertViewSet, AlertSubscriptionViewSet

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')
router.register(r'alerts', ThreatAlertViewSet, basename='threat-alert')
router.register(r'subscriptions', AlertSubscriptionViewSet, basename='alert-subscription')

urlpatterns = [
    path('', include(router.urls)),
]

