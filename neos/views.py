"""
NEO Views - API endpoints for NEO data
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import NEO, CloseApproach, NEOStatistics
from .serializers import (
    NEOListSerializer,
    NEODetailSerializer,
    CloseApproachSerializer,
    NEOStatisticsSerializer
)
from .services import NEODataService


class NEOViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Near-Earth Objects
    
    Provides list and detail views for NEO data from NASA
    """
    
    queryset = NEO.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_potentially_hazardous_asteroid', 'is_sentry_object']
    search_fields = ['name', 'neo_reference_id', 'designation']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NEODetailSerializer
        return NEOListSerializer
    
    @action(detail=False, methods=['get'])
    def potentially_hazardous(self, request):
        """Get all potentially hazardous asteroids"""
        phas = self.queryset.filter(is_potentially_hazardous_asteroid=True)
        page = self.paginate_queryset(phas)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(phas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_size(self, request):
        """Filter NEOs by size category"""
        size = request.query_params.get('size', None)
        
        if not size:
            return Response(
                {'error': 'Size parameter required: small, medium, large, very_large'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        size_ranges = {
            'small': (0, 0.1),
            'medium': (0.1, 0.5),
            'large': (0.5, 1.0),
            'very_large': (1.0, float('inf'))
        }
        
        if size not in size_ranges:
            return Response(
                {'error': 'Invalid size. Use: small, medium, large, very_large'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        min_size, max_size = size_ranges[size]
        neos = self.queryset.filter(
            estimated_diameter_max_km__gte=min_size
        )
        
        if max_size != float('inf'):
            neos = neos.filter(estimated_diameter_max_km__lt=max_size)
        
        page = self.paginate_queryset(neos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(neos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def sync_nasa_data(self, request):
        """Trigger sync with NASA NEO API"""
        service = NEODataService()
        result = service.sync_neo_data()
        
        return Response({
            'message': 'NEO data sync completed',
            'result': result
        })


class CloseApproachViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Close Approach data
    
    Provides information about NEO close approaches to Earth
    """
    
    queryset = CloseApproach.objects.all()
    serializer_class = CloseApproachSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['orbiting_body']
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming close approaches"""
        days = int(request.query_params.get('days', 7))
        
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=days)
        
        approaches = self.queryset.filter(
            close_approach_date__gte=start_date,
            close_approach_date__lte=end_date
        ).select_related('neo')
        
        serializer = self.get_serializer(approaches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def close_encounters(self, request):
        """Get very close approaches (within 10 lunar distances)"""
        threshold = float(request.query_params.get('threshold', 10))
        
        approaches = self.queryset.filter(
            miss_distance_lunar__lt=threshold
        ).select_related('neo')
        
        serializer = self.get_serializer(approaches, many=True)
        return Response(serializer.data)


class NEOStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for NEO statistics
    
    Provides aggregated statistics for dashboard display
    """
    
    queryset = NEOStatistics.objects.all()
    serializer_class = NEOStatisticsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest statistics"""
        latest_stats = self.queryset.first()
        
        if not latest_stats:
            return Response(
                {'error': 'No statistics available'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(latest_stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Recalculate statistics"""
        from .tasks import calculate_neo_statistics
        calculate_neo_statistics.delay()
        
        return Response({
            'message': 'Statistics calculation triggered'
        })

