"""
Notifications Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from .models import Notification, ThreatAlert, AlertSubscription
from .serializers import (
    NotificationSerializer,
    ThreatAlertSerializer,
    AlertSubscriptionSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for notifications
    """
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        unread = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        count = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({'marked_read': count})


class ThreatAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for threat alerts
    """
    
    queryset = ThreatAlert.objects.filter(is_active=True)
    serializer_class = ThreatAlertSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active threat alerts"""
        alerts = self.get_queryset()
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get critical alerts only"""
        critical = self.get_queryset().filter(alert_level='critical')
        serializer = self.get_serializer(critical, many=True)
        return Response(serializer.data)


class AlertSubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for alert subscriptions
    """
    
    queryset = AlertSubscription.objects.all()
    serializer_class = AlertSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

