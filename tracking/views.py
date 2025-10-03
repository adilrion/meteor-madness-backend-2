"""
Tracking Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta

from .models import MeteorShower, LiveTrackingSession, MeteorActivity
from .serializers import (
    MeteorShowerSerializer,
    LiveTrackingSessionSerializer,
    MeteorActivitySerializer
)


class MeteorShowerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for meteor showers
    """
    
    queryset = MeteorShower.objects.filter(is_active=True)
    serializer_class = MeteorShowerSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming meteor showers"""
        today = timezone.now().date()
        upcoming = self.queryset.filter(peak_date__gte=today).order_by('peak_date')[:10]
        
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active meteor showers"""
        today = timezone.now().date()
        active = self.queryset.filter(
            start_date__lte=today,
            end_date__gte=today
        )
        
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class LiveTrackingSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for live tracking sessions
    """
    
    queryset = LiveTrackingSession.objects.all()
    serializer_class = LiveTrackingSessionSerializer
    permission_classes = [AllowAny]


class MeteorActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for meteor activity
    """
    
    queryset = MeteorActivity.objects.all()
    serializer_class = MeteorActivitySerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current meteor activity"""
        latest = self.queryset.first()
        
        if not latest:
            return Response({'error': 'No activity data available'}, status=404)
        
        serializer = self.get_serializer(latest)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get activity history"""
        hours = int(request.query_params.get('hours', 24))
        
        cutoff = timezone.now() - timedelta(hours=hours)
        history = self.queryset.filter(timestamp__gte=cutoff)
        
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)

